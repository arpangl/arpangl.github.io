#!/usr/bin/env python3
"""
Independent verification solver for Problem 23551: Largest Square.
Uses a brute-force approach (different from the generator's incremental border check)
to cross-validate all test cases.
"""

import os
import sys

TCDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/23551/testcases"


def solve_bruteforce(grid, M, N, r, c):
    """Brute force: for each candidate side length, check ALL cells in the square."""
    ch = grid[r][c]
    max_k = min(r, c, M - 1 - r, N - 1 - c)
    best = 1
    for k in range(1, max_k + 1):
        side = 2 * k + 1
        all_same = True
        for i in range(r - k, r + k + 1):
            for j in range(c - k, c + k + 1):
                if grid[i][j] != ch:
                    all_same = False
                    break
            if not all_same:
                break
        if all_same:
            best = side
        else:
            break
    return best


def verify_file(idx):
    in_file = os.path.join(TCDIR, f"{idx:02d}.in")
    out_file = os.path.join(TCDIR, f"{idx:02d}.out")

    if not os.path.exists(in_file):
        return None

    with open(in_file) as f:
        lines = f.read().strip().split('\n')

    with open(out_file) as f:
        expected_lines = f.read().strip().split('\n')

    ptr = 0
    T = int(lines[ptr]); ptr += 1

    exp_ptr = 0
    errors = []

    for t in range(T):
        parts = lines[ptr].split(); ptr += 1
        M, N, Q = int(parts[0]), int(parts[1]), int(parts[2])

        grid = []
        for i in range(M):
            grid.append(lines[ptr]); ptr += 1

        queries = []
        for i in range(Q):
            r, c = map(int, lines[ptr].split()); ptr += 1
            queries.append((r, c))

        # Check header line
        exp_header = expected_lines[exp_ptr]; exp_ptr += 1
        expected_header = f"{M} {N} {Q}"
        if exp_header != expected_header:
            errors.append(f"  TC {t+1}: header mismatch: got '{exp_header}' expected '{expected_header}'")

        for qi, (r, c) in enumerate(queries):
            result = solve_bruteforce(grid, M, N, r, c)
            expected_val = int(expected_lines[exp_ptr]); exp_ptr += 1
            if result != expected_val:
                errors.append(f"  TC {t+1}, query ({r},{c}): brute_force={result}, file={expected_val}")

    return errors


all_ok = True
for idx in range(1, 30):
    result = verify_file(idx)
    if result is None:
        continue
    if len(result) == 0:
        print(f"  {idx:02d}: OK")
    else:
        all_ok = False
        print(f"  {idx:02d}: ERRORS")
        for e in result:
            print(e)

if all_ok:
    print("\nAll test cases verified successfully!")
else:
    print("\nSome test cases have errors!")
    sys.exit(1)
