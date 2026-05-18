#!/usr/bin/env python3
"""
Generate test cases for Simple Minded Hashing (problem 11192).

Constraints: 0 < L, S < 10000. Terminated by "0 0".
Answer fits in 32-bit signed integer.

Key observations:
- Only 26 letters, so if L > 26, answer is 0.
- Min sum for L letters = L*(L+1)/2
- Max sum for L letters = L*(53-L)/2
- Max possible sum overall = 351 (all 26 letters)
- If S > 351 or S < min_sum, answer is 0.
"""

import os

def solve_case(L, S):
    """Compute answer for a single (L, S) case."""
    if L > 26 or L <= 0:
        return 0

    min_sum = L * (L + 1) // 2
    max_sum = L * (53 - L) // 2

    if S < min_sum or S > max_sum:
        return 0

    target = min(S, 351)

    dp = [[0] * (target + 1) for _ in range(L + 1)]
    dp[0][0] = 1

    for letter in range(1, 27):
        for j in range(min(letter, L), 0, -1):
            for k in range(letter, target + 1):
                dp[j][k] += dp[j - 1][k - letter]

    return dp[L][target]


# Define test cases as list of (L, S) pairs, grouped by test file
test_files = []

# Test 1: Sample cases
test_files.append([
    (3, 10),
    (2, 3),
])

# Test 2: L=1 edge cases (single letter)
test_files.append([
    (1, 1),   # "a" -> 1 way
    (1, 26),  # "z" -> 1 way
    (1, 27),  # impossible, > 26
    (1, 13),  # "m" -> 1 way
])

# Test 3: L=26 edge cases (all letters)
test_files.append([
    (26, 351),  # only one way: abcdefghijklmnopqrstuvwxyz
    (26, 350),  # impossible (min = max = 351)
    (26, 352),  # impossible
])

# Test 4: L > 26 (always 0)
test_files.append([
    (27, 100),
    (100, 500),
    (9999, 9999),
])

# Test 5: S too small (below minimum sum)
test_files.append([
    (3, 5),   # min sum for L=3 is 6, so 0
    (5, 14),  # min sum for L=5 is 15, so 0
    (2, 2),   # min sum for L=2 is 3, so 0
    (10, 54), # min sum for L=10 is 55, so 0
])

# Test 6: S too large (above max sum)
test_files.append([
    (3, 76),   # max sum for L=3 is 75, so 0
    (2, 52),   # max sum for L=2 is 51, so 0
    (1, 9999), # impossible
    (5, 9999), # impossible
])

# Test 7: Minimum valid sums (exactly min_sum)
test_files.append([
    (1, 1),    # a
    (2, 3),    # ab
    (3, 6),    # abc
    (5, 15),   # abcde
    (10, 55),  # abcdefghij
    (13, 91),  # abcdefghijklm
    (26, 351), # all letters
])

# Test 8: Maximum valid sums (exactly max_sum)
test_files.append([
    (1, 26),    # z
    (2, 51),    # yz
    (3, 75),    # xyz
    (5, 120),   # vwxyz
    (10, 215),  # qrstuvwxyz
    (13, 260),  # nopqrstuvwxyz
])

# Test 9: L=2 various sums
test_files.append([
    (2, 3),    # ab -> 1
    (2, 10),   # several combos
    (2, 27),   # many combos (middle range)
    (2, 50),   # only xz -> 1
    (2, 51),   # yz -> 1
])

# Test 10: L=13 (half the alphabet) - peak combinatorics
test_files.append([
    (13, 175),  # roughly middle sum for L=13
    (13, 170),
    (13, 180),
    (13, 91),   # min
    (13, 260),  # max
])

# Test 11: Symmetric cases (L=13 has symmetric distribution)
test_files.append([
    (13, 100),
    (13, 251),  # 351-100 = 251
    (13, 150),
    (13, 201),  # 351-150 = 201
])

# Test 12: Large L with large S (still valid)
test_files.append([
    (20, 300),
    (25, 340),
    (24, 320),
    (15, 200),
])

# Test 13: L=1 boundary values
test_files.append([
    (1, 2),
    (1, 25),
    (1, 0),    # S=0 but S > 0 per constraints... let's keep it out
])
# Actually S > 0 per constraints. Replace:
test_files[12] = [
    (1, 2),
    (1, 25),
    (1, 14),
    (1, 15),
]

# Test 14: Various mid-range
test_files.append([
    (4, 14),   # min for L=4 is 10
    (4, 98),   # max for L=4 is 102
    (6, 50),
    (8, 100),
    (10, 150),
])

# Test 15: Stress test - many queries per file
test_files.append([
    (3, 10),
    (7, 77),
    (12, 200),
    (20, 270),
    (26, 351),
    (1, 1),
    (2, 51),
    (15, 250),
    (9, 130),
    (4, 50),
])

# Test 16: Edge with large S values (S near 9999)
test_files.append([
    (26, 351),
    (1, 9998),
    (2, 9998),
    (9999, 1),
    (5000, 5000),
])

# Test 17: S=1 edge cases
test_files.append([
    (1, 1),     # "a" -> 1
    (2, 1),     # impossible (min is 3)
    (3, 1),     # impossible
])

# Test 18: All L from 1 to 26 with their min sums
test_files.append([
    (i, i * (i + 1) // 2) for i in range(1, 27)
])

outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/11192/testcases"
os.makedirs(outdir, exist_ok=True)

for idx, cases in enumerate(test_files):
    file_num = f"{idx + 1:02d}"
    in_lines = []
    out_lines = []
    for case_idx, (L, S) in enumerate(cases):
        in_lines.append(f"{L} {S}")
        ans = solve_case(L, S)
        out_lines.append(f"Case {case_idx + 1}: {ans}")
    in_lines.append("0 0")

    in_path = os.path.join(outdir, f"{file_num}.in")
    out_path = os.path.join(outdir, f"{file_num}.out")

    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f"Test {file_num}: {len(cases)} cases written")
    for case_idx, (L, S) in enumerate(cases):
        ans = solve_case(L, S)
        print(f"  Case {case_idx+1}: L={L}, S={S} -> {ans}")

print(f"\nTotal: {len(test_files)} test files generated.")
