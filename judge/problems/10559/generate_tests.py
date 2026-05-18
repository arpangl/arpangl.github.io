#!/usr/bin/env python3
"""
Generate test cases for problem 10559: I Love Big Numbers !
n <= 1000, each test case is one line with a single integer.
Input is multiple test cases until EOF.
"""

import math
import os
import random

random.seed(42)

def digit_sum_of_factorial(n):
    f = math.factorial(n)
    return sum(int(d) for d in str(f))

# Define test cases: each test case is a list of n values
test_cases = []

# 01: Sample test case
test_cases.append([5, 60, 100])

# 02: Edge case - smallest values
test_cases.append([0, 1, 2])

# 03: Single digits
test_cases.append([3, 4, 5, 6, 7, 8, 9])

# 04: Small values 10-20
test_cases.append([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

# 05: Powers of 2
test_cases.append([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])

# 06: Boundary - maximum value
test_cases.append([1000])

# 07: Large values near max
test_cases.append([990, 995, 998, 999, 1000])

# 08: Multiples of 100
test_cases.append([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])

# 09: Multiples of 50
test_cases.append([50, 150, 250, 350, 450, 550, 650, 750, 850, 950])

# 10: Random small values (1-50)
test_cases.append(sorted(random.sample(range(1, 51), 10)))

# 11: Random medium values (51-500)
test_cases.append(sorted(random.sample(range(51, 501), 10)))

# 12: Random large values (501-1000)
test_cases.append(sorted(random.sample(range(501, 1001), 10)))

# 13: Single value - just 0
test_cases.append([0])

# 14: Single value - just 1
test_cases.append([1])

# 15: Consecutive values around interesting points
test_cases.append([24, 25, 26, 49, 50, 51, 99, 100, 101])

# 16: Random mix across full range
vals = sorted(random.sample(range(0, 1001), 15))
test_cases.append(vals)

# 17: Specific interesting factorials
test_cases.append([10, 20, 50, 100, 200, 500, 1000])

# 18: Values that are factorials themselves or near them
test_cases.append([6, 24, 120, 720])

outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10559/testcases"
os.makedirs(outdir, exist_ok=True)

for i, tc in enumerate(test_cases, 1):
    infile = os.path.join(outdir, f"{i:02d}.in")
    outfile = os.path.join(outdir, f"{i:02d}.out")

    with open(infile, "w") as fin:
        for n in tc:
            fin.write(f"{n}\n")

    with open(outfile, "w") as fout:
        for n in tc:
            fout.write(f"{digit_sum_of_factorial(n)}\n")

    print(f"Test case {i:02d}: {len(tc)} values, n in [{min(tc)}, {max(tc)}]")

print(f"\nTotal: {len(test_cases)} test cases generated.")
