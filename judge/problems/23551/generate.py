#!/usr/bin/env python3
"""
Generate test cases for Problem 23551: Largest Square

Problem: Given an M x N grid of characters and Q queries (r, c),
find the side length of the largest square centered at (r, c)
where all characters in the square are the same.

Key insight: The square must be centered at (r,c), so the side length
must be odd: 1, 3, 5, ... The max possible side is limited by
distance to edges and by uniformity of characters.
"""

import os
import random
import string

OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/23551/testcases"


def solve(grid, M, N, queries):
    """Compute the largest square side length centered at (r,c) with all same chars."""
    results = []
    for r, c in queries:
        ch = grid[r][c]
        # Max possible half-side (radius) limited by distance to edges
        max_k = min(r, c, M - 1 - r, N - 1 - c)
        best = 1  # side length 1 always works
        for k in range(1, max_k + 1):
            # Check if all chars in the square from (r-k, c-k) to (r+k, c+k) are ch
            # We only need to check the new border added at radius k
            ok = True
            # Top row and bottom row of the new border
            for col in range(c - k, c + k + 1):
                if grid[r - k][col] != ch or grid[r + k][col] != ch:
                    ok = False
                    break
            if ok:
                # Left col and right col of the new border (excluding corners already checked)
                for row in range(r - k + 1, r + k):
                    if grid[row][c - k] != ch or grid[row][c + k] != ch:
                        ok = False
                        break
            if ok:
                best = 2 * k + 1
            else:
                break
        results.append(best)
    return results


def make_test(test_cases):
    """Given a list of (grid, queries) tuples, return (input_str, output_str)."""
    T = len(test_cases)
    inp_lines = [str(T)]
    out_lines = []
    for grid, queries in test_cases:
        M = len(grid)
        N = len(grid[0])
        Q = len(queries)
        inp_lines.append(f"{M} {N} {Q}")
        for row in grid:
            inp_lines.append(row)
        for r, c in queries:
            inp_lines.append(f"{r} {c}")
        results = solve(grid, M, N, queries)
        out_lines.append(f"{M} {N} {Q}")
        for res in results:
            out_lines.append(str(res))
    return "\n".join(inp_lines) + "\n", "\n".join(out_lines) + "\n"


def write_test(idx, inp, out):
    prefix = f"{idx:02d}"
    with open(os.path.join(OUTDIR, f"{prefix}.in"), "w") as f:
        f.write(inp)
    with open(os.path.join(OUTDIR, f"{prefix}.out"), "w") as f:
        f.write(out)
    print(f"  Written {prefix}.in / {prefix}.out")


def random_grid(M, N, chars="ab", block_prob=None):
    """Generate a random grid."""
    grid = []
    for i in range(M):
        row = "".join(random.choice(chars) for _ in range(N))
        grid.append(row)
    return grid


def uniform_grid(M, N, ch='a'):
    return [ch * N for _ in range(M)]


def checkerboard_grid(M, N):
    grid = []
    for i in range(M):
        row = ""
        for j in range(N):
            row += 'a' if (i + j) % 2 == 0 else 'b'
        grid.append(row)
    return grid


def block_grid(M, N):
    """Grid with rectangular blocks of same characters."""
    grid = [['a'] * N for _ in range(M)]
    # Place some random blocks
    for _ in range(5):
        ch = random.choice('bcde')
        r1 = random.randint(0, M - 1)
        c1 = random.randint(0, N - 1)
        r2 = random.randint(r1, min(M - 1, r1 + random.randint(1, 15)))
        c2 = random.randint(c1, min(N - 1, c1 + random.randint(1, 15)))
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1):
                grid[i][j] = ch
    return ["".join(row) for row in grid]


# ============================================================
# Generate all test cases
# ============================================================
random.seed(42)
test_idx = 1

# ------ TC 01: Sample test case from problem statement ------
print("TC 01: Sample from problem")
grid = [
    "abbbaaaaaa",
    "abbbaaaaaa",
    "abbbaaaaaa",
    "aaaaaaaaaa",
    "aaaaaaaaaa",
    "aaccaaaaaa",
    "aaccaaaaaa",
]
queries = [(1, 2), (2, 4), (4, 6), (5, 2)]
inp, out = make_test([(grid, queries)])
write_test(1, inp, out)

# ------ TC 02: 1x1 matrix ------
print("TC 02: 1x1 matrix")
grid = ["z"]
queries = [(0, 0)]
inp, out = make_test([(grid, queries)])
write_test(2, inp, out)

# ------ TC 03: All zeros (single char) small ------
print("TC 03: All same char 5x5")
grid = uniform_grid(5, 5, 'a')
queries = [(0, 0), (2, 2), (4, 4), (0, 4), (1, 1)]
inp, out = make_test([(grid, queries)])
write_test(3, inp, out)

# ------ TC 04: All different chars (checkerboard) ------
print("TC 04: Checkerboard 6x6")
grid = checkerboard_grid(6, 6)
queries = [(0, 0), (1, 1), (2, 3), (3, 3), (5, 5)]
inp, out = make_test([(grid, queries)])
write_test(4, inp, out)

# ------ TC 05: Single row ------
print("TC 05: Single row")
grid = ["aaabbbaaaa"]
queries = [(0, 1), (0, 4), (0, 0), (0, 9)]
inp, out = make_test([(grid, queries)])
write_test(5, inp, out)

# ------ TC 06: Single column ------
print("TC 06: Single column")
grid = ["a", "a", "a", "b", "b", "a", "a"]
queries = [(1, 0), (3, 0), (0, 0), (6, 0)]
inp, out = make_test([(grid, queries)])
write_test(6, inp, out)

# ------ TC 07: 2x2 all same ------
print("TC 07: 2x2 all same")
grid = ["aa", "aa"]
queries = [(0, 0), (0, 1), (1, 0), (1, 1)]
inp, out = make_test([(grid, queries)])
write_test(7, inp, out)

# ------ TC 08: 3x3 all same ------
print("TC 08: 3x3 all same")
grid = ["bbb", "bbb", "bbb"]
queries = [(1, 1), (0, 0), (0, 2), (2, 0)]
inp, out = make_test([(grid, queries)])
write_test(8, inp, out)

# ------ TC 09: Large uniform grid 100x100 ------
print("TC 09: Large uniform 100x100")
grid = uniform_grid(100, 100, 'x')
queries = [(50, 50), (0, 0), (99, 99), (49, 49), (10, 10)]
inp, out = make_test([(grid, queries)])
write_test(9, inp, out)

# ------ TC 10: Large random grid 100x100, multiple queries ------
print("TC 10: Large random 100x100")
grid = random_grid(100, 100, "abc")
queries = [(random.randint(0, 99), random.randint(0, 99)) for _ in range(20)]
inp, out = make_test([(grid, queries)])
write_test(10, inp, out)

# ------ TC 11: Block patterns ------
print("TC 11: Block pattern grid 50x50")
grid = block_grid(50, 50)
queries = [(random.randint(0, 49), random.randint(0, 49)) for _ in range(15)]
inp, out = make_test([(grid, queries)])
write_test(11, inp, out)

# ------ TC 12: Multiple test cases in one input ------
print("TC 12: Multiple test cases (T=3)")
tc1_grid = ["aaa", "aaa", "aaa"]
tc1_q = [(1, 1)]
tc2_grid = ["ab", "ba"]
tc2_q = [(0, 0), (1, 1)]
tc3_grid = ["xxxxx", "xyyyx", "xyxyx", "xyyyx", "xxxxx"]
tc3_q = [(2, 2), (1, 1), (0, 0), (1, 2)]
inp, out = make_test([(tc1_grid, tc1_q), (tc2_grid, tc2_q), (tc3_grid, tc3_q)])
write_test(12, inp, out)

# ------ TC 13: Edge queries (corners and edges of large grid) ------
print("TC 13: Edge queries on 20x20")
grid = uniform_grid(20, 20, 'q')
queries = [(0, 0), (0, 19), (19, 0), (19, 19), (0, 10), (10, 0), (19, 10), (10, 19)]
inp, out = make_test([(grid, queries)])
write_test(13, inp, out)

# ------ TC 14: Grid with a big square block in center ------
print("TC 14: Big block in center")
M, N = 21, 21
grid = [['a'] * N for _ in range(M)]
# Place a 11x11 block of 'b' centered at (10,10)
for i in range(5, 16):
    for j in range(5, 16):
        grid[i][j] = 'b'
grid = ["".join(row) for row in grid]
queries = [(10, 10), (5, 5), (15, 15), (4, 4), (10, 5), (0, 0), (10, 15)]
inp, out = make_test([(grid, queries)])
write_test(14, inp, out)

# ------ TC 15: Concentric squares ------
print("TC 15: Concentric squares")
M, N = 15, 15
grid = [['a'] * N for _ in range(M)]
# Ring of 'b' at distance 1-2 from center (7,7)
for i in range(5, 10):
    for j in range(5, 10):
        grid[i][j] = 'b'
# Center back to 'a'
grid[7][7] = 'a'
grid = ["".join(row) for row in grid]
queries = [(7, 7), (5, 5), (6, 6), (0, 0), (14, 14)]
inp, out = make_test([(grid, queries)])
write_test(15, inp, out)

# ------ TC 16: Multiple T with varied sizes ------
print("TC 16: Multiple T=5 varied sizes")
cases = []
# 1x1
cases.append((["m"], [(0, 0)]))
# 1x10
cases.append((["aaaaaaaaaa"], [(0, 5)]))
# 10x1
cases.append(([c for c in "bbbbbbbbbb"], [(5, 0)]))
# 4x4 random
g = random_grid(4, 4, "pq")
cases.append((g, [(1, 1), (2, 2)]))
# 8x8 random
g = random_grid(8, 8, "xyz")
cases.append((g, [(3, 3), (4, 4), (0, 7)]))
inp, out = make_test(cases)
write_test(16, inp, out)

# ------ TC 17: Maximum T=20, small grids ------
print("TC 17: T=20 small grids")
cases = []
for _ in range(20):
    m = random.randint(1, 10)
    n = random.randint(1, 10)
    g = random_grid(m, n, "abcd")
    q_count = random.randint(1, 5)
    qs = [(random.randint(0, m - 1), random.randint(0, n - 1)) for _ in range(q_count)]
    cases.append((g, qs))
inp, out = make_test(cases)
write_test(17, inp, out)

# ------ TC 18: Stress test - max dimensions, max queries ------
print("TC 18: Stress 100x100, Q=20")
grid = random_grid(100, 100, "ab")
queries = [(random.randint(0, 99), random.randint(0, 99)) for _ in range(20)]
inp, out = make_test([(grid, queries)])
write_test(18, inp, out)

# ------ TC 19: Grid where answer at center is large ------
print("TC 19: Large answer at center")
M, N = 99, 99
grid = uniform_grid(M, N, 'z')
queries = [(49, 49), (0, 0), (98, 98), (25, 25), (49, 0)]
inp, out = make_test([(grid, queries)])
write_test(19, inp, out)

# ------ TC 20: Near-uniform grid with one different char ------
print("TC 20: Near-uniform with one defect")
M, N = 50, 50
grid = [['a'] * N for _ in range(M)]
grid[25][25] = 'b'  # single defect
grid = ["".join(row) for row in grid]
queries = [(25, 25), (24, 24), (25, 24), (0, 0), (49, 49), (25, 26)]
inp, out = make_test([(grid, queries)])
write_test(20, inp, out)

print("\nAll test cases generated successfully!")
