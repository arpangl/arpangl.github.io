#!/usr/bin/env python3
"""
Generate test cases for problem 10603 - Cutting Sticks.

Constraints:
  - l < 1000 (positive integer, l=0 terminates)
  - n < 50 (number of cuts)
  - 0 < c_i < l, strictly increasing
  - Input ends with l=0

We generate 18 test files covering:
  01: Sample input
  02: Single cut, minimal stick
  03: Single cut, large stick
  04: Two cuts
  05: Maximum n=49 cuts with large stick (l=999)
  06: Maximum n=49 cuts with smaller stick
  07: All cuts at consecutive positions (1,2,...,n) small stick
  08: Cuts spread far apart
  09: Cuts clustered at the left
  10: Cuts clustered at the right
  11: Cuts clustered in the middle
  12: n=1 with cut near the end
  13: Multiple test cases in one input (mixed)
  14: Large number of test cases (10 cases)
  15: Stick length 1 is impossible (min l with a cut needs l>=2), l=2 n=1
  16: Symmetric cuts
  17: n=49 with l=50 (maximum cuts for minimal room)
  18: Stress test - several max-size cases
"""

import random
import os

def solve_case(l, cuts):
    """Compute minimum cutting cost using interval DP."""
    pts = [0] + cuts + [l]
    m = len(pts)
    INF = float('inf')
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            dp[i][j] = INF
            cost = pts[j] - pts[i]
            for k in range(i + 1, j):
                val = dp[i][k] + dp[k][j] + cost
                if val < dp[i][j]:
                    dp[i][j] = val
    return dp[0][m - 1]


def generate_random_cuts(l, n):
    """Generate n strictly increasing cut positions in (0, l)."""
    positions = sorted(random.sample(range(1, l), n))
    return positions


def write_test(test_id, cases, base_dir):
    """Write a test case file pair. cases is a list of (l, cuts) tuples."""
    in_path = os.path.join(base_dir, f"{test_id:02d}.in")
    out_path = os.path.join(base_dir, f"{test_id:02d}.out")

    in_lines = []
    out_lines = []

    for l, cuts in cases:
        in_lines.append(str(l))
        in_lines.append(str(len(cuts)))
        in_lines.append(' '.join(map(str, cuts)))
        cost = solve_case(l, cuts)
        out_lines.append(f"The minimum cutting is {cost}.")

    in_lines.append("0")  # terminator

    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f"  Test {test_id:02d}: {len(cases)} case(s) written")


def main():
    random.seed(42)
    base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10603/testcases"
    os.makedirs(base_dir, exist_ok=True)

    # 01: Sample input
    write_test(1, [
        (100, [25, 50, 75]),
        (10, [4, 5, 7, 8]),
    ], base_dir)

    # 02: Single cut, minimal stick (l=2, cut at 1)
    write_test(2, [
        (2, [1]),
    ], base_dir)

    # 03: Single cut, large stick
    write_test(3, [
        (999, [500]),
    ], base_dir)

    # 04: Two cuts
    write_test(4, [
        (100, [25, 75]),
        (10, [3, 7]),
    ], base_dir)

    # 05: Maximum n=49 cuts with l=999
    cuts_05 = sorted(random.sample(range(1, 999), 49))
    write_test(5, [
        (999, cuts_05),
    ], base_dir)

    # 06: Maximum n=49 cuts with l=500
    cuts_06 = sorted(random.sample(range(1, 500), 49))
    write_test(6, [
        (500, cuts_06),
    ], base_dir)

    # 07: Consecutive cuts 1..n, small stick
    write_test(7, [
        (20, list(range(1, 20))),  # n=19 cuts at 1,2,...,19
    ], base_dir)

    # 08: Cuts spread far apart
    write_test(8, [
        (999, [100, 300, 500, 700, 900]),
    ], base_dir)

    # 09: Cuts clustered at the left
    write_test(9, [
        (999, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ], base_dir)

    # 10: Cuts clustered at the right
    write_test(10, [
        (999, [989, 990, 991, 992, 993, 994, 995, 996, 997, 998]),
    ], base_dir)

    # 11: Cuts clustered in the middle
    write_test(11, [
        (999, [495, 496, 497, 498, 499, 500, 501, 502, 503, 504]),
    ], base_dir)

    # 12: n=1 with cut near the end
    write_test(12, [
        (999, [998]),
        (999, [1]),
    ], base_dir)

    # 13: Multiple mixed test cases
    write_test(13, [
        (50, [10, 20, 30, 40]),
        (7, [1, 3, 5]),
        (100, [50]),
        (200, [1, 199]),
    ], base_dir)

    # 14: 10 random test cases
    cases_14 = []
    for _ in range(10):
        l = random.randint(2, 999)
        max_n = min(49, l - 1)
        n = random.randint(1, max_n)
        cuts = sorted(random.sample(range(1, l), n))
        cases_14.append((l, cuts))
    write_test(14, cases_14, base_dir)

    # 15: Minimal possible: l=2, n=1, cut at 1
    write_test(15, [
        (2, [1]),
        (3, [1]),
        (3, [2]),
        (3, [1, 2]),
    ], base_dir)

    # 16: Symmetric cuts
    write_test(16, [
        (100, [10, 20, 30, 40, 50, 60, 70, 80, 90]),
        (200, [50, 100, 150]),
    ], base_dir)

    # 17: n=49 with l=50 (maximum cuts for tight stick)
    write_test(17, [
        (50, list(range(1, 50))),  # n=49, cuts at 1..49
    ], base_dir)

    # 18: Stress - several max-size cases
    cases_18 = []
    for _ in range(5):
        l = random.randint(900, 999)
        cuts = sorted(random.sample(range(1, l), 49))
        cases_18.append((l, cuts))
    write_test(18, cases_18, base_dir)

    print(f"\nDone! Generated 18 test cases in {base_dir}")


if __name__ == '__main__':
    main()
