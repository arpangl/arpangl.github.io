#!/usr/bin/env python3
"""
Generate test cases for 22171 - Dungeon Master (3D BFS shortest path).
Produces 18 test cases covering various scenarios.
Each test case file contains one or more dungeons followed by "0 0 0".
"""

import os
import random
from collections import deque

OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/22171/testcases"

# ─── BFS Solver ───────────────────────────────────────────────────────────────

def solve_dungeon(L, R, C, grid):
    """
    grid[l][r] is a string of length C.
    Returns the shortest distance from S to E, or -1 if impossible.
    """
    sl = sr = sc = el = er = ec = -1
    for l in range(L):
        for r in range(R):
            for c in range(C):
                if grid[l][r][c] == 'S':
                    sl, sr, sc = l, r, c
                elif grid[l][r][c] == 'E':
                    el, er, ec = l, r, c

    if sl == -1 or el == -1:
        return -1

    # S == E edge case
    if sl == el and sr == er and sc == ec:
        return 0

    dist = [[[-1]*C for _ in range(R)] for _ in range(L)]
    dist[sl][sr][sc] = 0
    q = deque([(sl, sr, sc)])
    dirs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    while q:
        ll, rr, cc = q.popleft()
        for dl, dr, dc in dirs:
            nl, nr, nc = ll+dl, rr+dr, cc+dc
            if 0 <= nl < L and 0 <= nr < R and 0 <= nc < C:
                if grid[nl][nr][nc] != '#' and dist[nl][nr][nc] == -1:
                    dist[nl][nr][nc] = dist[ll][rr][cc] + 1
                    if nl == el and nr == er and nc == ec:
                        return dist[nl][nr][nc]
                    q.append((nl, nr, nc))
    return -1


def solve_input(text):
    """Parse full input text (possibly multiple dungeons) and return output text."""
    lines = text.strip().split('\n')
    idx = 0
    results = []

    while idx < len(lines):
        # skip blank lines
        while idx < len(lines) and lines[idx].strip() == '':
            idx += 1
        if idx >= len(lines):
            break

        parts = lines[idx].strip().split()
        L, R, C = int(parts[0]), int(parts[1]), int(parts[2])
        idx += 1

        if L == 0 and R == 0 and C == 0:
            break

        grid = []
        for l in range(L):
            # skip blank lines between levels
            while idx < len(lines) and lines[idx].strip() == '':
                idx += 1
            level = []
            for r in range(R):
                level.append(lines[idx].strip())
                idx += 1
            grid.append(level)

        d = solve_dungeon(L, R, C, grid)
        if d >= 0:
            results.append(f"Escaped in {d} minute(s).")
        else:
            results.append("Trapped!")

    return '\n'.join(results) + '\n'


def dungeon_to_text(L, R, C, grid):
    """Convert a single dungeon to input text (without the terminating 0 0 0)."""
    lines = [f"{L} {R} {C}"]
    for l in range(L):
        for r in range(R):
            lines.append(grid[l][r])
        lines.append("")  # blank line after each level
    return '\n'.join(lines)


def make_grid(L, R, C, fill='.'):
    return [[fill * C for _ in range(R)] for _ in range(L)]


def set_cell(grid, l, r, c, ch):
    row = list(grid[l][r])
    row[c] = ch
    grid[l][r] = ''.join(row)


def random_dungeon(L, R, C, rock_prob=0.3, seed=None):
    """Generate a random dungeon with given rock probability."""
    if seed is not None:
        random.seed(seed)
    grid = []
    for l in range(L):
        level = []
        for r in range(R):
            row = ''
            for c in range(C):
                row += '#' if random.random() < rock_prob else '.'
            level.append(row)
        grid.append(level)

    # Place S and E on random open cells (or force them open)
    sl, sr, sc = random.randint(0, L-1), random.randint(0, R-1), random.randint(0, C-1)
    set_cell(grid, sl, sr, sc, 'S')

    while True:
        el, er, ec = random.randint(0, L-1), random.randint(0, R-1), random.randint(0, C-1)
        if (el, er, ec) != (sl, sr, sc):
            break
    set_cell(grid, el, er, ec, 'E')
    return grid


# ─── Test Case Definitions ────────────────────────────────────────────────────

test_cases = []  # list of input strings (each ends with "0 0 0\n")


# TC 01: Sample from problem statement
tc01 = """3 4 5
S....
.###.
.##..
###.#

#####
#####
##.##
##...

#####
#####
#.###
####E

1 3 3
S##
#E#
###

0 0 0
"""
test_cases.append(tc01)


# TC 02: Single cell with S=E (well, S and E can't be same char, so 1x1x1 with S adjacent to E is smallest;
# Actually re-reading: S and E are separate. Minimum: 1 1 2 -> S next to E)
tc02 = """1 1 2
SE

0 0 0
"""
test_cases.append(tc02)


# TC 03: S and E adjacent vertically (2 layers)
tc03 = """2 1 1
S

E

0 0 0
"""
test_cases.append(tc03)


# TC 04: No path - completely blocked
tc04 = """1 3 3
S#.
###
.#E

0 0 0
"""
test_cases.append(tc04)


# TC 05: Single layer open grid, S top-left, E bottom-right
tc05 = """1 5 5
S....
.....
.....
.....
....E

0 0 0
"""
test_cases.append(tc05)


# TC 06: Winding path in single layer (snake maze)
tc06_grid = make_grid(1, 7, 7, '#')
# Create a winding path
path = []
for r in range(7):
    if r % 2 == 0:
        for c in range(7):
            path.append((0, r, c))
    else:
        for c in range(6, -1, -1):
            path.append((0, r, c))
for (l, r, c) in path:
    set_cell(tc06_grid, l, r, c, '.')
set_cell(tc06_grid, 0, 0, 0, 'S')
set_cell(tc06_grid, 0, 6, 6, 'E')
tc06 = dungeon_to_text(1, 7, 7, tc06_grid) + "0 0 0\n"
test_cases.append(tc06)


# TC 07: Multiple layers with vertical-only path
tc07_grid = make_grid(5, 1, 1, '.')
set_cell(tc07_grid, 0, 0, 0, 'S')
set_cell(tc07_grid, 4, 0, 0, 'E')
tc07 = dungeon_to_text(5, 1, 1, tc07_grid) + "0 0 0\n"
test_cases.append(tc07)


# TC 08: Trapped - E fully surrounded by rocks in 3D (all 6 neighbors are #)
tc08 = """3 3 3
...
.S.
...

.#.
###
.#.

.#.
#E#
.#.

0 0 0
"""
test_cases.append(tc08)


# TC 09: Large fully open dungeon (30x30x30) - max distance
tc09_L, tc09_R, tc09_C = 30, 30, 30
tc09_grid = make_grid(tc09_L, tc09_R, tc09_C, '.')
set_cell(tc09_grid, 0, 0, 0, 'S')
set_cell(tc09_grid, 29, 29, 29, 'E')
tc09 = dungeon_to_text(tc09_L, tc09_R, tc09_C, tc09_grid) + "0 0 0\n"
test_cases.append(tc09)


# TC 10: Large dungeon with moderate rocks (30x30x30, 30% rock)
tc10_grid = random_dungeon(30, 30, 30, rock_prob=0.30, seed=42)
tc10 = dungeon_to_text(30, 30, 30, tc10_grid) + "0 0 0\n"
test_cases.append(tc10)


# TC 11: Large dungeon with heavy rocks (30x30x30, 50% rock) - likely trapped
tc11_grid = random_dungeon(30, 30, 30, rock_prob=0.50, seed=123)
tc11 = dungeon_to_text(30, 30, 30, tc11_grid) + "0 0 0\n"
test_cases.append(tc11)


# TC 12: Long winding 3D path - spiral going up through layers
tc12_L, tc12_R, tc12_C = 10, 10, 10
tc12_grid = make_grid(tc12_L, tc12_R, tc12_C, '#')
# Create a spiral-like path going up
# Each layer: go along one edge, then up
for l in range(10):
    if l % 4 == 0:
        for c in range(10):
            set_cell(tc12_grid, l, 0, c, '.')
        if l + 1 < 10:
            set_cell(tc12_grid, l, 0, 9, '.')  # connection point
    elif l % 4 == 1:
        for r in range(10):
            set_cell(tc12_grid, l, r, 9, '.')
        if l + 1 < 10:
            set_cell(tc12_grid, l, 9, 9, '.')
    elif l % 4 == 2:
        for c in range(10):
            set_cell(tc12_grid, l, 9, c, '.')
        if l + 1 < 10:
            set_cell(tc12_grid, l, 9, 0, '.')
    elif l % 4 == 3:
        for r in range(10):
            set_cell(tc12_grid, l, r, 0, '.')
        if l + 1 < 10:
            set_cell(tc12_grid, l, 0, 0, '.')
# Connect layers vertically at transition points
for l in range(9):
    if l % 4 == 0:
        set_cell(tc12_grid, l+1, 0, 9, '.')
    elif l % 4 == 1:
        set_cell(tc12_grid, l+1, 9, 9, '.')
    elif l % 4 == 2:
        set_cell(tc12_grid, l+1, 9, 0, '.')
    elif l % 4 == 3:
        set_cell(tc12_grid, l+1, 0, 0, '.')

set_cell(tc12_grid, 0, 0, 0, 'S')
set_cell(tc12_grid, 9, 0, 0, 'E')
tc12 = dungeon_to_text(tc12_L, tc12_R, tc12_C, tc12_grid) + "0 0 0\n"
test_cases.append(tc12)


# TC 13: Multiple dungeons in one input (3 small ones)
tc13 = """1 1 2
SE

2 2 2
S.
..

..
.E

1 3 3
S..
...
..E

0 0 0
"""
test_cases.append(tc13)


# TC 14: Dungeon where shortest path goes up then down
tc14 = """3 3 3
S#.
.#.
.#.

...
.#.
...

.#.
.#.
.#E

0 0 0
"""
test_cases.append(tc14)


# TC 15: One layer, large maze with guaranteed path (20x20)
random.seed(999)
tc15_R, tc15_C = 20, 20
tc15_grid = make_grid(1, tc15_R, tc15_C, '.')
# Add some rocks but leave a clear path along row 0 and column 19
for r in range(tc15_R):
    for c in range(tc15_C):
        if random.random() < 0.25 and (r, c) != (0, 0) and (r, c) != (19, 19):
            set_cell(tc15_grid, 0, r, c, '#')
# Guarantee a path: clear row 0 and column 19
for c in range(tc15_C):
    set_cell(tc15_grid, 0, 0, c, '.')
for r in range(tc15_R):
    set_cell(tc15_grid, 0, r, 19, '.')
set_cell(tc15_grid, 0, 0, 0, 'S')
set_cell(tc15_grid, 0, 19, 19, 'E')
tc15 = dungeon_to_text(1, tc15_R, tc15_C, tc15_grid) + "0 0 0\n"
test_cases.append(tc15)


# TC 16: Narrow corridor across multiple layers (1xCx1)
tc16 = """1 1 10
S........E

0 0 0
"""
test_cases.append(tc16)


# TC 17: Large dungeon with low rock density (should find path, 25x25x25)
tc17_grid = random_dungeon(25, 25, 25, rock_prob=0.20, seed=777)
tc17 = dungeon_to_text(25, 25, 25, tc17_grid) + "0 0 0\n"
test_cases.append(tc17)


# TC 18: E reachable only through a single narrow tunnel between layers
tc18 = """3 5 5
S....
.####
.####
.####
.....

#####
#####
##.##
#####
#####

#####
####.
####.
####.
####E

0 0 0
"""
test_cases.append(tc18)


# ─── Write Test Cases ─────────────────────────────────────────────────────────

os.makedirs(OUTDIR, exist_ok=True)

for i, tc_input in enumerate(test_cases, start=1):
    fname = f"{i:02d}"
    in_path = os.path.join(OUTDIR, f"{fname}.in")
    out_path = os.path.join(OUTDIR, f"{fname}.out")

    # Normalize: ensure input ends with newline
    tc_clean = tc_input.strip() + '\n'

    with open(in_path, 'w') as f:
        f.write(tc_clean)

    output = solve_input(tc_clean)

    with open(out_path, 'w') as f:
        f.write(output)

    print(f"TC {fname}: written  ->  {output.strip()}")

print(f"\nTotal: {len(test_cases)} test cases generated in {OUTDIR}")
