#!/usr/bin/env python3
"""
Download problem statements from gpe-helper.setsal.dev into a local JSON file.

Usage:
    python3 fetch_problem_statements.py
    python3 fetch_problem_statements.py --pid 10416
"""

import argparse
import html
import json
import re
import time
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://gpe-helper.setsal.dev"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "problem_statements.json"
DEFAULT_PROBLEMS_DIR = Path(__file__).resolve().parent / "problems"
USER_AGENT = "Mozilla/5.0 (compatible; GPE-Helper-Fetcher/1.0)"


def fetch_json(url: str, timeout: float, retries: int = 3, backoff: float = 0.35) -> dict:
    last_error: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        req = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json,text/plain,*/*",
            },
        )
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
        except HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError(url) from exc
            last_error = exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc

        if attempt < retries:
            time.sleep(backoff * attempt)

    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def html_to_text(content: str) -> str:
    text = content.replace("\r", "\n")
    text = re.sub(r"(?is)<script.*?>.*?</script>", "", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", "", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</(p|div|h1|h2|h3|h4|h5|h6|pre|li|tr|table|ul|ol|hr)>", "\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "- ", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.replace("\u00a0", " ")

    lines = []
    for line in text.splitlines():
        cleaned = re.sub(r"[ \t]+", " ", line).strip()
        if cleaned:
            lines.append(cleaned)

    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return "\n".join(deduped).strip()


def extract_problem_url(content: str) -> Optional[str]:
    match = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"', content, flags=re.IGNORECASE)
    if not match:
        return None
    return html.unescape(match.group(1))


def collect_problem_ids(problems_dir: Path, only_pid: Optional[str]) -> list[str]:
    if only_pid:
        return [only_pid]
    pids = []
    for problem_dir in sorted(problems_dir.iterdir()):
        if problem_dir.is_dir() and (problem_dir / "problem.json").exists():
            pids.append(problem_dir.name)
    return pids


def main():
    parser = argparse.ArgumentParser(description="Fetch GPE problem statements")
    parser.add_argument("--base-url", default=BASE_URL, help="Base URL of the source site")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output JSON path")
    parser.add_argument("--problems-dir", default=str(DEFAULT_PROBLEMS_DIR), help="Local problems dir")
    parser.add_argument("--pid", default=None, help="Fetch only one problem id")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout seconds")
    args = parser.parse_args()

    problems_dir = Path(args.problems_dir).resolve()
    output_path = Path(args.output).resolve()
    pids = collect_problem_ids(problems_dir, args.pid)
    if not pids:
        raise SystemExit("No problem ids found.")

    statements = {}
    ok_count = 0
    skip_count = 0
    err_count = 0

    for pid in pids:
        snapshot_url = f"{args.base_url.rstrip('/')}/question_snapshots/contents/{pid}.json"
        try:
            payload = fetch_json(snapshot_url, timeout=args.timeout)
            content = payload.get("content", "")
            if not isinstance(content, str) or not content.strip():
                raise ValueError("content field is empty")

            description = html_to_text(content)
            if not description:
                raise ValueError("description parsed as empty")

            problem_url = extract_problem_url(content) or f"{args.base_url.rstrip('/')}/problems/{pid}"
            statements[pid] = {
                "problem_url": problem_url,
                "description": description,
            }
            ok_count += 1
            print(f"[OK]   {pid}")
        except FileNotFoundError:
            skip_count += 1
            print(f"[SKIP] {pid} (snapshot not found)")
        except Exception as exc:
            err_count += 1
            print(f"[ERR]  {pid} ({exc})")

    output = {
        "source": args.base_url.rstrip("/"),
        "count": len(statements),
        "statements": statements,
    }
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\nDone.")
    print(f"Output: {output_path}")
    print(f"Fetched: {ok_count}, Skipped: {skip_count}, Errors: {err_count}")


if __name__ == "__main__":
    main()
