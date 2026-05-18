import random
import os

OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10601/testcases"

cases = []

# Case 01: Sample input
cases.append("""2
5 4
S...
.#.#
.#..
.##.
...E
6 6
.S...E
.#.##.
.#....
.#.##.
.####.
......""")

# Case 02: Minimal grid 2x2, S and E adjacent but need 1-step move
cases.append("""1
2 2
SE
..""")

# Case 03: 2x2 all open, S top-left E bottom-right
cases.append("""1
2 2
S.
.E""")

# Case 04: 2x2 blocked
cases.append("""1
2 2
S#
#E""")

# Case 05: S == E adjacent in 1-step, straight line
cases.append("""1
1 7
S....E.""")

# Case 06: Long corridor, 1xN
cases.append("""1
1 20
S..................E""")

# Case 07: Tall corridor, Nx1
cases.append("""1
20 1
S
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
E""")

# Case 08: Open grid 6x6, S top-left E bottom-right
cases.append("""1
6 6
S.....
......
......
......
......
.....E""")

# Case 09: Maze with no solution (E completely walled off)
cases.append("""1
5 5
S....
.....
..##.
..#E#
..###""")

# Case 10: Single row, S and E distance exactly 6 (1+2+3)
cases.append("""1
1 8
S......E""")

# Case 11: Grid where shortest BFS path exists but cycle constraint makes it longer
cases.append("""1
7 7
S......
.#####.
.......
.#####.
.......
.#####.
......E""")

# Case 12: Grid with multiple test cases, some solvable some not
cases.append("""3
3 3
S.E
...
...
3 3
S.#
.#.
#.E
4 4
S...
....
....
...E""")

# Case 13: Large open grid 10x10
cases.append("""1
10 10
S.........
..........
..........
..........
..........
..........
..........
..........
..........
.........E""")

# Case 14: Spiral-like maze
cases.append("""1
7 7
S.....#
#####.#
......#
.####.#
.#..#.#
.#....#
.######
""".strip() + "\n" + "")  # E not placed, fix below

# Fix case 14 - proper spiral with S and E
cases[13] = """1
7 7
S.....#
#####.#
......#
.####.#
.#.E#.#
.#....#
.######"""

# Case 15: S and E same row, walls blocking direct path, must go around
cases.append("""1
5 8
S..#...E
...#....
...#....
...#....
........""")

# Case 16: Large grid with narrow passages (stress cycle constraint)
rows = 10
cols = 10
grid = [['.' for _ in range(cols)] for _ in range(rows)]
grid[0][0] = 'S'
grid[rows-1][cols-1] = 'E'
# Add walls creating a zigzag path
for r in range(rows):
    for c in range(cols):
        if (r + c) % 3 == 1 and grid[r][c] == '.':
            if random.random() < 0.3:
                grid[r][c] = '#'
# Ensure S and E are not overwritten
grid[0][0] = 'S'
grid[rows-1][cols-1] = 'E'
random.seed(42)
grid_str = '\n'.join(''.join(row) for row in grid)
cases.append(f"1\n{rows} {cols}\n{grid_str}")

# Case 17: Medium random grid 15x15
random.seed(123)
R, C = 15, 15
grid = [['.' for _ in range(C)] for _ in range(R)]
grid[0][0] = 'S'
grid[R-1][C-1] = 'E'
for r in range(R):
    for c in range(C):
        if grid[r][c] == '.' and random.random() < 0.2:
            grid[r][c] = '#'
grid[0][0] = 'S'
grid[R-1][C-1] = 'E'
grid_str = '\n'.join(''.join(row) for row in grid)
cases.append(f"1\n{R} {C}\n{grid_str}")

# Case 18: Large grid 50x50 with moderate walls
random.seed(456)
R, C = 50, 50
grid = [['.' for _ in range(C)] for _ in range(R)]
grid[0][0] = 'S'
grid[R-1][C-1] = 'E'
for r in range(R):
    for c in range(C):
        if grid[r][c] == '.' and random.random() < 0.25:
            grid[r][c] = '#'
grid[0][0] = 'S'
grid[R-1][C-1] = 'E'
grid_str = '\n'.join(''.join(row) for row in grid)
cases.append(f"1\n{R} {C}\n{grid_str}")

# Case 19: Large grid 100x100 sparse walls
random.seed(789)
R, C = 100, 100
grid = [['.' for _ in range(C)] for _ in range(R)]
grid[0][0] = 'S'
grid[R-1][C-1] = 'E'
for r in range(R):
    for c in range(C):
        if grid[r][c] == '.' and random.random() < 0.15:
            grid[r][c] = '#'
grid[0][0] = 'S'
grid[R-1][C-1] = 'E'
grid_str = '\n'.join(''.join(row) for row in grid)
cases.append(f"1\n{R} {C}\n{grid_str}")

# Case 20: Stress test - 300x300 open grid (tests performance)
R, C = 300, 300
grid_lines = []
for r in range(R):
    row = '.' * C
    if r == 0:
        row = 'S' + row[1:]
    if r == R - 1:
        row = row[:-1] + 'E'
    grid_lines.append(row)
grid_str = '\n'.join(grid_lines)
cases.append(f"1\n{R} {C}\n{grid_str}")

# Write all cases
for i, case in enumerate(cases):
    idx = f"{i+1:02d}"
    path = os.path.join(OUTDIR, f"{idx}.in")
    # Clean up: strip trailing whitespace from each line, ensure single trailing newline
    lines = case.strip().split('\n')
    cleaned = '\n'.join(line.rstrip() for line in lines) + '\n'
    with open(path, 'w') as f:
        f.write(cleaned)
    print(f"Written {idx}.in")

print(f"Total: {len(cases)} test cases generated")
