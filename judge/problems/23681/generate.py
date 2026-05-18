#!/usr/bin/env python3
"""
Generate test cases for Bachet's Game (Problem 23681).

Test case design:
 01: Sample input (verbatim)
 02: Single stone, single move {1}
 03: n=1 with multiple moves
 04: Classic Nim: moves={1,2,3} (k+1 pattern)
 05: Only move is 1 (parity game)
 06: Moves={1,2} small n
 07: Large n with moves={1,2} (parity-like mod 3)
 08: Moves with gaps, e.g. {1,4}
 09: Moves={1,5} medium n
 10: Larger move set, medium n
 11: Large n, large move set (max m=10)
 12: n=1000000, moves={1}
 13: n=999999, moves={1}
 14: Stress: multiple large-n lines
 15: Moves={1,2,3,4,5,6,7,8,9,10} (max m, sequential)
 16: Moves={1,6} interesting cycle
 17: n=2, moves={1} minimal game
 18: Large n, moves={1,3,5,7,9} (odd moves only)
"""

import random
import os

# We'll define each test case as a list of lines, each line = "n m s1 s2 ... sm"
test_cases = []

# 01: Sample
test_cases.append([
    "20 3 1 3 8",
    "21 3 1 3 8",
    "22 3 1 3 8",
    "23 3 1 3 8",
    "1000000 10 1 23 38 11 7 5 4 8 3 13",
    "999996 10 1 23 38 11 7 5 4 8 3 13",
])

# 02: Single stone, single move
test_cases.append([
    "1 1 1",
])

# 03: n=1 with multiple moves (Stan always wins: take the 1 stone)
test_cases.append([
    "1 3 1 5 10",
    "1 5 1 2 3 4 5",
])

# 04: Classic Nim: moves={1,2,3}. Winner determined by n mod 4 != 0
test_cases.append([
    "1 3 1 2 3",
    "2 3 1 2 3",
    "3 3 1 2 3",
    "4 3 1 2 3",
    "5 3 1 2 3",
    "12 3 1 2 3",
    "13 3 1 2 3",
    "100 3 1 2 3",
])

# 05: Only move is 1 (parity: odd n -> Stan wins, even n -> Ollie wins)
test_cases.append([
    "1 1 1",
    "2 1 1",
    "3 1 1",
    "4 1 1",
    "5 1 1",
    "100 1 1",
    "101 1 1",
    "999999 1 1",
    "1000000 1 1",
])

# 06: Moves={1,2}, small n (mod 3: 0->Ollie, else Stan)
test_cases.append([
    "1 2 1 2",
    "2 2 1 2",
    "3 2 1 2",
    "4 2 1 2",
    "5 2 1 2",
    "6 2 1 2",
    "7 2 1 2",
    "9 2 1 2",
    "10 2 1 2",
])

# 07: Large n with moves={1,2}
test_cases.append([
    "999999 2 1 2",
    "1000000 2 1 2",
    "999998 2 1 2",
    "500000 2 1 2",
    "500001 2 1 2",
    "500002 2 1 2",
])

# 08: Moves={1,4}, interesting cycle
test_cases.append([
    "1 2 1 4",
    "2 2 1 4",
    "3 2 1 4",
    "4 2 1 4",
    "5 2 1 4",
    "6 2 1 4",
    "7 2 1 4",
    "8 2 1 4",
    "9 2 1 4",
    "10 2 1 4",
    "100 2 1 4",
    "1000 2 1 4",
])

# 09: Moves={1,5}, medium n
test_cases.append([
    "10 2 1 5",
    "11 2 1 5",
    "12 2 1 5",
    "50 2 1 5",
    "100 2 1 5",
    "1000 2 1 5",
    "10000 2 1 5",
])

# 10: Larger move set, medium n
test_cases.append([
    "50 5 1 3 5 7 9",
    "100 5 1 3 5 7 9",
    "200 5 1 3 5 7 9",
    "500 5 1 3 5 7 9",
    "1000 5 1 3 5 7 9",
])

# 11: Large n, max move set (m=10)
test_cases.append([
    "1000000 10 1 2 3 4 5 6 7 8 9 10",
    "999999 10 1 2 3 4 5 6 7 8 9 10",
    "999990 10 1 2 3 4 5 6 7 8 9 10",
    "500000 10 1 2 3 4 5 6 7 8 9 10",
])

# 12: n=1000000, moves={1} (even -> Ollie)
test_cases.append([
    "1000000 1 1",
])

# 13: n=999999, moves={1} (odd -> Stan)
test_cases.append([
    "999999 1 1",
])

# 14: Stress: multiple large-n lines with varied move sets
random.seed(42)
lines_14 = []
for _ in range(6):
    n = random.randint(500000, 1000000)
    m = random.randint(2, 10)
    moves = [1]  # always include 1
    while len(moves) < m:
        s = random.randint(2, 100)
        if s not in moves:
            moves.append(s)
    moves.sort()
    line = f"{n} {m} {' '.join(map(str, moves))}"
    lines_14.append(line)
test_cases.append(lines_14)

# 15: Moves={1,2,...,10}, sequential, various n
test_cases.append([
    "1 10 1 2 3 4 5 6 7 8 9 10",
    "10 10 1 2 3 4 5 6 7 8 9 10",
    "11 10 1 2 3 4 5 6 7 8 9 10",
    "22 10 1 2 3 4 5 6 7 8 9 10",
    "100 10 1 2 3 4 5 6 7 8 9 10",
])

# 16: Moves={1,6}, interesting cycle
test_cases.append([
    "1 2 1 6",
    "6 2 1 6",
    "7 2 1 6",
    "8 2 1 6",
    "13 2 1 6",
    "14 2 1 6",
    "100 2 1 6",
    "1000 2 1 6",
    "100000 2 1 6",
])

# 17: n=2, moves={1}
test_cases.append([
    "2 1 1",
    "3 1 1",
    "2 2 1 2",
    "2 3 1 2 3",
])

# 18: Large n, odd moves only {1,3,5,7,9}
test_cases.append([
    "1000000 5 1 3 5 7 9",
    "999999 5 1 3 5 7 9",
    "999998 5 1 3 5 7 9",
    "123456 5 1 3 5 7 9",
    "654321 5 1 3 5 7 9",
])

# Now write them out
outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/23681/testcases"

for i, lines in enumerate(test_cases, start=1):
    fname = f"{i:02d}"
    in_path = os.path.join(outdir, f"{fname}.in")
    with open(in_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')

print(f"Generated {len(test_cases)} test input files.")
