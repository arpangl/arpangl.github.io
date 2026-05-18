#!/usr/bin/env python3
"""
Generate test cases for 22821 - Oil Deposits.

Problem: count connected components of '@' in a grid, 8-connected.
Input: multiple grids, each starts with "m n", then m lines of n chars (* or @).
       Terminated by "0 0".
Output: one integer per grid (number of oil deposits).
"""

import os
import random
from collections import deque

OUTPUT_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/22821/testcases"

# ─── BFS solver ───────────────────────────────────────────────────────────────

def solve_grid(grid, m, n):
    """Count connected components of '@' using BFS (8-connected)."""
    visited = [[False] * n for _ in range(m)]
    count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '@' and not visited[i][j]:
                count += 1
                queue = deque()
                queue.append((i, j))
                visited[i][j] = True
                while queue:
                    ci, cj = queue.popleft()
                    for di, dj in directions:
                        ni, nj = ci + di, cj + dj
                        if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj] and grid[ni][nj] == '@':
                            visited[ni][nj] = True
                            queue.append((ni, nj))
    return count


def solve_input(text):
    """Parse full input (may contain multiple grids) and return list of answers."""
    lines = text.strip().split('\n')
    idx = 0
    answers = []
    while idx < len(lines):
        parts = lines[idx].split()
        m, n = int(parts[0]), int(parts[1])
        idx += 1
        if m == 0:
            break
        grid = []
        for _ in range(m):
            grid.append(lines[idx].strip())
            idx += 1
        answers.append(solve_grid(grid, m, n))
    return answers


# ─── Grid generators ─────────────────────────────────────────────────────────

def make_grid(m, n, fill='*'):
    return [[fill] * n for _ in range(m)]


def grid_to_strings(grid):
    return [''.join(row) for row in grid]


def random_grid(m, n, prob=0.3):
    """Random grid where each cell is '@' with probability prob."""
    grid = []
    for _ in range(m):
        row = []
        for _ in range(n):
            row.append('@' if random.random() < prob else '*')
        grid.append(row)
    return grid


# ─── Test case definitions ────────────────────────────────────────────────────

def gen_test_cases():
    """Return list of (description, list_of_grids).
    Each grid is (m, n, list_of_row_strings).
    """
    cases = []

    # 01: Sample from problem statement
    grids = []
    grids.append((1, 1, ['*']))
    grids.append((3, 5, ['*@*@*', '**@**', '*@*@*']))
    grids.append((1, 8, ['@@****@*']))
    grids.append((5, 5, ['****@', '*@@*@', '*@**@', '@@@*@', '@@**@']))
    cases.append(("sample", grids))

    # 02: Empty grids of various sizes
    grids = []
    grids.append((1, 1, ['*']))
    grids.append((5, 5, ['*****'] * 5))
    grids.append((10, 10, ['*' * 10] * 10))
    cases.append(("all_empty", grids))

    # 03: Single '@' cell
    grids = []
    grids.append((1, 1, ['@']))
    grids.append((3, 3, ['***', '*@*', '***']))
    cases.append(("single_cell", grids))

    # 04: Entire grid is '@'
    grids = []
    grids.append((1, 1, ['@']))
    grids.append((3, 3, ['@@@', '@@@', '@@@']))
    grids.append((5, 5, ['@' * 5] * 5))
    cases.append(("full_grid", grids))

    # 05: Diagonal chain — should be ONE deposit (8-connected)
    g = make_grid(5, 5)
    for i in range(5):
        g[i][i] = '@'
    grids = [(5, 5, grid_to_strings(g))]
    cases.append(("diagonal_chain", grids))

    # 06: Anti-diagonal chain
    g = make_grid(5, 5)
    for i in range(5):
        g[i][4 - i] = '@'
    grids = [(5, 5, grid_to_strings(g))]
    cases.append(("anti_diagonal", grids))

    # 07: Checkerboard pattern (every other cell) — all connected diagonally = 1 deposit
    m, n = 6, 6
    g = make_grid(m, n)
    for i in range(m):
        for j in range(n):
            if (i + j) % 2 == 0:
                g[i][j] = '@'
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("checkerboard_6x6", grids))

    # 08: Isolated single cells (no two adjacent even diagonally)
    m, n = 7, 7
    g = make_grid(m, n)
    # Place '@' at every 3rd row and 3rd col
    for i in range(0, m, 3):
        for j in range(0, n, 3):
            g[i][j] = '@'
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("isolated_cells", grids))

    # 09: Horizontal and vertical lines as separate deposits
    m, n = 10, 10
    g = make_grid(m, n)
    # Horizontal line at row 1
    for j in range(n):
        g[1][j] = '@'
    # Horizontal line at row 5
    for j in range(n):
        g[5][j] = '@'
    # Horizontal line at row 9
    for j in range(n):
        g[9][j] = '@'
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("horizontal_lines", grids))

    # 10: L-shapes and T-shapes
    m, n = 10, 10
    g = make_grid(m, n)
    # L-shape top-left
    for i in range(4):
        g[i][0] = '@'
    for j in range(3):
        g[3][j] = '@'
    # T-shape bottom-right
    for j in range(6, 10):
        g[6][j] = '@'
    g[7][8] = '@'
    g[8][8] = '@'
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("l_and_t_shapes", grids))

    # 11: Ring / hollow square
    m, n = 7, 7
    g = make_grid(m, n)
    for j in range(n):
        g[0][j] = '@'
        g[m - 1][j] = '@'
    for i in range(m):
        g[i][0] = '@'
        g[i][n - 1] = '@'
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("ring", grids))

    # 12: Multiple small grids in one input
    grids = []
    grids.append((2, 2, ['@@', '@@']))
    grids.append((2, 2, ['@*', '*@']))
    grids.append((2, 2, ['*@', '@*']))
    grids.append((2, 2, ['@*', '**']))
    grids.append((2, 2, ['**', '**']))
    cases.append(("small_2x2_grids", grids))

    # 13: Large sparse grid (100x100, ~5% oil)
    random.seed(42)
    m, n = 100, 100
    g = random_grid(m, n, prob=0.05)
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("large_sparse_100x100", grids))

    # 14: Large dense grid (100x100, ~40% oil)
    random.seed(123)
    m, n = 100, 100
    g = random_grid(m, n, prob=0.40)
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("large_dense_100x100", grids))

    # 15: Large medium grid (100x100, ~15% oil)
    random.seed(999)
    m, n = 100, 100
    g = random_grid(m, n, prob=0.15)
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("large_medium_100x100", grids))

    # 16: Single row
    grids = []
    grids.append((1, 100, ['@*' * 50]))
    grids.append((1, 50, ['@' * 50]))
    cases.append(("single_row", grids))

    # 17: Single column
    col = []
    for i in range(100):
        col.append('@' if i % 4 == 0 else '*')
    grids = [(100, 1, col)]
    cases.append(("single_column", grids))

    # 18: Spiral pattern
    m, n = 11, 11
    g = make_grid(m, n)
    # Draw a spiral manually
    # outer ring
    for j in range(n):
        g[0][j] = '@'
    for i in range(1, m):
        g[i][n - 1] = '@'
    for j in range(n - 2, -1, -1):
        g[m - 1][j] = '@'
    for i in range(m - 2, 0, -1):
        g[i][0] = '@'
    # second ring
    for j in range(2, n - 2):
        g[2][j] = '@'
    for i in range(3, m - 2):
        g[i][n - 3] = '@'
    for j in range(n - 4, 1, -1):
        g[m - 3][j] = '@'
    for i in range(m - 4, 2, -1):
        g[i][2] = '@'
    # third ring center
    for j in range(4, n - 4):
        g[4][j] = '@'
    for i in range(5, m - 4):
        g[i][n - 5] = '@'
    for j in range(n - 6, 3, -1):
        g[m - 5][j] = '@'
    for i in range(m - 6, 4, -1):
        g[i][4] = '@'
    # center dot
    g[5][5] = '@'
    grids = [(m, n, grid_to_strings(g))]
    cases.append(("spiral", grids))

    return cases


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cases = gen_test_cases()

    print(f"Generating {len(cases)} test cases...\n")

    for idx, (desc, grids) in enumerate(cases, start=1):
        # Build input text
        lines = []
        for m, n, rows in grids:
            lines.append(f"{m} {n}")
            for row in rows:
                lines.append(row)
        lines.append("0 0")
        input_text = '\n'.join(lines) + '\n'

        # Solve
        answers = solve_input(input_text)
        output_text = '\n'.join(str(a) for a in answers) + '\n'

        # Write files
        prefix = f"{idx:02d}"
        in_path = os.path.join(OUTPUT_DIR, f"{prefix}.in")
        out_path = os.path.join(OUTPUT_DIR, f"{prefix}.out")

        with open(in_path, 'w') as f:
            f.write(input_text)
        with open(out_path, 'w') as f:
            f.write(output_text)

        # Summary
        grid_summaries = []
        ai = 0
        for m, n, rows in grids:
            grid_summaries.append(f"{m}x{n}->ans={answers[ai]}")
            ai += 1
        print(f"  {prefix} [{desc}]: {', '.join(grid_summaries)}")

    # ── Verification pass ────────────────────────────────────────────────────
    print("\n--- Verification ---")
    all_ok = True
    for idx in range(1, len(cases) + 1):
        prefix = f"{idx:02d}"
        in_path = os.path.join(OUTPUT_DIR, f"{prefix}.in")
        out_path = os.path.join(OUTPUT_DIR, f"{prefix}.out")

        with open(in_path) as f:
            input_text = f.read()
        with open(out_path) as f:
            expected = f.read().strip()

        answers = solve_input(input_text)
        computed = '\n'.join(str(a) for a in answers)

        if computed == expected:
            print(f"  {prefix}: OK")
        else:
            print(f"  {prefix}: MISMATCH!")
            print(f"    expected: {expected}")
            print(f"    computed: {computed}")
            all_ok = False

    if all_ok:
        print("\nAll test cases verified successfully.")
    else:
        print("\nSOME TEST CASES FAILED!")

    # ── Verify sample from problem statement ─────────────────────────────────
    print("\n--- Sample verification ---")
    sample_input = """1 1
*
3 5
*@*@*
**@**
*@*@*
1 8
@@****@*
5 5
****@
*@@*@
*@**@
@@@*@
@@**@
0 0
"""
    sample_expected = [0, 1, 2, 2]
    sample_computed = solve_input(sample_input)
    if sample_computed == sample_expected:
        print("  Sample matches expected output: PASS")
    else:
        print(f"  Sample MISMATCH: expected {sample_expected}, got {sample_computed}")


if __name__ == '__main__':
    main()
