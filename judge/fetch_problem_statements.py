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
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://gpe-helper.setsal.dev"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "problem_statements.json"
DEFAULT_PROBLEMS_DIR = Path(__file__).resolve().parent / "problems"
USER_AGENT = "Mozilla/5.0 (compatible; GPE-Helper-Fetcher/1.0)"
UNDERLINE_CHAR = chr(0x2500)  # ─


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
    """Legacy flat-text converter (kept for backward compatibility)."""
    text = content.replace("\r", "\n")
    text = re.sub(r"(?is)<script.*?>.*?</script>", "", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", "", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</(p|div|h1|h2|h3|h4|h5|h6|pre|li|tr|table|ul|ol|hr)>", "\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "- ", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.replace("\u00a0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    lines = [l for l in lines if l]
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return "\n".join(deduped).strip()


def _strip_tags(s: str) -> str:
    return re.sub(r"(?s)<[^>]+>", "", s)


def _clean_inline(s: str) -> str:
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = _strip_tags(s)
    s = html.unescape(s).replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s


def _format_sample_block(block: str) -> str:
    labels = [_clean_inline(m) for m in re.findall(r"(?is)<h3[^>]*>(.*?)</h3>", block)]
    pres = re.findall(r"(?is)<pre[^>]*>(.*?)</pre>", block)
    if not pres:
        return ""
    out = []
    for idx, pre in enumerate(pres):
        label = labels[idx] if idx < len(labels) else f"Sample {idx + 1}"
        raw = _strip_tags(pre)
        raw = html.unescape(raw).replace("\r\n", "\n").replace("\r", "\n")
        raw = raw.strip("\n")
        indented = "\n".join("    " + line.rstrip() for line in raw.split("\n"))
        underline = UNDERLINE_CHAR * max(len(label), 4)
        out.append(f"\n{label}\n{underline}\n{indented}\n")
    return "\n".join(out)


def html_to_formatted_text(content: str) -> str:
    """Convert problem-snapshot HTML into readable plain text.

    Layout: section headers underlined with \u2500, sample I/O indented as code blocks.
    Designed to render well under CSS `white-space: pre-wrap`.
    """
    text = content

    # Drop trailing "Source / URL / Keyword" metadata table (always preceded by <hr />).
    text = re.sub(
        r"(?is)<hr\s*/?>\s*<table(?:(?!</table>).)*?Source:.*?</table>",
        "",
        text,
    )

    # Title (<h2>) and "Time Limit: \u2026" are already captured as metadata.
    text = re.sub(r"(?is)<h2[^>]*>.*?</h2>", "", text)
    text = re.sub(r"(?i)Time Limit:\s*[^<\n]*", "", text)

    # Sample input/output table \u2192 labeled indented blocks.
    text = re.sub(
        r'(?is)<div id="sampleinputoutput">.*?</div>',
        lambda m: _format_sample_block(m.group(0)),
        text,
    )

    # Section headers (Description / Input / Output / \u2026)
    def _h3(match: re.Match) -> str:
        title = _clean_inline(match.group(1))
        if not title:
            return ""
        underline = UNDERLINE_CHAR * max(len(title), 4)
        return f"\n\n{title}\n{underline}\n"

    text = re.sub(r"(?is)<h3[^>]*>(.*?)</h3>", _h3, text)

    # Block boundaries \u2192 newlines.
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p\s*>", "\n\n", text)
    text = re.sub(r"(?i)</(div|h4|h5|h6|tr|table|ul|ol)>", "\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "- ", text)
    text = re.sub(r"(?i)</li>", "\n", text)
    text = re.sub(r"(?i)<hr\s*/?>", "\n", text)

    text = _strip_tags(text)
    text = html.unescape(text).replace("\u00a0", " ")

    # Collapse spaces per line but preserve sample-block indentation.
    out_lines = []
    for line in text.split("\n"):
        if line.startswith("    "):
            out_lines.append(line.rstrip())
        else:
            out_lines.append(re.sub(r"[ \t]+", " ", line).strip())

    result = "\n".join(out_lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


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
        if problem_dir.is_dir() and not problem_dir.name.startswith("."):
            pids.append(problem_dir.name)
    return pids


def load_name_map(problems_dir: Path) -> dict:
    list_file = problems_dir.parent / "problems_list.json"
    if not list_file.exists():
        return {}
    try:
        data = json.loads(list_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if isinstance(data, list):
        return {item.get("pid"): item.get("name", "") for item in data if isinstance(item, dict)}
    return {}


def fetch_one(pid: str, base_url: str, timeout: float):
    snapshot_url = f"{base_url.rstrip('/')}/question_snapshots/contents/{pid}.json"
    payload = fetch_json(snapshot_url, timeout=timeout)
    content = payload.get("content", "")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("content field is empty")
    description = html_to_formatted_text(content)
    if not description:
        raise ValueError("description parsed as empty")
    problem_url = extract_problem_url(content) or f"{base_url.rstrip('/')}/problems/{pid}"
    return {"problem_url": problem_url, "description": description}


def write_back_problem_json(problems_dir: Path, pid: str, info: dict, name_map: dict) -> None:
    problem_dir = problems_dir / pid
    if not problem_dir.exists():
        return
    pj = problem_dir / "problem.json"
    if pj.exists():
        try:
            meta = json.loads(pj.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            meta = {}
    else:
        meta = {"pid": pid, "name": name_map.get(pid, ""), "time_limit": 3.0, "category": []}
    meta["description"] = info["description"]
    if not meta.get("url"):
        meta["url"] = info["problem_url"]
    pj.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="Fetch GPE problem statements")
    parser.add_argument("--base-url", default=BASE_URL, help="Base URL of the source site")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Aggregated output JSON path")
    parser.add_argument("--problems-dir", default=str(DEFAULT_PROBLEMS_DIR), help="Local problems dir")
    parser.add_argument("--pid", default=None, help="Fetch only one problem id")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout seconds")
    parser.add_argument("--workers", type=int, default=16, help="Parallel worker threads")
    parser.add_argument("--no-write-back", action="store_true", help="Skip updating each problem.json")
    args = parser.parse_args()

    problems_dir = Path(args.problems_dir).resolve()
    output_path = Path(args.output).resolve()
    pids = collect_problem_ids(problems_dir, args.pid)
    if not pids:
        raise SystemExit("No problem ids found.")
    name_map = load_name_map(problems_dir)

    statements: dict = {}
    counts = {"ok": 0, "skip": 0, "err": 0}
    counts_lock = threading.Lock()
    print_lock = threading.Lock()

    def task(pid: str):
        try:
            info = fetch_one(pid, args.base_url, args.timeout)
            with counts_lock:
                statements[pid] = info
                counts["ok"] += 1
            with print_lock:
                print(f"[OK]   {pid}")
            if not args.no_write_back:
                write_back_problem_json(problems_dir, pid, info, name_map)
        except FileNotFoundError:
            with counts_lock:
                counts["skip"] += 1
            with print_lock:
                print(f"[SKIP] {pid} (snapshot not found)")
        except Exception as exc:
            with counts_lock:
                counts["err"] += 1
            with print_lock:
                print(f"[ERR]  {pid} ({exc})")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(task, pid) for pid in pids]
        for _ in as_completed(futures):
            pass

    output = {
        "source": args.base_url.rstrip("/"),
        "count": len(statements),
        "statements": dict(sorted(statements.items())),
    }
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\nDone.")
    print(f"Output: {output_path}")
    print(f"Fetched: {counts['ok']}, Skipped: {counts['skip']}, Errors: {counts['err']}")


if __name__ == "__main__":
    main()
