#!/usr/bin/env python3
"""
Generate test cases for Tight Words (10637).

Constraints: 0 <= k <= 9, 1 <= n <= 100

Test case strategy:
  01: Sample input
  02: k=0 (only digit 0), various n — always 100%
  03: k=1 (binary), small n
  04: k=1 (binary), large n
  05: k=9, n=1 — always 100%
  06: k=9, n=2
  07: k=9, n=100 (max n, max k)
  08: k=0, n=100 (single digit, max length)
  09: k=0, n=1 (smallest possible)
  10: Various k with n=1 (all should be 100%)
  11: k=5, medium n values
  12: k=2, large n
  13: k=9, various n
  14: All k from 0..9 with n=2
  15: Mixed edge cases
  16: Large n with small k
  17: Stress test — many lines with max values
  18: k=1 with n=100
"""

import os

OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10637/testcases"

test_cases = []

# 01: Sample input
test_cases.append([
    (4, 1),
    (2, 5),
    (3, 5),
    (8, 7),
])

# 02: k=0, various n — only one digit, always tight, 100%
test_cases.append([
    (0, 1),
    (0, 2),
    (0, 5),
    (0, 10),
    (0, 50),
    (0, 100),
])

# 03: k=1 (binary), small n
test_cases.append([
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 10),
])

# 04: k=1 (binary), large n
test_cases.append([
    (1, 50),
    (1, 75),
    (1, 100),
])

# 05: k=9, n=1 — all single-digit words are tight
test_cases.append([
    (9, 1),
])

# 06: k=9, n=2
test_cases.append([
    (9, 2),
])

# 07: k=9, n=100 (max everything)
test_cases.append([
    (9, 100),
])

# 08: k=0, n=100
test_cases.append([
    (0, 100),
])

# 09: k=0, n=1 (absolute minimum)
test_cases.append([
    (0, 1),
])

# 10: All k values with n=1 (all should be 100%)
test_cases.append([
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),
    (9, 1),
])

# 11: k=5, medium n values
test_cases.append([
    (5, 2),
    (5, 5),
    (5, 10),
    (5, 20),
    (5, 50),
])

# 12: k=2, large n
test_cases.append([
    (2, 10),
    (2, 20),
    (2, 50),
    (2, 80),
    (2, 100),
])

# 13: k=9, various n
test_cases.append([
    (9, 2),
    (9, 5),
    (9, 10),
    (9, 25),
    (9, 50),
    (9, 75),
    (9, 100),
])

# 14: All k from 0..9 with n=2
test_cases.append([
    (0, 2),
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (6, 2),
    (7, 2),
    (8, 2),
    (9, 2),
])

# 15: Mixed edge/corner cases
test_cases.append([
    (0, 1),
    (9, 100),
    (1, 100),
    (5, 1),
    (3, 3),
    (7, 50),
    (4, 99),
    (6, 77),
])

# 16: Large n with small k (percentage becomes very small)
test_cases.append([
    (3, 100),
    (4, 100),
    (5, 100),
    (6, 100),
    (7, 100),
    (8, 100),
])

# 17: Stress — many lines
test_cases.append([
    (k, n) for k in range(0, 10) for n in [1, 50, 100]
])

# 18: n=2 and n=3 for all k (verify transition logic)
test_cases.append([
    (0, 2), (0, 3),
    (1, 2), (1, 3),
    (2, 2), (2, 3),
    (3, 2), (3, 3),
    (4, 2), (4, 3),
    (5, 2), (5, 3),
    (6, 2), (6, 3),
    (7, 2), (7, 3),
    (8, 2), (8, 3),
    (9, 2), (9, 3),
])

for idx, cases in enumerate(test_cases, 1):
    fname_in = os.path.join(OUTDIR, f"{idx:02d}.in")
    with open(fname_in, 'w') as f:
        for k, n in cases:
            f.write(f"{k} {n}\n")

print(f"Generated {len(test_cases)} test case input files.")
