import math
import os
import json

def solve_case(n):
    if n == 0:
        return "0.000000 0"

    prob_none = 1.0
    log_all = 0.0

    for k in range(n):
        pk = 1.0 / ((k + 1) * (k + 2))
        prob_none *= (1.0 - pk)
        log_all += math.log10(pk)

    prob_at_least_one = 1.0 - prob_none
    zeros = int(-math.floor(log_all)) - 1
    if zeros < 0:
        zeros = 0

    return f"{prob_at_least_one:.6f} {zeros}"

# Test cases: each input file can have multiple lines
test_cases = [
    # Case 1: Sample
    [1, 2, 20],
    # Case 2: Single 0
    [0],
    # Case 3: Small values
    [1],
    # Case 4: Small values 2
    [2, 3, 4, 5],
    # Case 5: Medium
    [10, 50, 100],
    # Case 6: Larger
    [500, 1000],
    # Case 7: Powers of 10
    [1, 10, 100, 1000, 10000],
    # Case 8: Large
    [100000],
    # Case 9: Various medium
    [7, 15, 30, 77, 200],
    # Case 10: Edge near max
    [999999],
    # Case 11: Sequential small
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    # Case 12: Large values
    [50000, 100000, 500000],
    # Case 13: Specific tricky values
    [3, 13, 42, 99],
    # Case 14: Mix
    [1, 999999],
    # Case 15: Medium batch
    [25, 75, 150, 300, 600, 1200],
]

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10675/testcases'
os.makedirs(TESTDIR, exist_ok=True)

for i, cases in enumerate(test_cases):
    inp = '\n'.join(str(c) for c in cases) + '\n'
    out_lines = []
    for c in cases:
        out_lines.append(solve_case(c))
    out = '\n'.join(out_lines) + '\n'

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    print(f"Case {i+1:02d}: OK ({len(cases)} subcases)")

problem = {
    "pid": "10675",
    "name": "Urn-ball Probabilities!",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

print("All test cases generated!")
