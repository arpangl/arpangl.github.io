#!/usr/bin/env python3
"""
Generate test cases for Homer Simpson (11174).

Constraints: 0 < m, n, t < 10000
Each test case is one line: m n t
Multiple test cases per file (EOF terminated).

We generate 18 test files, each containing several lines of test cases.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from solve import solve, format_output

TESTCASE_DIR = os.path.join(os.path.dirname(__file__), "testcases")

test_cases_per_file = [
    # 01: Sample cases
    [
        (3, 5, 54),
        (3, 5, 55),
    ],
    # 02: T exactly divisible by m only
    [
        (4, 7, 16),   # 16/4=4 burgers, 0 remain
        (6, 5, 18),   # 18/6=3, but 18/5=3 r3; try combos: 3*6=18 -> 3 burgers; 0*6+3*5=15 r3; 1*6+2*5=16 r2; 2*6+1*5=17 r1 => best no-waste is 3 burgers
        (10, 3, 30),  # 30/10=3 or 30/3=10 -> 10 burgers
    ],
    # 03: T exactly divisible by n only
    [
        (7, 4, 16),   # 16/4=4 burgers
        (7, 3, 9),    # 9/3=3 burgers
        (11, 5, 25),  # 25/5=5 burgers
    ],
    # 04: T exactly divisible by both m and n
    [
        (3, 5, 15),   # 15/3=5 burgers (better than 15/5=3)
        (6, 10, 30),  # 30/6=5, 30/10=3; combos: 5*6=30->5; 0*6+3*10=30->3; best=5
        (2, 3, 6),    # 6/2=3 burgers
    ],
    # 05: T not divisible by either (must drink beer)
    [
        (3, 5, 4),    # can't make 4: 1*3=3 r1, 0*5 r4 -> best is 1 burger, 1 remain
        (7, 11, 5),   # can't eat any: 0 burgers, 5 remain
        (4, 6, 5),    # 1*4=4 r1 -> 1 burger, 1 remain
        (3, 5, 1),    # 0 burgers, 1 remain
    ],
    # 06: m = n (same burger time)
    [
        (5, 5, 25),   # 25/5=5 burgers
        (5, 5, 27),   # 5*5=25 r2 -> 5 burgers, 2 remain
        (3, 3, 9),    # 9/3=3 burgers
        (3, 3, 10),   # 3*3=9 r1 -> 3 burgers, 1 remain
    ],
    # 07: m = 1 (can always fill exactly)
    [
        (1, 5, 100),  # 100/1=100, but 20*5=100->20; best? 100 burgers with m=1
        (1, 7, 9999), # 9999 burgers
        (1, 1, 50),   # 50 burgers
    ],
    # 08: n = 1 (can always fill exactly)
    [
        (5, 1, 100),  # 100 burgers
        (7, 1, 9999), # 9999 burgers
        (99, 1, 100), # 100 burgers (all type n)
    ],
    # 09: Large T, small m and n
    [
        (2, 3, 9999), # large
        (3, 5, 9998),
        (2, 5, 9997),
    ],
    # 10: Large T, large m and n
    [
        (9999, 9998, 9999), # 1 burger type m
        (5000, 4999, 9999), # 1*5000+1*4999=9999 -> 2 burgers
        (9998, 9999, 9999), # 1 burger type n
    ],
    # 11: T < m and T < n (impossible, must drink beer for all time... but with 0 burgers)
    [
        (5, 7, 3),    # 0 burgers, 3 remain
        (100, 200, 50), # 0 burgers, 50 remain
        (9999, 9998, 1), # 0 burgers, 1 remain
    ],
    # 12: Edge cases with small values
    [
        (1, 2, 1),    # 1 burger
        (2, 1, 1),    # 1 burger
        (1, 1, 1),    # 1 burger
        (2, 3, 1),    # 0 burgers, 1 remain
        (1, 9999, 9999), # 9999 burgers
    ],
    # 13: Cases where greedy fails (need to check combinations)
    [
        (3, 5, 11),   # 2*3+1*5=11 -> 3 burgers
        (3, 7, 13),   # 2*3+1*7=13 -> 3 burgers
        (4, 6, 10),   # 1*4+1*6=10 -> 2 burgers
        (7, 11, 29),  # 1*7+2*11=29 -> 3 burgers
    ],
    # 14: Coprime m, n with various T
    [
        (7, 11, 100), # need to find best combo
        (13, 17, 500),
        (3, 7, 41),   # 41 = some combo
        (9, 4, 37),   # 37 = 1*9+7*4=37 -> 8 burgers
    ],
    # 15: Large number of burgers
    [
        (1, 2, 9999),  # 9999 burgers
        (2, 3, 9999),  # need combo: 9999=3*3+4998*1? no: a*2+b*3=9999
        (1, 3, 8000),  # 8000 burgers
    ],
    # 16: T is prime, m and n don't divide it
    [
        (4, 6, 97),   # 97: 4a+6b. best with min waste
        (6, 10, 97),  # 97: 6a+10b
        (8, 12, 97),  # 97: 8a+12b (both even, odd T -> always remainder)
    ],
    # 17: Stress test - many test cases in one file
    [
        (2, 3, 100),
        (3, 4, 100),
        (4, 5, 100),
        (5, 6, 100),
        (6, 7, 100),
        (7, 8, 100),
        (8, 9, 100),
        (9, 10, 100),
        (10, 11, 100),
        (11, 12, 100),
    ],
    # 18: More edge/tricky cases
    [
        (2, 4, 7),    # 2a+4b=7? 3*2+0*4=6 r1; 1*2+1*4=6 r1; best=3 burgers r1
        (9999, 9998, 9997), # 0 burgers, 9997 remain
        (3, 5, 3),    # 1 burger
        (5, 3, 3),    # 1 burger (type n)
        (100, 1, 9999), # 9999 burgers (all type n=1)
    ],
]

def main():
    os.makedirs(TESTCASE_DIR, exist_ok=True)

    for i, cases in enumerate(test_cases_per_file, start=1):
        filename_in = os.path.join(TESTCASE_DIR, f"{i:02d}.in")
        filename_out = os.path.join(TESTCASE_DIR, f"{i:02d}.out")

        input_lines = []
        output_lines = []

        for (m, n, t) in cases:
            # Validate constraints
            assert 0 < m < 10000, f"m={m} out of range"
            assert 0 < n < 10000, f"n={n} out of range"
            assert 0 < t < 10000, f"t={t} out of range"

            input_lines.append(f"{m} {n} {t}")
            burgers, remain = solve(m, n, t)
            output_lines.append(format_output(burgers, remain))

        with open(filename_in, "w") as f:
            f.write("\n".join(input_lines) + "\n")

        with open(filename_out, "w") as f:
            f.write("\n".join(output_lines) + "\n")

        print(f"Generated {filename_in} and {filename_out} ({len(cases)} cases)")

    print(f"\nTotal: {len(test_cases_per_file)} test files generated.")

if __name__ == "__main__":
    main()
