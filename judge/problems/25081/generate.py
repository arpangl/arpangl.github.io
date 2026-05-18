#!/usr/bin/env python3
"""
BFS solver and test case generator for Problem 25081: Solving Maze Problems.

10x10 maze. S=start, G=goal, #=wall, .=open.
Mark solution path with '+'. S and G both become '+'.
If no path: "No solution".
Output ends with an empty line.
Each maze has exactly one solution path (unique shortest path).
"""

import os
from collections import deque


def solve_maze(grid):
    """
    Solve a 10x10 maze using BFS. Returns the grid with path marked '+',
    or None if no solution.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start = None
    goal = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'G':
                goal = (r, c)

    if start is None or goal is None:
        return None

    # BFS
    visited = [[False]*cols for _ in range(rows)]
    parent = [[None]*cols for _ in range(rows)]
    queue = deque([start])
    visited[start[0]][start[1]] = True

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # E, W, S, N

    found = False
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            found = True
            break
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                if grid[nr][nc] != '#':
                    visited[nr][nc] = True
                    parent[nr][nc] = (r, c)
                    queue.append((nr, nc))

    if not found:
        return None

    # Trace path
    result = [list(row) for row in grid]
    cur = goal
    while cur is not None:
        r, c = cur
        result[r][c] = '+'
        cur = parent[r][c]

    return [''.join(row) for row in result]


def count_shortest_paths(grid_str, start, end):
    """Count number of distinct shortest paths using BFS."""
    R = len(grid_str)
    C = len(grid_str[0])

    dist = [[-1]*C for _ in range(R)]
    count = [[0]*C for _ in range(R)]

    queue = deque([start])
    dist[start[0]][start[1]] = 0
    count[start[0]][start[1]] = 1

    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and grid_str[nr][nc] != '#':
                if dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    count[nr][nc] = count[r][c]
                    queue.append((nr, nc))
                elif dist[nr][nc] == dist[r][c] + 1:
                    count[nr][nc] += count[r][c]

    return count[end[0]][end[1]]


def validate_and_write(name, maze_str, base_dir, expected_solvable=None):
    """Validate a test case and write .in/.out files."""
    grid = maze_str.strip().split('\n')
    assert len(grid) == 10, f"TC {name}: expected 10 rows, got {len(grid)}"
    for i, row in enumerate(grid):
        assert len(row) == 10, f"TC {name} row {i}: expected 10 cols, got {len(row)} in '{row}'"

    # Find S and G
    s_pos = g_pos = None
    for r in range(10):
        for c in range(10):
            if grid[r][c] == 'S': s_pos = (r,c)
            if grid[r][c] == 'G': g_pos = (r,c)
    assert s_pos is not None, f"TC {name}: no S found"
    assert g_pos is not None, f"TC {name}: no G found"

    # Check only valid chars
    for r in range(10):
        for c in range(10):
            assert grid[r][c] in 'SG#.', f"TC {name}: invalid char '{grid[r][c]}' at ({r},{c})"

    result = solve_maze(grid)

    if result is not None:
        cnt = count_shortest_paths(grid, s_pos, g_pos)
        if cnt != 1:
            print(f"  FAIL: TC {name} has {cnt} shortest paths!")
            return False
        if expected_solvable is False:
            print(f"  FAIL: TC {name} expected no solution but found one!")
            return False
        print(f"  TC {name}: OK (solvable, unique path, S={s_pos}, G={g_pos})")
    else:
        if expected_solvable is True:
            print(f"  FAIL: TC {name} expected solution but found none!")
            return False
        print(f"  TC {name}: OK (no solution, S={s_pos}, G={g_pos})")

    # Write files
    in_path = os.path.join(base_dir, f"{name}.in")
    out_path = os.path.join(base_dir, f"{name}.out")

    with open(in_path, 'w') as f:
        f.write(maze_str.strip() + '\n')

    if result is None:
        with open(out_path, 'w') as f:
            f.write("No solution\n")
    else:
        with open(out_path, 'w') as f:
            f.write('\n'.join(result) + '\n')

    return True


def main():
    base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/25081/testcases"
    os.makedirs(base_dir, exist_ok=True)

    print("Generating and validating test cases...\n")
    all_ok = True

    # TC 01: Sample from the problem statement
    all_ok &= validate_and_write("01", """\
S..#######
##.......#
#####.####
#####.####
.#........
#####.####
#####.....
.#....####
###.#.....
#########G""", base_dir, expected_solvable=True)

    # TC 02: No solution - G completely walled off
    all_ok &= validate_and_write("02", """\
S.........
..........
..........
..........
....###...
....#G#...
....###...
..........
..........
..........""", base_dir, expected_solvable=False)

    # TC 03: S and G adjacent horizontally (minimal path)
    all_ok &= validate_and_write("03", """\
SG########
##########
##########
##########
##########
##########
##########
##########
##########
##########""", base_dir, expected_solvable=True)

    # TC 04: S top-left, G bottom-right, L-shaped corridor
    all_ok &= validate_and_write("04", """\
S.########
#.########
#.########
#.########
#.########
#.########
#.########
#.########
#.########
#........G""", base_dir, expected_solvable=True)

    # TC 05: S bottom-right, G top-left, zigzag corridor (fixed connectivity)
    all_ok &= validate_and_write("05", """\
G.........
#########.
..........
.#########
..........
#########.
..........
.#########
..........
.########S""", base_dir, expected_solvable=True)

    # TC 06: S and G on same row, straight horizontal path
    all_ok &= validate_and_write("06", """\
##########
##########
##########
##########
S........G
##########
##########
##########
##########
##########""", base_dir, expected_solvable=True)

    # TC 07: S and G on same column, straight vertical path
    all_ok &= validate_and_write("07", """\
####S#####
####.#####
####.#####
####.#####
####.#####
####.#####
####.#####
####.#####
####.#####
####G#####""", base_dir, expected_solvable=True)

    # TC 08: Spiral-like maze with unique path (single-width corridors)
    all_ok &= validate_and_write("08", """\
S#########
.#########
.#########
.........#
########.#
########.#
########.#
#........#
#.########
#........G""", base_dir, expected_solvable=True)

    # TC 09: No solution - S completely walled off
    all_ok &= validate_and_write("09", """\
#S########
##########
##########
##########
##########
##########
##########
##########
##########
########G.""", base_dir, expected_solvable=False)

    # TC 10: Winding path through center (verified unique)
    all_ok &= validate_and_write("10", """\
S.########
#.########
#.........
########.#
########.#
########.#
#........#
#.########
#........G
##########""", base_dir, expected_solvable=True)

    # TC 11: Narrow single-cell corridor bottleneck
    all_ok &= validate_and_write("11", """\
S.........
#########.
#########.
#########.
#########.
#########.
#########.
#########.
#########.
.........G""", base_dir, expected_solvable=True)

    # TC 12: S in center area, G at bottom-right corner
    all_ok &= validate_and_write("12", """\
..........
.########.
.#......#.
.#.####.#.
.#.#S#..#.
.#.#.##.#.
.#.#....#.
.#.######.
.#........
.########G""", base_dir, expected_solvable=True)

    # TC 13: S at top-left, G in center area
    all_ok &= validate_and_write("13", """\
S#........
.#.######.
.#.#....#.
.#.#.##.#.
.#.#.G#.#.
.#.#..#.#.
.#.####.#.
.#......#.
.########.
..........""", base_dir, expected_solvable=True)

    # TC 14: No solution - wall bisects the grid completely
    all_ok &= validate_and_write("14", """\
S.....####
......####
......####
......####
##########
####......
####......
####......
####.....G
####......""", base_dir, expected_solvable=False)

    # TC 15: Zigzag path going down-right
    all_ok &= validate_and_write("15", """\
S#########
.#########
.#########
.........#
########.#
########.#
#........#
#.########
#.########
#........G""", base_dir, expected_solvable=True)

    # TC 16: S bottom-left, G top-right, zigzag
    all_ok &= validate_and_write("16", """\
#########G
#########.
..........
.#########
..........
#########.
..........
.#########
..........
S#########""", base_dir, expected_solvable=True)

    # TC 17: S and G adjacent vertically
    all_ok &= validate_and_write("17", """\
##########
##########
##########
##########
####S#####
####G#####
##########
##########
##########
##########""", base_dir, expected_solvable=True)

    # TC 18: No solution - S and G both isolated in different quadrants
    all_ok &= validate_and_write("18", """\
##########
#S########
##########
##########
##########
##########
##########
##########
########G#
##########""", base_dir, expected_solvable=False)

    # TC 19: Long serpentine path filling most of the grid
    all_ok &= validate_and_write("19", """\
S........#
########.#
.........#
.#########
.........#
########.#
.........#
.#########
.........#
########.G""", base_dir, expected_solvable=True)

    # TC 20: No solution - large open areas but a wall separates them
    all_ok &= validate_and_write("20", """\
S.........
..........
..........
..........
..........
##########
..........
..........
..........
.........G""", base_dir, expected_solvable=False)

    print()
    if all_ok:
        print("All test cases validated successfully!")
    else:
        print("Some test cases FAILED validation!")
    print(f"Generated test cases in {base_dir}")


if __name__ == '__main__':
    main()
