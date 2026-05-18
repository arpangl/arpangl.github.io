#!/usr/bin/env python3
"""
Build static manifest for pure-frontend judge mode.

Usage:
    python3 build_frontend_manifest.py
"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROBLEMS_DIR = BASE_DIR / "problems"
PROBLEMS_LIST_FILE = BASE_DIR / "problems_list.json"
OUTPUT_FILE = BASE_DIR / "problems_manifest.json"
PROBLEM_SOURCE_BASE_URL = "https://gpe-helper.setsal.dev/problems"
DEFAULT_TIME_LIMIT = 3.0


def load_problem_ids() -> list[tuple[str, str]]:
    if PROBLEMS_LIST_FILE.exists():
        raw = json.loads(PROBLEMS_LIST_FILE.read_text(encoding="utf-8"))
        items = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            pid = str(item.get("pid", "")).strip()
            if not pid:
                continue
            name = str(item.get("name", pid)).strip() or pid
            items.append((pid, name))
        if items:
            return items

    items = []
    if not PROBLEMS_DIR.exists():
        return items
    for path in sorted(PROBLEMS_DIR.iterdir()):
        if path.is_dir():
            items.append((path.name, path.name))
    return items


def collect_testcase_names(problem_dir: Path) -> list[str]:
    tc_dir = problem_dir / "testcases"
    if not tc_dir.exists():
        return []

    names = []
    for in_file in sorted(tc_dir.glob("*.in")):
        out_file = in_file.with_suffix(".out")
        if out_file.exists():
            names.append(in_file.stem)
    return names


def main():
    records = []
    for pid, fallback_name in load_problem_ids():
        problem_dir = PROBLEMS_DIR / pid
        if not problem_dir.exists() or not problem_dir.is_dir():
            continue

        meta = {}
        meta_file = problem_dir / "problem.json"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {}

        testcase_names = collect_testcase_names(problem_dir)
        raw_url = meta.get("url")
        problem_url = (
            raw_url
            if isinstance(raw_url, str) and raw_url.strip()
            else f"{PROBLEM_SOURCE_BASE_URL}/{pid}"
        )
        raw_description = meta.get("description")
        description = (
            raw_description
            if isinstance(raw_description, str) and raw_description.strip()
            else ""
        )

        records.append(
            {
                "pid": pid,
                "name": str(meta.get("name", fallback_name)),
                "time_limit": float(meta.get("time_limit", DEFAULT_TIME_LIMIT)),
                "category": meta.get("category", []),
                "accept_rate": meta.get("accept_rate"),
                "description": description,
                "problem_url": problem_url,
                "testcase_count": len(testcase_names),
                "testcase_names": testcase_names,
            }
        )

    payload = {
        "count": len(records),
        "problems": records,
    }
    OUTPUT_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_FILE} ({len(records)} problems)")


if __name__ == "__main__":
    main()
