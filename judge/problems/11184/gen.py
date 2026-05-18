import os
import json
import random

def isqrt(n):
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def solve_case(n):
    s = isqrt(n)
    return s * s

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/11184/testcases'
os.makedirs(TESTDIR, exist_ok=True)

test_cases = [
    # Case 1: Sample
    [1, 90],
    # Case 2: Small values
    [1, 2, 3, 4],
    # Case 3: Perfect squares
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
    # Case 4: Just above perfect square
    [2, 5, 10, 17, 26],
    # Case 5: Just below perfect square
    [3, 8, 15, 24, 35],
    # Case 6: Large N
    [1000000000],
    # Case 7: Very large N (50 digits)
    [10**50],
    # Case 8: Very large N (100 digits)
    [10**100],
    # Case 9: Large perfect square
    [10**50 * 10**50],  # = 10^100, which is a perfect square
    # Case 10: N=1
    [1],
    # Case 11: Random medium values
    [12345, 67890, 999999],
    # Case 12: Large values near perfect squares
    [10**100 - 1],
    # Case 13: Various big numbers
    [10**20, 10**40, 10**60, 10**80],
    # Case 14: Random big numbers
    [int('9' * 50), int('1' * 100)],
    # Case 15: Edge cases
    [2, 10**100, 999999999999999999999999999999999999999999999999999],
]

for i, cases in enumerate(test_cases):
    inp_lines = [str(c) for c in cases] + ['0']
    inp = '\n'.join(inp_lines) + '\n'

    out_lines = [str(solve_case(c)) for c in cases]
    out = '\n'.join(out_lines) + '\n'

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    print(f"Case {i+1:02d}: OK ({len(cases)} subcases)")

problem = {
    "pid": "11184",
    "name": "Opening Doors",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

print("All test cases generated!")
