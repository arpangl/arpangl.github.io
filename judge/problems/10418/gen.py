#!/usr/bin/env python3
"""
Minesweeper test case generator and solver.

Problem: Given a grid with mines (*) and safe squares (.), replace each '.'
with the count of adjacent mines (8-directional). Multiple fields per input,
terminated by "0 0". Output "Field #x:" header, blank line between fields.
"""

import random
import os

OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10418/testcases"


def solve(fields):
    """Given a list of (n, m, grid) tuples, produce the full output string."""
    results = []
    for idx, (n, m, grid) in enumerate(fields):
        block = [f"Field #{idx + 1}:"]
        for r in range(n):
            row = []
            for c in range(m):
                if grid[r][c] == '*':
                    row.append('*')
                else:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == '*':
                                count += 1
                    row.append(str(count))
            block.append(''.join(row))
        results.append('\n'.join(block))
    return '\n\n'.join(results) + '\n'


def make_input(fields):
    """Given a list of (n, m, grid) tuples, produce the full input string."""
    lines = []
    for n, m, grid in fields:
        lines.append(f"{n} {m}")
        for row in grid:
            lines.append(row)
    lines.append("0 0")
    return '\n'.join(lines) + '\n'


def random_grid(n, m, mine_prob=0.3):
    grid = []
    for _ in range(n):
        row = ''.join('*' if random.random() < mine_prob else '.' for _ in range(m))
        grid.append(row)
    return grid


def all_mines_grid(n, m):
    return ['*' * m for _ in range(n)]


def no_mines_grid(n, m):
    return ['.' * m for _ in range(n)]


def single_mine_grid(n, m, r, c):
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append('*' if i == r and j == c else '.')
        grid.append(''.join(row))
    return grid


def checkerboard_grid(n, m):
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append('*' if (i + j) % 2 == 0 else '.')
        grid.append(''.join(row))
    return grid


def border_mines_grid(n, m):
    """Mines only on the border."""
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            if i == 0 or i == n - 1 or j == 0 or j == m - 1:
                row.append('*')
            else:
                row.append('.')
        grid.append(''.join(row))
    return grid


def diagonal_mines_grid(n, m):
    """Mines on the main diagonal."""
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append('*' if i == j else '.')
        grid.append(''.join(row))
    return grid


def corner_mines_grid(n, m):
    """Mines only in the 4 corners."""
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            if (i, j) in [(0, 0), (0, m-1), (n-1, 0), (n-1, m-1)]:
                row.append('*')
            else:
                row.append('.')
        grid.append(''.join(row))
    return grid


# ---- Define test cases ----
# Each test case is a list of fields (each input file can have multiple fields).

test_cases = []

# TC 01: Sample from problem statement
test_cases.append([
    (4, 4, ["*...", "....", ".*..", "...."]),
    (3, 5, ["**...", ".....", ".*..."]),
])

# TC 02: 1x1 grid with mine
test_cases.append([
    (1, 1, ["*"]),
])

# TC 03: 1x1 grid without mine
test_cases.append([
    (1, 1, ["."]),
])

# TC 04: All mines (small)
test_cases.append([
    (3, 3, all_mines_grid(3, 3)),
])

# TC 05: No mines (small)
test_cases.append([
    (3, 3, no_mines_grid(3, 3)),
])

# TC 06: Single mine in center of 3x3
test_cases.append([
    (3, 3, single_mine_grid(3, 3, 1, 1)),
])

# TC 07: Single mine in corner (0,0) of 4x4
test_cases.append([
    (4, 4, single_mine_grid(4, 4, 0, 0)),
])

# TC 08: Single mine on edge (0,2) of 4x5
test_cases.append([
    (4, 5, single_mine_grid(4, 5, 0, 2)),
])

# TC 09: Mines in all 4 corners of 5x5
test_cases.append([
    (5, 5, corner_mines_grid(5, 5)),
])

# TC 10: Checkerboard pattern 5x5
test_cases.append([
    (5, 5, checkerboard_grid(5, 5)),
])

# TC 11: Border mines 5x5
test_cases.append([
    (5, 5, border_mines_grid(5, 5)),
])

# TC 12: Diagonal mines 5x5
test_cases.append([
    (5, 5, diagonal_mines_grid(5, 5)),
])

# TC 13: 1xM row grid (1x10, random)
random.seed(42)
test_cases.append([
    (1, 10, random_grid(1, 10, 0.4)),
])

# TC 14: Nx1 column grid (10x1, random)
random.seed(43)
test_cases.append([
    (10, 1, random_grid(10, 1, 0.4)),
])

# TC 15: Multiple fields in one input (3 small fields)
test_cases.append([
    (2, 2, ["*.", ".*"]),
    (2, 2, ["..", ".."]),
    (2, 2, ["**", "**"]),
])

# TC 16: Medium random grid 10x10
random.seed(44)
test_cases.append([
    (10, 10, random_grid(10, 10, 0.25)),
])

# TC 17: Large grid 100x100 with sparse mines
random.seed(45)
test_cases.append([
    (100, 100, random_grid(100, 100, 0.05)),
])

# TC 18: Large grid 100x100 with dense mines
random.seed(46)
test_cases.append([
    (100, 100, random_grid(100, 100, 0.7)),
])

# TC 19: Large grid 100x100 all mines
test_cases.append([
    (100, 100, all_mines_grid(100, 100)),
])

# TC 20: Large grid 100x100 no mines
test_cases.append([
    (100, 100, no_mines_grid(100, 100)),
])


# ---- Generate and verify ----
for i, fields in enumerate(test_cases):
    tc_num = f"{i + 1:02d}"
    inp = make_input(fields)
    out = solve(fields)

    # Verify: parse input back and re-solve to check consistency
    lines = inp.strip().split('\n')
    idx = 0
    parsed_fields = []
    while idx < len(lines):
        parts = lines[idx].split()
        n, m = int(parts[0]), int(parts[1])
        idx += 1
        if n == 0 and m == 0:
            break
        grid = []
        for _ in range(n):
            grid.append(lines[idx])
            idx += 1
        parsed_fields.append((n, m, grid))

    out2 = solve(parsed_fields)
    assert out == out2, f"TC {tc_num}: re-solve mismatch!"

    # Additional checks
    out_lines = out.strip().split('\n')
    field_idx = 0
    ol = 0
    for fn, (n, m, grid) in enumerate(fields):
        header = out_lines[ol]
        assert header == f"Field #{fn + 1}:", f"TC {tc_num} field {fn+1}: bad header '{header}'"
        ol += 1
        for r in range(n):
            row = out_lines[ol]
            assert len(row) == m, f"TC {tc_num} field {fn+1} row {r}: len {len(row)} != {m}"
            for c in range(m):
                if grid[r][c] == '*':
                    assert row[c] == '*', f"TC {tc_num}: mine not preserved at ({r},{c})"
                else:
                    assert row[c].isdigit(), f"TC {tc_num}: non-digit at ({r},{c}): '{row[c]}'"
                    val = int(row[c])
                    assert 0 <= val <= 8, f"TC {tc_num}: invalid count {val} at ({r},{c})"
            ol += 1
        if fn < len(fields) - 1:
            assert out_lines[ol] == '', f"TC {tc_num}: missing blank line between fields"
            ol += 1

    # Write files
    in_path = os.path.join(OUTDIR, f"{tc_num}.in")
    out_path = os.path.join(OUTDIR, f"{tc_num}.out")
    with open(in_path, 'w') as f:
        f.write(inp)
    with open(out_path, 'w') as f:
        f.write(out)

    print(f"TC {tc_num}: OK ({len(fields)} field(s))")

print(f"\nAll {len(test_cases)} test cases generated and verified!")
