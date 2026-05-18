#!/usr/bin/env python3
"""
Generate test cases for problem 10468 - Maximum Product.

Constraints:
- 1 <= N <= 18
- -10 <= S_i <= 10
- Multiple test cases per input, separated by blank lines
- EOF-terminated

We generate 18 test files, each containing 1-3 test cases.
"""

import os
import random

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10468/testcases"


def solve_case(elems):
    """Find maximum positive product of consecutive subsequence, or 0."""
    n = len(elems)
    max_prod = 0
    for i in range(n):
        prod = 1
        for j in range(i, n):
            prod *= elems[j]
            if prod > max_prod:
                max_prod = prod
    return max_prod


def format_input(cases):
    """Format list of element-lists into input string."""
    parts = []
    for elems in cases:
        parts.append(str(len(elems)))
        parts.append(' '.join(map(str, elems)))
        parts.append('')  # blank line after each case
    return '\n'.join(parts)


def format_output(cases):
    """Format output for list of element-lists."""
    parts = []
    for i, elems in enumerate(cases, 1):
        p = solve_case(elems)
        parts.append(f"Case #{i}: The maximum product is {p}.")
        parts.append('')  # blank line after each case
    return '\n'.join(parts)


def write_test(test_id, cases):
    """Write a single test file pair."""
    in_path = os.path.join(TESTCASE_DIR, f"{test_id:02d}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{test_id:02d}.out")
    with open(in_path, 'w') as f:
        f.write(format_input(cases))
    with open(out_path, 'w') as f:
        f.write(format_output(cases))


# ---- Test case definitions ----

test_id = 0

# 01: Sample test case from problem
test_id += 1
write_test(test_id, [
    [2, 4, -3],
    [2, 5, -1, 2, -1],
])

# 02: Single element positive
test_id += 1
write_test(test_id, [
    [7],
])

# 03: Single element negative -> answer is 0
test_id += 1
write_test(test_id, [
    [-5],
])

# 04: Single element zero -> answer is 0
test_id += 1
write_test(test_id, [
    [0],
])

# 05: All zeros -> answer is 0
test_id += 1
write_test(test_id, [
    [0, 0, 0, 0, 0],
])

# 06: All positive -> product of entire array
test_id += 1
write_test(test_id, [
    [1, 2, 3, 4, 5],
])

# 07: All negative, even count -> product of entire array is positive
test_id += 1
write_test(test_id, [
    [-2, -3, -4, -5],
])

# 08: All negative, odd count -> must skip one end
test_id += 1
write_test(test_id, [
    [-2, -3, -5],
])

# 09: Contains zero in the middle, breaking products
test_id += 1
write_test(test_id, [
    [3, -2, 0, 5, -1],
    [-1, 0, -1],
])

# 10: Two negatives make positive, zeros around
test_id += 1
write_test(test_id, [
    [0, -3, -7, 0],
])

# 11: Maximum possible product: 10^18 (all 10s, N=18)
test_id += 1
write_test(test_id, [
    [10] * 18,
])

# 12: Alternating positive and negative
test_id += 1
write_test(test_id, [
    [2, -3, 4, -5, 6, -7, 8],
])

# 13: Large negative product that becomes positive with even negatives
test_id += 1
write_test(test_id, [
    [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
])

# 14: Mix with zeros splitting segments
test_id += 1
write_test(test_id, [
    [5, -2, 3, 0, -4, 6, -2, 0, 7, 8],
])

# 15: All -1s, various lengths
test_id += 1
write_test(test_id, [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
])

# 16: Single element = 1
test_id += 1
write_test(test_id, [
    [1],
    [-1],
    [0],
])

# 17: N=18, random values (seeded for reproducibility)
test_id += 1
random.seed(42)
write_test(test_id, [
    [random.randint(-10, 10) for _ in range(18)],
    [random.randint(-10, 10) for _ in range(18)],
])

# 18: Stress test - multiple cases with N=18
test_id += 1
random.seed(123)
write_test(test_id, [
    [random.randint(-10, 10) for _ in range(18)],
    [random.randint(-10, 10) for _ in range(18)],
    [random.randint(-10, 10) for _ in range(18)],
])

# 19: Edge case - negative followed by zero followed by negative
test_id += 1
write_test(test_id, [
    [-5, 0, -3],
    [-1, -2, -3, -4, 0, -5, -6],
])

# 20: All elements are 10 or -10 with N=18
test_id += 1
random.seed(999)
elems = [random.choice([-10, 10]) for _ in range(18)]
write_test(test_id, [
    elems,
])

print(f"Generated {test_id} test cases.")
