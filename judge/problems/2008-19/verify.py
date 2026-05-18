#!/usr/bin/env python3
"""Verify all test cases by re-running solution and comparing outputs."""
import subprocess
import os
import sys

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-19/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-19/solution.py"

def verify():
    files = sorted(f for f in os.listdir(TESTCASE_DIR) if f.endswith('.in'))
    all_pass = True

    for inf in files:
        idx = inf.replace('.in', '')
        outf = idx + '.out'

        in_path = os.path.join(TESTCASE_DIR, inf)
        out_path = os.path.join(TESTCASE_DIR, outf)

        with open(in_path) as f:
            input_data = f.read()
        with open(out_path) as f:
            expected = f.read()

        result = subprocess.run(
            ["python3", SOLUTION],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=120
        )

        actual = result.stdout

        if actual == expected:
            print(f"Test {idx}: PASS")
        else:
            print(f"Test {idx}: FAIL")
            # Show first diff
            exp_lines = expected.split('\n')
            act_lines = actual.split('\n')
            for i, (e, a) in enumerate(zip(exp_lines, act_lines)):
                if e != a:
                    print(f"  Line {i+1}: expected {repr(e)}, got {repr(a)}")
                    break
            if len(exp_lines) != len(act_lines):
                print(f"  Line count: expected {len(exp_lines)}, got {len(act_lines)}")
            all_pass = False

    if all_pass:
        print(f"\nAll {len(files)} tests passed!")
    else:
        print(f"\nSome tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    verify()
