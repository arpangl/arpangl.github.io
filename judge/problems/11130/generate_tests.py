#!/usr/bin/env python3
"""
Generate test cases for Problem 11130: The Priest Mathematician
Each test case is a file with multiple lines of N values, terminated by EOF.
We generate 15-20 test case files with various edge cases and corner cases.
"""

import os
import sys

# First, precompute all answers
MAXN = 10001

def solve():
    f = [0] * MAXN
    if MAXN > 1:
        f[1] = 1

    best_k = 0
    for n in range(2, MAXN):
        min_val = None
        new_best_k = best_k
        for k in range(max(1, best_k), n):
            val = 2 * f[k] + (1 << (n - k)) - 1
            if min_val is None or val < min_val:
                min_val = val
                new_best_k = k
            elif val > min_val:
                break
        f[n] = min_val
        best_k = new_best_k
    return f

f = solve()

TESTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/11130/testcases"

def write_test(idx, inputs):
    """Write a test case pair: idx.in and idx.out"""
    fname_in = os.path.join(TESTDIR, f"{idx:02d}.in")
    fname_out = os.path.join(TESTDIR, f"{idx:02d}.out")

    with open(fname_in, 'w') as fin:
        for n in inputs:
            fin.write(f"{n}\n")

    with open(fname_out, 'w') as fout:
        for n in inputs:
            fout.write(f"{f[n]}\n")

tc = 1

# Test 01: Sample input from problem statement
write_test(tc, [1, 2, 28, 64])
tc += 1

# Test 02: Edge case - single 0
write_test(tc, [0])
tc += 1

# Test 03: Edge case - single 1
write_test(tc, [1])
tc += 1

# Test 04: Small values 0-10
write_test(tc, list(range(0, 11)))
tc += 1

# Test 05: Small values 11-20
write_test(tc, list(range(11, 21)))
tc += 1

# Test 06: Triangular number boundaries (where optimal k changes)
# Triangular numbers: 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120
# The critical points where t changes are at n = t*(t+1)/2
tri = []
for t in range(1, 25):
    tn = t * (t + 1) // 2
    if tn <= 10000:
        tri.append(tn)
        if tn - 1 >= 0:
            tri.append(tn - 1)
        if tn + 1 <= 10000:
            tri.append(tn + 1)
tri = sorted(set(tri))
write_test(tc, tri)
tc += 1

# Test 07: Powers of 2
pows = [2**i for i in range(0, 14) if 2**i <= 10000]
write_test(tc, pows)
tc += 1

# Test 08: Large values near maximum
write_test(tc, [9990, 9991, 9992, 9993, 9994, 9995, 9996, 9997, 9998, 9999, 10000])
tc += 1

# Test 09: Maximum value alone
write_test(tc, [10000])
tc += 1

# Test 10: Medium values
write_test(tc, [50, 100, 200, 500, 1000, 2000, 3000, 5000, 7500])
tc += 1

# Test 11: Repeated values
write_test(tc, [64, 64, 64, 0, 0, 1, 1])
tc += 1

# Test 12: Descending order
write_test(tc, [10000, 5000, 2500, 1000, 500, 100, 50, 10, 5, 1, 0])
tc += 1

# Test 13: Values around 64 (the classic problem size)
write_test(tc, [60, 61, 62, 63, 64, 65, 66, 67, 68])
tc += 1

# Test 14: Many small values in random-ish order
import random
random.seed(42)
vals14 = [random.randint(0, 100) for _ in range(30)]
write_test(tc, vals14)
tc += 1

# Test 15: Many medium-large values
random.seed(123)
vals15 = [random.randint(100, 10000) for _ in range(20)]
write_test(tc, vals15)
tc += 1

# Test 16: Specific interesting values - perfect squares
squares = [i*i for i in range(1, 101) if i*i <= 10000]
write_test(tc, squares)
tc += 1

# Test 17: Every 1000th value
write_test(tc, list(range(0, 10001, 1000)))
tc += 1

# Test 18: Single large value in the middle range
write_test(tc, [4999, 5000, 5001])
tc += 1

print(f"Generated {tc - 1} test cases in {TESTDIR}")
