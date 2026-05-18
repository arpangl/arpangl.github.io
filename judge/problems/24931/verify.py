#!/usr/bin/env python3
"""Verify all test cases: run solver on each .in and compare with .out."""
import subprocess
import os
import sys

BASE = "/Users/lambert/Documents/GPE-Helper/judge/problems/24931/testcases"
SOLVER = "/Users/lambert/Documents/GPE-Helper/judge/problems/24931/solve.py"

def is_palindrome(s):
    return s == s[::-1]

all_pass = True
for i in range(1, 19):
    in_file = os.path.join(BASE, f"{i:02d}.in")
    out_file = os.path.join(BASE, f"{i:02d}.out")

    if not os.path.exists(in_file) or not os.path.exists(out_file):
        print(f"Test {i:02d}: MISSING files")
        all_pass = False
        continue

    result = subprocess.run(
        ["python3", SOLVER],
        stdin=open(in_file),
        capture_output=True, text=True, timeout=30
    )

    expected = open(out_file).read()
    got = result.stdout

    if got != expected:
        print(f"Test {i:02d}: OUTPUT MISMATCH")
        print(f"  Expected lines: {len(expected.splitlines())}")
        print(f"  Got lines:      {len(got.splitlines())}")
        # Show first difference
        exp_lines = expected.splitlines()
        got_lines = got.splitlines()
        for j, (e, g) in enumerate(zip(exp_lines, got_lines)):
            if e != g:
                print(f"  First diff at line {j}: expected[:{min(80,len(e))}]={e[:80]!r}, got[:{min(80,len(g))}]={g[:80]!r}")
                break
        all_pass = False
        continue

    # Also verify every output line is a palindrome and starts with the input
    in_lines = open(in_file).read().splitlines()
    out_lines = expected.splitlines()
    ok = True
    for j, (inp, out) in enumerate(zip(in_lines, out_lines)):
        if not out.startswith(inp):
            print(f"Test {i:02d} line {j}: output doesn't start with input")
            ok = False
            break
        if not is_palindrome(out):
            print(f"Test {i:02d} line {j}: output is NOT a palindrome (len={len(out)})")
            ok = False
            break

    if ok:
        print(f"Test {i:02d}: PASS ({len(in_lines)} cases)")
    else:
        all_pass = False

if all_pass:
    print("\nAll tests passed!")
else:
    print("\nSome tests FAILED!")
    sys.exit(1)
