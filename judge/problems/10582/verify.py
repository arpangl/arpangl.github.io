#!/usr/bin/env python3
"""
Verify all test cases for Problem 10582: Power Strings
using the KMP failure function approach (independent from the brute-force generator).
"""

import os
import glob

TESTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10582/testcases"


def solve_kmp(s):
    """
    Find the largest n such that s = a^n using KMP failure function.

    The key insight: build the failure (partial match) table for s.
    If len(s) is divisible by (len(s) - fail[-1] - 1), then the minimal
    period is (len(s) - fail[-1] - 1), and n = len(s) / period.
    Otherwise n = 1.

    Note: fail[i] = length of longest proper prefix of s[0..i] that is also a suffix,
    minus 1 (i.e., fail[i] is the index of the last char of that prefix).
    We use the convention where fail[i] = -1 means no proper prefix match.
    """
    n = len(s)
    if n == 0:
        return 1

    # Build KMP failure table
    fail = [-1] * n
    k = -1
    for i in range(1, n):
        while k >= 0 and s[k + 1] != s[i]:
            k = fail[k]
        if s[k + 1] == s[i]:
            k += 1
        fail[i] = k

    # The minimal period length
    period = n - fail[n - 1] - 1

    if n % period == 0:
        return n // period
    else:
        return 1


def solve_bruteforce(s):
    """Brute force: try all period lengths that divide len(s)."""
    n = len(s)
    for period in range(1, n + 1):
        if n % period != 0:
            continue
        base = s[:period]
        reps = n // period
        if base * reps == s:
            return reps
    return 1


def main():
    in_files = sorted(glob.glob(os.path.join(TESTDIR, "*.in")))

    total_strings = 0
    all_ok = True

    for in_file in in_files:
        case_name = os.path.basename(in_file).replace('.in', '')
        out_file = in_file.replace('.in', '.out')

        with open(in_file, 'r') as f:
            in_lines = f.read().split('\n')

        with open(out_file, 'r') as f:
            expected_outputs = f.read().strip().split('\n')

        idx = 0
        for line in in_lines:
            line = line.rstrip('\r\n')
            if line == '.':
                break
            if line == '':
                continue

            ans_kmp = solve_kmp(line)
            ans_bf = solve_bruteforce(line)
            expected = int(expected_outputs[idx])

            if ans_kmp != expected or ans_bf != expected:
                print(f"MISMATCH in case {case_name}, string #{idx+1}:")
                display = line if len(line) <= 60 else line[:57] + "..."
                print(f"  string: \"{display}\" (len={len(line)})")
                print(f"  expected: {expected}, kmp: {ans_kmp}, bruteforce: {ans_bf}")
                all_ok = False

            # Also verify: base * n == s
            period = len(line) // expected
            base = line[:period]
            assert base * expected == line, f"Verification failed for case {case_name}, string #{idx+1}"

            idx += 1
            total_strings += 1

        if idx != len(expected_outputs):
            print(f"MISMATCH in case {case_name}: {idx} strings in input but {len(expected_outputs)} outputs")
            all_ok = False

    if all_ok:
        print(f"ALL {len(in_files)} test cases verified ({total_strings} total strings). No mismatches found.")
    else:
        print("VERIFICATION FAILED - see mismatches above.")


if __name__ == '__main__':
    main()
