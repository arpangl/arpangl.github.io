#!/usr/bin/env python3
"""
GPE Judge - A simple online judge system for GPE problems.
Supports C++14 and Python 3.9 submissions.

Usage:
    python judge.py <problem_id> <source_file> [--time-limit SEC] [--memory-limit MB]
    python judge.py --list                     # List all available problems
    python judge.py --info <problem_id>        # Show problem info
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import shutil
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────
JUDGE_DIR = Path(__file__).parent
PROBLEMS_DIR = JUDGE_DIR / "problems"
DEFAULT_TIME_LIMIT = 3.0   # seconds
DEFAULT_MEMORY_LIMIT = 256  # MB


def _is_python39(executable: str) -> bool:
    try:
        result = subprocess.run(
            [executable, "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and result.stdout.strip() == "3.9"


def detect_python39_executable() -> Optional[str]:
    """Resolve a Python 3.9 executable path."""
    candidates = []
    for cmd in ("python3.9", "python3"):
        resolved = shutil.which(cmd)
        if resolved:
            candidates.append(resolved)

    # Common macOS system path (can be Python 3.9 even when python3.9 is missing).
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python):
        candidates.append(system_python)

    checked = set()
    for executable in candidates:
        if executable in checked:
            continue
        checked.add(executable)
        if _is_python39(executable):
            return executable
    return None


PYTHON39_EXECUTABLE = detect_python39_executable()


class Verdict(Enum):
    AC = "Accepted"
    WA = "Wrong Answer"
    TLE = "Time Limit Exceeded"
    RE = "Runtime Error"
    CE = "Compilation Error"
    SE = "System Error"


@dataclass
class TestResult:
    verdict: Verdict
    time_ms: float = 0.0
    testcase: str = ""
    expected: str = ""
    actual: str = ""
    error_msg: str = ""


@dataclass
class JudgeResult:
    problem_id: str
    source_file: str
    language: str
    results: list = field(default_factory=list)
    total: int = 0
    passed: int = 0

    @property
    def verdict(self) -> Verdict:
        if not self.results:
            return Verdict.SE
        for r in self.results:
            if r.verdict != Verdict.AC:
                return r.verdict
        return Verdict.AC


# ── Color output helpers ───────────────────────────────────────────────
class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def verdict_color(v: Verdict) -> str:
        if v == Verdict.AC:
            return Color.GREEN
        elif v in (Verdict.WA, Verdict.RE, Verdict.CE):
            return Color.RED
        elif v == Verdict.TLE:
            return Color.YELLOW
        return Color.CYAN


def detect_language(source_file: str) -> str:
    ext = Path(source_file).suffix.lower()
    if ext in (".cpp", ".cc", ".cxx", ".c++"):
        return "cpp"
    elif ext in (".py", ".python"):
        return "python"
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Use .cpp or .py")


def compile_cpp(source_file: str, output_binary: str) -> Optional[str]:
    """Compile C++14 source. Returns error message on failure, None on success."""
    cmd = [
        "g++", "-std=c++14", "-O2", "-Wall",
        "-o", output_binary, source_file,
        "-lm"
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return result.stderr
        return None
    except subprocess.TimeoutExpired:
        return "Compilation timed out (30s)"
    except FileNotFoundError:
        return "g++ not found. Please install a C++ compiler."


def run_testcase(
    executable: str,
    language: str,
    input_data: str,
    time_limit: float
) -> tuple[str, float, Optional[str]]:
    """
    Run executable with input_data.
    Returns (stdout, elapsed_ms, error_message_or_None).
    """
    if language == "cpp":
        cmd = [executable]
    else:
        if not PYTHON39_EXECUTABLE:
            return "", 0, "Python 3.9 executable not found (tried python3.9/python3)."
        cmd = [PYTHON39_EXECUTABLE, executable]

    try:
        start = time.monotonic()
        proc = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=time_limit + 0.5  # small grace period
        )
        elapsed = (time.monotonic() - start) * 1000  # ms

        if elapsed > time_limit * 1000:
            return "", elapsed, "TLE"

        if proc.returncode != 0:
            return "", elapsed, f"Runtime Error (exit code {proc.returncode})\n{proc.stderr[:500]}"

        return proc.stdout, elapsed, None

    except subprocess.TimeoutExpired:
        elapsed = time_limit * 1000
        return "", elapsed, "TLE"
    except Exception as e:
        return "", 0, str(e)


def normalize_output(text: str) -> str:
    """Normalize output for comparison: strip trailing whitespace per line, strip trailing newlines."""
    lines = text.rstrip("\n").split("\n")
    return "\n".join(line.rstrip() for line in lines)


def compare_outputs(expected: str, actual: str) -> bool:
    return normalize_output(expected) == normalize_output(actual)


def get_testcases(problem_id: str) -> list[tuple[str, str, str]]:
    """Get list of (name, input_path, output_path) for a problem."""
    tc_dir = PROBLEMS_DIR / problem_id / "testcases"
    if not tc_dir.exists():
        return []

    testcases = []
    for f in sorted(tc_dir.glob("*.in")):
        out_file = f.with_suffix(".out")
        if out_file.exists():
            testcases.append((f.stem, str(f), str(out_file)))

    return testcases


def judge(
    problem_id: str,
    source_file: str,
    time_limit: float = DEFAULT_TIME_LIMIT,
    memory_limit: int = DEFAULT_MEMORY_LIMIT,
) -> JudgeResult:
    """Judge a submission against all test cases."""

    source_file = os.path.abspath(source_file)
    if not os.path.exists(source_file):
        result = JudgeResult(problem_id, source_file, "unknown")
        result.results.append(TestResult(
            verdict=Verdict.SE, error_msg=f"Source file not found: {source_file}"
        ))
        return result

    language = detect_language(source_file)
    jr = JudgeResult(problem_id, source_file, language)

    # Check problem exists
    problem_dir = PROBLEMS_DIR / problem_id
    if not problem_dir.exists():
        jr.results.append(TestResult(
            verdict=Verdict.SE, error_msg=f"Problem {problem_id} not found"
        ))
        return jr

    # Load problem metadata for time limit override
    meta_file = problem_dir / "problem.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            time_limit = meta.get("time_limit", time_limit)

    # Compile if C++
    executable = source_file
    tmp_dir = None
    if language == "cpp":
        tmp_dir = tempfile.mkdtemp(prefix="gpe_judge_")
        binary_path = os.path.join(tmp_dir, "solution")
        err = compile_cpp(source_file, binary_path)
        if err:
            jr.results.append(TestResult(
                verdict=Verdict.CE, error_msg=err
            ))
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return jr
        executable = binary_path

    # Run test cases
    testcases = get_testcases(problem_id)
    if not testcases:
        jr.results.append(TestResult(
            verdict=Verdict.SE, error_msg="No test cases found for this problem"
        ))
        if tmp_dir:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        return jr

    jr.total = len(testcases)

    for name, in_path, out_path in testcases:
        with open(in_path) as f:
            input_data = f.read()
        with open(out_path) as f:
            expected = f.read()

        stdout, elapsed, error = run_testcase(executable, language, input_data, time_limit)

        if error == "TLE":
            jr.results.append(TestResult(
                verdict=Verdict.TLE, time_ms=elapsed, testcase=name
            ))
        elif error:
            jr.results.append(TestResult(
                verdict=Verdict.RE, time_ms=elapsed, testcase=name, error_msg=error
            ))
        elif compare_outputs(expected, stdout):
            jr.results.append(TestResult(
                verdict=Verdict.AC, time_ms=elapsed, testcase=name
            ))
            jr.passed += 1
        else:
            jr.results.append(TestResult(
                verdict=Verdict.WA, time_ms=elapsed, testcase=name,
                expected=expected[:200], actual=stdout[:200]
            ))

    if tmp_dir:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return jr


def print_result(jr: JudgeResult):
    """Pretty-print judge result."""
    c = Color

    print(f"\n{c.BOLD}{'='*60}{c.RESET}")
    print(f"{c.BOLD}Problem:{c.RESET} {jr.problem_id}")
    print(f"{c.BOLD}Source:{c.RESET}  {jr.source_file}")
    print(f"{c.BOLD}Language:{c.RESET} {'C++14' if jr.language == 'cpp' else 'Python 3.9'}")
    print(f"{c.BOLD}{'='*60}{c.RESET}\n")

    for r in jr.results:
        vc = Color.verdict_color(r.verdict)
        status = f"{vc}{c.BOLD}{r.verdict.value}{c.RESET}"

        if r.verdict == Verdict.CE:
            print(f"  {status}")
            print(f"    {r.error_msg}")
            continue

        if r.verdict == Verdict.SE:
            print(f"  {status}: {r.error_msg}")
            continue

        time_str = f"{r.time_ms:.0f}ms" if r.time_ms > 0 else ""
        print(f"  Test {r.testcase:>3s}  {status}  {time_str}")

        if r.verdict == Verdict.WA:
            print(f"    Expected: {r.expected[:80]}...")
            print(f"    Actual:   {r.actual[:80]}...")
        elif r.verdict == Verdict.RE:
            print(f"    {r.error_msg[:120]}")

    print(f"\n{c.BOLD}{'─'*60}{c.RESET}")
    overall_vc = Color.verdict_color(jr.verdict)
    print(f"  Result: {overall_vc}{c.BOLD}{jr.verdict.value}{c.RESET}  "
          f"({jr.passed}/{jr.total} passed)")
    print(f"{c.BOLD}{'='*60}{c.RESET}\n")


def list_problems():
    """List all available problems."""
    c = Color
    print(f"\n{c.BOLD}Available Problems:{c.RESET}\n")

    if not PROBLEMS_DIR.exists():
        print("  No problems directory found.")
        return

    problems = sorted(PROBLEMS_DIR.iterdir())
    if not problems:
        print("  No problems found.")
        return

    for p in problems:
        if not p.is_dir():
            continue
        meta_file = p / "problem.json"
        name = p.name
        tc_count = len(list((p / "testcases").glob("*.in"))) if (p / "testcases").exists() else 0

        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
                name = meta.get("name", name)
                tl = meta.get("time_limit", DEFAULT_TIME_LIMIT)
        else:
            tl = DEFAULT_TIME_LIMIT

        print(f"  {c.CYAN}{p.name:>10s}{c.RESET}  {name:<50s}  "
              f"({tc_count} tests, {tl}s TL)")

    print()


def show_problem_info(problem_id: str):
    """Show detailed problem info."""
    c = Color
    problem_dir = PROBLEMS_DIR / problem_id

    if not problem_dir.exists():
        print(f"Problem {problem_id} not found.")
        return

    meta_file = problem_dir / "problem.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
        print(f"\n{c.BOLD}Problem {problem_id}{c.RESET}")
        print(f"  Name: {meta.get('name', 'N/A')}")
        print(f"  Time Limit: {meta.get('time_limit', DEFAULT_TIME_LIMIT)}s")
        print(f"  Categories: {', '.join(meta.get('category', [])) or 'N/A'}")
        print(f"  AcceptRate: {meta.get('accept_rate', 'N/A')}%")

    testcases = get_testcases(problem_id)
    print(f"  Test cases: {len(testcases)}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="GPE Judge - Judge C++14/Python3 submissions"
    )
    parser.add_argument("problem_id", nargs="?", help="Problem ID")
    parser.add_argument("source_file", nargs="?", help="Source file (.cpp or .py)")
    parser.add_argument("--time-limit", type=float, default=None, help="Time limit in seconds")
    parser.add_argument("--memory-limit", type=int, default=DEFAULT_MEMORY_LIMIT, help="Memory limit in MB")
    parser.add_argument("--list", action="store_true", help="List all problems")
    parser.add_argument("--info", type=str, help="Show problem info")

    args = parser.parse_args()

    if args.list:
        list_problems()
        return

    if args.info:
        show_problem_info(args.info)
        return

    if not args.problem_id or not args.source_file:
        parser.print_help()
        return

    time_limit = args.time_limit if args.time_limit else DEFAULT_TIME_LIMIT

    jr = judge(args.problem_id, args.source_file, time_limit, args.memory_limit)
    print_result(jr)

    # Exit with non-zero if not AC
    sys.exit(0 if jr.verdict == Verdict.AC else 1)


if __name__ == "__main__":
    main()
