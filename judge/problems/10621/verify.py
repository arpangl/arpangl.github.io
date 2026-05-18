#!/usr/bin/env python3
"""Verify all test cases for Problem 10621: Luggage"""
import os
import glob

TESTCASES_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10621/testcases"

def can_partition(weights):
    total = sum(weights)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for w in weights:
        for j in range(target, w - 1, -1):
            if dp[j - w]:
                dp[j] = True
    return dp[target]

errors = 0
total_cases = 0

for in_file in sorted(glob.glob(os.path.join(TESTCASES_DIR, "*.in"))):
    base = in_file.replace('.in', '')
    out_file = base + '.out'
    test_name = os.path.basename(base)

    with open(in_file) as f:
        lines = f.read().strip().split('\n')
    with open(out_file) as f:
        expected = f.read().strip().split('\n')

    m = int(lines[0])
    assert len(lines) == m + 1, f"{test_name}: Expected {m+1} lines, got {len(lines)}"
    assert len(expected) == m, f"{test_name}: Expected {m} output lines, got {len(expected)}"

    for i in range(m):
        total_cases += 1
        weights = list(map(int, lines[i + 1].split()))
        n = len(weights)
        s = sum(weights)

        # Constraint checks
        if n < 1 or n > 20:
            print(f"  ERROR {test_name} case {i+1}: n={n} out of range [1,20]")
            errors += 1
        if s > 200:
            print(f"  ERROR {test_name} case {i+1}: sum={s} > 200")
            errors += 1
        if any(w < 1 for w in weights):
            print(f"  ERROR {test_name} case {i+1}: weight < 1 found")
            errors += 1

        # Verify answer
        computed = "YES" if can_partition(weights) else "NO"
        if computed != expected[i]:
            print(f"  ERROR {test_name} case {i+1}: expected={expected[i]}, computed={computed}")
            errors += 1

if errors == 0:
    print(f"ALL PASSED: {total_cases} cases across {len(glob.glob(os.path.join(TESTCASES_DIR, '*.in')))} test files verified.")
else:
    print(f"FAILED: {errors} errors found.")
