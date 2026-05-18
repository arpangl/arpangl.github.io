#!/usr/bin/env python3
"""
Generate test cases for 2015-07: Minimum Path Sum

Problem: Given an r-by-c grid of non-negative integers, find the minimum path sum
from top-left to bottom-right, moving only right or down.

Input format:
  n (number of test cases)
  For each test case:
    r c
    r lines of c integers each

Output format:
  For each test case, one line with the minimum path sum.
"""

import random
import os

def solve(grid, r, c):
    """DP solution for minimum path sum."""
    dp = [[0] * c for _ in range(r)]
    dp[0][0] = grid[0][0]
    # Fill first row
    for j in range(1, c):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    # Fill first column
    for i in range(1, r):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    # Fill rest
    for i in range(1, r):
        for j in range(1, c):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    return dp[r-1][c-1]


def make_test(cases):
    """Given a list of (r, c, grid) tuples, return (input_str, output_str)."""
    n = len(cases)
    inp_lines = [str(n)]
    out_lines = []
    for (r, c, grid) in cases:
        inp_lines.append(f"{r} {c}")
        for row in grid:
            inp_lines.append(" ".join(map(str, row)))
        ans = solve(grid, r, c)
        out_lines.append(str(ans))
    return "\n".join(inp_lines) + "\n", "\n".join(out_lines) + "\n"


def random_grid(r, c, lo=0, hi=100):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def write_test(idx, inp, out):
    base = f"/Users/lambert/Documents/GPE-Helper/judge/problems/2015-07/testcases"
    tag = f"{idx:02d}"
    with open(os.path.join(base, f"{tag}.in"), "w") as f:
        f.write(inp)
    with open(os.path.join(base, f"{tag}.out"), "w") as f:
        f.write(out)
    # Verify by re-parsing
    verify(inp, out)
    print(f"  Written {tag}.in / {tag}.out")


def verify(inp, out):
    """Re-parse and verify the input/output pair."""
    lines = inp.strip().split("\n")
    idx = 0
    n = int(lines[idx]); idx += 1
    expected = out.strip().split("\n")
    assert len(expected) == n, f"Expected {n} outputs, got {len(expected)}"
    for t in range(n):
        r, c = map(int, lines[idx].split()); idx += 1
        grid = []
        for i in range(r):
            row = list(map(int, lines[idx].split()))
            assert len(row) == c, f"Row {i} has {len(row)} cols, expected {c}"
            grid.append(row)
            idx += 1
        ans = solve(grid, r, c)
        assert str(ans) == expected[t], f"Test case {t}: expected {ans}, got {expected[t]}"


def main():
    random.seed(42)
    test_id = 1

    # ===== Test 01: Sample from problem statement =====
    print("Test 01: Sample input")
    cases = [
        (3, 3, [[1,3,1],[1,5,1],[4,2,1]]),
        (4, 4, [[1,1,1,2],[2,1,1,2],[2,1,1,1],[2,1,1,1]]),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 02: 1x1 grid (single cell) =====
    print("Test 02: 1x1 grid")
    cases = [(1, 1, [[0]]), (1, 1, [[42]]), (1, 1, [[999]])]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 03: 1-row grids =====
    print("Test 03: Single row grids")
    cases = [
        (1, 5, [[1, 2, 3, 4, 5]]),
        (1, 1, [[7]]),
        (1, 10, [[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]]),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 04: 1-column grids =====
    print("Test 04: Single column grids")
    cases = [
        (5, 1, [[1],[2],[3],[4],[5]]),
        (1, 1, [[0]]),
        (10, 1, [[i] for i in range(10)]),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 05: All zeros =====
    print("Test 05: All zeros grid")
    cases = [
        (5, 5, [[0]*5 for _ in range(5)]),
        (3, 7, [[0]*7 for _ in range(3)]),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 06: All same value =====
    print("Test 06: All same value")
    cases = [
        (4, 4, [[5]*4 for _ in range(4)]),  # path length = 4+4-1 = 7, sum = 35
        (3, 3, [[1]*3 for _ in range(3)]),  # path length = 5, sum = 5
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 07: Path forced right then down =====
    print("Test 07: Optimal path is all-right-then-all-down")
    grid = [[0]*5 for _ in range(5)]
    # Make going down early very expensive
    for i in range(1, 5):
        for j in range(0, 4):
            grid[i][j] = 999
    # Top row and last column are cheap
    for j in range(5):
        grid[0][j] = 1
    for i in range(5):
        grid[i][4] = 1
    grid[0][4] = 1  # overlap
    cases = [(5, 5, grid)]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 08: Path forced down then right =====
    print("Test 08: Optimal path is all-down-then-all-right")
    grid = [[999]*5 for _ in range(5)]
    for i in range(5):
        grid[i][0] = 1
    for j in range(5):
        grid[4][j] = 1
    grid[4][0] = 1  # overlap
    cases = [(5, 5, grid)]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 09: 2x2 grids (all combos small) =====
    print("Test 09: Multiple 2x2 grids")
    cases = [
        (2, 2, [[1, 2], [3, 4]]),   # min(1+2+4, 1+3+4) = 7 vs 8 => 7
        (2, 2, [[1, 100], [1, 1]]),  # min(1+100+1, 1+1+1) = 3
        (2, 2, [[0, 0], [0, 0]]),
        (2, 2, [[999, 1], [1, 999]]),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 10: Large values in grid =====
    print("Test 10: Large values")
    cases = [
        (3, 3, [[999, 999, 999], [999, 999, 999], [999, 999, 999]]),
        (2, 2, [[1000, 1000], [1000, 1000]]),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 11: Diagonal-ish pattern =====
    print("Test 11: Diagonal pattern")
    r, c = 6, 6
    grid = [[100]*c for _ in range(r)]
    # Make diagonal cheap
    for i in range(r):
        for j in range(c):
            if abs(i - j) <= 1:
                grid[i][j] = 1
    cases = [(r, c, grid)]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 12: Random medium grid =====
    print("Test 12: Random 10x10")
    cases = [(10, 10, random_grid(10, 10, 0, 100))]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 13: Random large grid =====
    print("Test 13: Random 50x50")
    cases = [(50, 50, random_grid(50, 50, 0, 500))]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 14: Random large grid 100x100 =====
    print("Test 14: Random 100x100")
    cases = [(100, 100, random_grid(100, 100, 0, 1000))]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 15: Rectangular grids (wide) =====
    print("Test 15: Wide rectangular grids")
    cases = [
        (2, 100, random_grid(2, 100, 0, 50)),
        (3, 80, random_grid(3, 80, 0, 50)),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 16: Rectangular grids (tall) =====
    print("Test 16: Tall rectangular grids")
    cases = [
        (100, 2, random_grid(100, 2, 0, 50)),
        (80, 3, random_grid(80, 3, 0, 50)),
    ]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 17: Multiple test cases in one input =====
    print("Test 17: Many small test cases in one input")
    cases = []
    for _ in range(20):
        r = random.randint(1, 10)
        c = random.randint(1, 10)
        cases.append((r, c, random_grid(r, c, 0, 99)))
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 18: Checkerboard pattern =====
    print("Test 18: Checkerboard pattern")
    r, c = 8, 8
    grid = [[(i + j) % 2 * 99 + 1 for j in range(c)] for i in range(r)]
    cases = [(r, c, grid)]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 19: Stress test - large with many test cases =====
    print("Test 19: Stress - multiple medium grids")
    cases = []
    for _ in range(5):
        r = random.randint(30, 60)
        c = random.randint(30, 60)
        cases.append((r, c, random_grid(r, c, 0, 999)))
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    # ===== Test 20: Edge - grid with zeros except start and end =====
    print("Test 20: Zeros except corners")
    r, c = 5, 5
    grid = [[0]*c for _ in range(r)]
    grid[0][0] = 100
    grid[r-1][c-1] = 200
    cases = [(r, c, grid)]
    inp, out = make_test(cases)
    write_test(test_id, inp, out); test_id += 1

    print(f"\nDone! Generated {test_id - 1} test cases.")


if __name__ == "__main__":
    main()
