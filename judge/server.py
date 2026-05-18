#!/usr/bin/env python3
"""
GPE Judge Web Server

Provides:
- Static frontend at /
- JSON APIs:
  - GET  /api/health
  - GET  /api/problems
  - GET  /api/problems/<problem_id>
  - POST /api/judge
"""

import argparse
import json
import re
import tempfile
import traceback
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError

import judge as judge_core


BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
PROBLEMS_DIR = BASE_DIR / "problems"
PROBLEMS_LIST_FILE = BASE_DIR / "problems_list.json"
MAX_CODE_SIZE = 200_000
PROBLEM_SOURCE_BASE_URL = "https://gpe-helper.setsal.dev/problems"
PROBLEM_CONTENT_BASE_URL = "https://gpe-helper.setsal.dev/question_snapshots/contents"

SUPPORTED_LANGUAGES = {
    "cpp14": {"suffix": ".cpp", "label": "C++14"},
    "python39": {"suffix": ".py", "label": "Python 3.9"},
}

PROBLEM_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]+$")


def _load_json_file(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate_problem_id(problem_id: str):
    if not problem_id or not PROBLEM_ID_PATTERN.fullmatch(problem_id):
        raise ValueError("Invalid problem_id format")


def _problem_dir(problem_id: str) -> Path:
    _validate_problem_id(problem_id)
    problem_path = PROBLEMS_DIR / problem_id
    if not problem_path.exists() or not problem_path.is_dir():
        raise FileNotFoundError(f"Problem {problem_id} not found")
    return problem_path


def _problem_testcase_count(problem_id: str) -> int:
    tc_dir = _problem_dir(problem_id) / "testcases"
    if not tc_dir.exists():
        return 0
    return len(list(tc_dir.glob("*.in")))


def _truncate_text(text: str, limit: int = 900) -> str:
    normalized = text.rstrip("\n")
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[:limit]}\n... (truncated)"


def _problem_samples(problem_id: str, sample_limit: int = 2) -> list:
    tc_dir = _problem_dir(problem_id) / "testcases"
    if not tc_dir.exists():
        return []

    pairs = []
    for in_file in sorted(tc_dir.glob("*.in")):
        out_file = in_file.with_suffix(".out")
        if out_file.exists():
            pairs.append((in_file, out_file))
        if len(pairs) >= sample_limit:
            break

    samples = []
    for in_file, out_file in pairs:
        input_text = in_file.read_text(encoding="utf-8", errors="ignore")
        output_text = out_file.read_text(encoding="utf-8", errors="ignore")
        samples.append(
            {
                "name": in_file.stem,
                "input": _truncate_text(input_text),
                "output": _truncate_text(output_text),
            }
        )
    return samples


def _problem_detail(problem_id: str) -> dict:
    problem_path = _problem_dir(problem_id)
    meta_path = problem_path / "problem.json"
    meta = {}
    if meta_path.exists():
        meta = _load_json_file(meta_path)

    raw_description = meta.get("description")
    description = raw_description if isinstance(raw_description, str) and raw_description.strip() else ""
    raw_problem_url = meta.get("url")
    problem_url = raw_problem_url if isinstance(raw_problem_url, str) and raw_problem_url.strip() else (
        f"{PROBLEM_SOURCE_BASE_URL}/{problem_id}"
    )

    return {
        "pid": problem_id,
        "name": meta.get("name", problem_id),
        "time_limit": meta.get("time_limit", judge_core.DEFAULT_TIME_LIMIT),
        "category": meta.get("category", []),
        "accept_rate": meta.get("accept_rate"),
        "testcase_count": _problem_testcase_count(problem_id),
        "description": description,
        "problem_url": problem_url,
        "samples": _problem_samples(problem_id),
    }


def load_problem_list() -> list:
    if PROBLEMS_LIST_FILE.exists():
        raw = _load_json_file(PROBLEMS_LIST_FILE)
        problems = []
        for item in raw:
            if not isinstance(item, dict) or "pid" not in item:
                continue
            pid = str(item["pid"])
            name = str(item.get("name", pid))
            try:
                tc_count = _problem_testcase_count(pid)
            except (FileNotFoundError, ValueError):
                continue
            problems.append({"pid": pid, "name": name, "testcase_count": tc_count})
        return problems

    # Fallback: build from directory layout.
    problems = []
    if not PROBLEMS_DIR.exists():
        return problems
    for item in sorted(PROBLEMS_DIR.iterdir()):
        if not item.is_dir():
            continue
        pid = item.name
        try:
            detail = _problem_detail(pid)
        except (FileNotFoundError, ValueError):
            continue
        problems.append(
            {"pid": pid, "name": detail["name"], "testcase_count": detail["testcase_count"]}
        )
    return problems


def _parse_positive_float(value, field_name: str):
    if value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")
    if parsed <= 0:
        raise ValueError(f"{field_name} must be > 0")
    return parsed


def _parse_positive_int(value, field_name: str):
    if value is None:
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an integer")
    if parsed <= 0:
        raise ValueError(f"{field_name} must be > 0")
    return parsed


def _serialize_judge_result(jr: judge_core.JudgeResult) -> dict:
    language_key = "cpp14" if jr.language == "cpp" else "python39"
    return {
        "problem_id": jr.problem_id,
        "language": language_key,
        "language_label": SUPPORTED_LANGUAGES[language_key]["label"],
        "overall_verdict": jr.verdict.name,
        "overall_label": jr.verdict.value,
        "passed": jr.passed,
        "total": jr.total,
        "results": [
            {
                "testcase": r.testcase,
                "verdict": r.verdict.name,
                "label": r.verdict.value,
                "time_ms": round(r.time_ms, 2),
                "expected": r.expected,
                "actual": r.actual,
                "error_msg": r.error_msg,
            }
            for r in jr.results
        ],
    }


def judge_submission(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object")

    problem_id = str(payload.get("problem_id", "")).strip()
    language = str(payload.get("language", "")).strip().lower()
    code = payload.get("code")

    if not problem_id:
        raise ValueError("problem_id is required")
    _problem_dir(problem_id)

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError("language must be one of: cpp14, python39")

    if not isinstance(code, str) or not code.strip():
        raise ValueError("code is required")
    if len(code.encode("utf-8")) > MAX_CODE_SIZE:
        raise ValueError(f"code exceeds max size ({MAX_CODE_SIZE} bytes)")

    req_time_limit = _parse_positive_float(payload.get("time_limit"), "time_limit")
    req_memory_limit = _parse_positive_int(payload.get("memory_limit"), "memory_limit")

    time_limit = req_time_limit if req_time_limit is not None else judge_core.DEFAULT_TIME_LIMIT
    memory_limit = (
        req_memory_limit if req_memory_limit is not None else judge_core.DEFAULT_MEMORY_LIMIT
    )

    source_suffix = SUPPORTED_LANGUAGES[language]["suffix"]

    with tempfile.TemporaryDirectory(prefix="gpe_submission_") as tmp_dir:
        source_path = Path(tmp_dir) / f"solution{source_suffix}"
        source_path.write_text(code, encoding="utf-8")
        jr = judge_core.judge(problem_id, str(source_path), time_limit, memory_limit)
    return _serialize_judge_result(jr)


class JudgeRequestHandler(SimpleHTTPRequestHandler):
    server_version = "GPEJudge/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def _send_json(self, payload: dict, status: int = HTTPStatus.OK):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ValueError("Missing Content-Length")
        try:
            length = int(raw_length)
        except ValueError:
            raise ValueError("Invalid Content-Length")
        if length <= 0:
            raise ValueError("Empty request body")

        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc.msg}")
        return payload

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self._send_json(
                {
                    "status": "ok",
                    "languages": [
                        {"key": key, "label": info["label"]}
                        for key, info in SUPPORTED_LANGUAGES.items()
                    ],
                }
            )
            return

        if path == "/api/problems":
            self._send_json({"problems": load_problem_list()})
            return

        if path.startswith("/api/problems/") and path.endswith("/content"):
            problem_id = unquote(path[len("/api/problems/"):-len("/content")]).strip()
            try:
                _validate_problem_id(problem_id)
            except ValueError as exc:
                self._send_json({"error": "invalid_request", "message": str(exc)}, HTTPStatus.BAD_REQUEST)
                return
            try:
                url = f"{PROBLEM_CONTENT_BASE_URL}/{problem_id}.json"
                req = Request(url, headers={"User-Agent": "GPEJudge/1.0"})
                with urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                self._send_json(data)
            except URLError as exc:
                self._send_json({"error": "upstream_error", "message": str(exc)}, HTTPStatus.BAD_GATEWAY)
            except Exception as exc:
                self._send_json({"error": "internal_error", "message": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        if path.startswith("/api/problems/"):
            problem_id = unquote(path[len("/api/problems/") :]).strip()
            try:
                detail = _problem_detail(problem_id)
            except ValueError as exc:
                self._send_json({"error": "invalid_request", "message": str(exc)}, HTTPStatus.BAD_REQUEST)
                return
            except FileNotFoundError as exc:
                self._send_json({"error": "not_found", "message": str(exc)}, HTTPStatus.NOT_FOUND)
                return
            self._send_json(detail)
            return

        # Static frontend
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/judge":
            self._send_json({"error": "not_found", "message": "Endpoint not found"}, HTTPStatus.NOT_FOUND)
            return

        try:
            payload = self._read_json_body()
            result = judge_submission(payload)
            self._send_json(result)
        except ValueError as exc:
            self._send_json({"error": "invalid_request", "message": str(exc)}, HTTPStatus.BAD_REQUEST)
        except FileNotFoundError as exc:
            self._send_json({"error": "not_found", "message": str(exc)}, HTTPStatus.NOT_FOUND)
        except Exception as exc:
            traceback.print_exc()
            self._send_json(
                {"error": "internal_error", "message": f"Server error: {exc}"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )


def main():
    parser = argparse.ArgumentParser(description="GPE Judge Web Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    args = parser.parse_args()

    if not WEB_DIR.exists():
        raise FileNotFoundError(f"Frontend directory not found: {WEB_DIR}")

    server = ThreadingHTTPServer((args.host, args.port), JudgeRequestHandler)
    print(f"GPE Judge server running at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
