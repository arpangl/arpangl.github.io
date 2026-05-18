import random
import os
import subprocess
import sys

SOLUTION_PATH = "/Users/lambert/Documents/GPE-Helper/judge/problems/10633/solution.py"
TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10633/testcases"

def make_grid_str(M, N, grid):
    lines = []
    for row in grid:
        lines.append(' '.join(map(str, row)))
    return lines

def build_test_case(cases):
    """Build a full input string from a list of (M, N, grid) tuples."""
    lines = []
    for M, N, grid in cases:
        lines.append(f"{M} {N}")
        lines.extend(make_grid_str(M, N, grid))
    lines.append("0 0")
    return '\n'.join(lines)

def all_zeros(M, N):
    return [[0]*N for _ in range(M)]

def all_ones(M, N):
    return [[1]*N for _ in range(M)]

def random_grid(M, N, prob_tree=0.3):
    return [[1 if random.random() < prob_tree else 0 for _ in range(N)] for _ in range(M)]

def checkerboard(M, N):
    return [[(i+j) % 2 for j in range(N)] for i in range(M)]

def single_zero_at(M, N, r, c):
    grid = all_ones(M, N)
    grid[r][c] = 0
    return grid

def border_ones_inside_zeros(M, N):
    grid = []
    for i in range(M):
        row = []
        for j in range(N):
            if i == 0 or i == M-1 or j == 0 or j == N-1:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)
    return grid

def diagonal_ones(M, N):
    grid = all_zeros(M, N)
    for i in range(min(M, N)):
        grid[i][i] = 1
    return grid

def column_stripe(M, N):
    """Alternating columns of 0 and 1."""
    return [[j % 2 for j in range(N)] for _ in range(M)]

def row_stripe(M, N):
    """Alternating rows of 0 and 1."""
    return [[i % 2]*N for i in range(M)]

def sparse_trees(M, N, count):
    grid = all_zeros(M, N)
    positions = random.sample(range(M*N), min(count, M*N))
    for p in positions:
        grid[p // N][p % N] = 1
    return grid

def cross_pattern(M, N):
    """Trees along the middle row and middle column."""
    grid = all_zeros(M, N)
    mr, mc = M // 2, N // 2
    for j in range(N):
        grid[mr][j] = 1
    for i in range(M):
        grid[i][mc] = 1
    return grid

def get_answer(input_str):
    result = subprocess.run(
        [sys.executable, SOLUTION_PATH],
        input=input_str, capture_output=True, text=True
    )
    return result.stdout.strip()

def write_test(idx, input_str, output_str):
    in_path = os.path.join(TESTCASE_DIR, f"{idx:02d}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{idx:02d}.out")
    with open(in_path, 'w') as f:
        f.write(input_str + '\n')
    with open(out_path, 'w') as f:
        f.write(output_str + '\n')

def main():
    random.seed(42)
    test_cases = []

    # TC 01: Sample test case
    tc01 = [(6, 7, [
        [0,1,1,0,1,1,0],
        [0,0,0,0,0,1,0],
        [1,0,0,0,0,0,1],
        [0,1,0,0,0,0,1],
        [1,1,0,0,0,1,0],
        [1,1,0,1,1,0,0],
    ])]
    test_cases.append(tc01)

    # TC 02: Minimum size - 1x1 with 0 (answer=1)
    test_cases.append([(1, 1, [[0]])])

    # TC 03: Minimum size - 1x1 with 1 (answer=0)
    test_cases.append([(1, 1, [[1]])])

    # TC 04: All zeros 5x5 (answer=25)
    test_cases.append([(5, 5, all_zeros(5, 5))])

    # TC 05: All ones 5x5 (answer=0)
    test_cases.append([(5, 5, all_ones(5, 5))])

    # TC 06: Single zero in a grid of ones
    test_cases.append([(4, 4, single_zero_at(4, 4, 2, 3))])

    # TC 07: Checkerboard pattern (answer should be 1)
    test_cases.append([(5, 5, checkerboard(5, 5))])

    # TC 08: Border ones, inside zeros
    test_cases.append([(6, 8, border_ones_inside_zeros(6, 8))])

    # TC 09: Diagonal ones (rest zeros)
    test_cases.append([(7, 7, diagonal_ones(7, 7))])

    # TC 10: Column stripes
    test_cases.append([(5, 6, column_stripe(5, 6))])

    # TC 11: Row stripes
    test_cases.append([(6, 5, row_stripe(6, 5))])

    # TC 12: Cross pattern
    test_cases.append([(7, 9, cross_pattern(7, 9))])

    # TC 13: 1xN all zeros (single row)
    test_cases.append([(1, 10, all_zeros(1, 10))])

    # TC 14: Mx1 all zeros (single column)
    test_cases.append([(10, 1, all_zeros(10, 1))])

    # TC 15: Sparse trees in large grid
    test_cases.append([(50, 50, sparse_trees(50, 50, 25))])

    # TC 16: Dense trees in large grid
    test_cases.append([(50, 50, random_grid(50, 50, 0.7))])

    # TC 17: Max size all zeros (100x100)
    test_cases.append([(100, 100, all_zeros(100, 100))])

    # TC 18: Max size random moderate density
    test_cases.append([(100, 100, random_grid(100, 100, 0.3))])

    # TC 19: Multiple test cases in one input
    tc19 = [
        (3, 3, all_zeros(3, 3)),
        (3, 3, all_ones(3, 3)),
        (2, 5, [[0,0,1,0,0],[0,0,1,0,0]]),
        (4, 4, checkerboard(4, 4)),
    ]
    test_cases.append(tc19)

    # TC 20: Rectangular (non-square) edge: wide and tall
    g20 = all_zeros(3, 100)
    # Place a few trees to split it
    g20[1][50] = 1
    test_cases.append([(3, 100, g20)])

    for idx, cases in enumerate(test_cases, 1):
        input_str = build_test_case(cases)
        output_str = get_answer(input_str)
        write_test(idx, input_str, output_str)
        # Quick sanity display
        answers = output_str.split('\n')
        print(f"TC {idx:02d}: {len(cases)} case(s), answers={answers}")

    print(f"\nGenerated {len(test_cases)} test cases in {TESTCASE_DIR}")

if __name__ == '__main__':
    main()
