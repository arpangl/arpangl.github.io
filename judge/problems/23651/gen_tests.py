#!/usr/bin/env python3
"""
Generate test cases for problem 23651 - The jackpot (Maximum Subarray Sum).

Constraints:
- N <= 10000 (positive integer, 0 terminates)
- Each bet: integer, |bet| in (0, 1000) exclusive => bet in [-999, -1] or [1, 999]
  (greater than 0 and less than 1000 in absolute value)

Edge cases to cover:
1. Sample test case
2. Single positive element
3. Single negative element
4. All positive elements
5. All negative elements
6. Mix: positive at start, negative at end
7. Mix: negative at start, positive at end
8. Alternating positive/negative
9. Large single positive then many small negatives
10. Many small positives then one large negative
11. Multiple test cases in one input
12. N=1 positive
13. N=1 negative
14. N=10000 all positive (max N)
15. N=10000 all negative (max N)
16. N=10000 mixed random
17. Maximum subarray in the middle
18. Two equal-max subarrays
19. All same value positive
20. Alternating: big positive, small negative
"""

import random
import os

random.seed(42)

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/23651/testcases"

def solve_case(bets):
    """Kadane's algorithm: return max subarray sum, or 0 if all negative."""
    max_ending_here = 0
    max_so_far = 0
    for b in bets:
        max_ending_here = max(0, max_ending_here + b)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

def format_output(result):
    if result > 0:
        return f"The maximum winning streak is {result}."
    else:
        return "Losing streak."

def rand_bet():
    """Random bet: integer in [-999, -1] or [1, 999]."""
    v = random.randint(1, 999)
    if random.random() < 0.5:
        v = -v
    return v

def rand_positive():
    return random.randint(1, 999)

def rand_negative():
    return -random.randint(1, 999)

test_cases = []

# TC 01: Sample test case (multiple cases in one input)
tc01_cases = [
    [12, -4, -10, 4, 9],
    [-2, -1, -2],
]
test_cases.append(("01", tc01_cases))

# TC 02: Single positive element
test_cases.append(("02", [[500]]))

# TC 03: Single negative element
test_cases.append(("03", [[-300]]))

# TC 04: All positive (small N)
tc04 = [random.randint(1, 999) for _ in range(10)]
test_cases.append(("04", [tc04]))

# TC 05: All negative (small N)
tc05 = [-random.randint(1, 999) for _ in range(10)]
test_cases.append(("05", [tc05]))

# TC 06: Positive at start, negative at end
tc06 = [rand_positive() for _ in range(5)] + [rand_negative() for _ in range(5)]
test_cases.append(("06", [tc06]))

# TC 07: Negative at start, positive at end
tc07 = [rand_negative() for _ in range(5)] + [rand_positive() for _ in range(5)]
test_cases.append(("07", [tc07]))

# TC 08: Alternating positive/negative
tc08 = []
for i in range(20):
    if i % 2 == 0:
        tc08.append(rand_positive())
    else:
        tc08.append(rand_negative())
test_cases.append(("08", [tc08]))

# TC 09: Large positive then many small negatives
tc09 = [999] + [-1 for _ in range(50)]
test_cases.append(("09", [tc09]))

# TC 10: Many small positives then one large negative
tc10 = [1 for _ in range(50)] + [-999]
test_cases.append(("10", [tc10]))

# TC 11: Multiple test cases in one input (5 random cases)
tc11_cases = []
for _ in range(5):
    n = random.randint(1, 100)
    bets = [rand_bet() for _ in range(n)]
    tc11_cases.append(bets)
test_cases.append(("11", tc11_cases))

# TC 12: N=1 with positive value (boundary)
test_cases.append(("12", [[1]]))

# TC 13: N=1 with negative value (boundary)
test_cases.append(("13", [[-1]]))

# TC 14: N=10000, all positive (max N, large sum)
tc14 = [rand_positive() for _ in range(10000)]
test_cases.append(("14", [tc14]))

# TC 15: N=10000, all negative (max N, losing streak)
tc15 = [rand_negative() for _ in range(10000)]
test_cases.append(("15", [tc15]))

# TC 16: N=10000, mixed random
tc16 = [rand_bet() for _ in range(10000)]
test_cases.append(("16", [tc16]))

# TC 17: Maximum subarray in the middle
tc17 = [rand_negative() for _ in range(20)] + [rand_positive() for _ in range(20)] + [rand_negative() for _ in range(20)]
test_cases.append(("17", [tc17]))

# TC 18: Two potential max subarrays (test that global max is found)
# [big positive segment] [very negative] [big positive segment]
tc18 = [100]*10 + [-999] + [99]*10
test_cases.append(("18", [tc18]))

# TC 19: All same positive value
tc19 = [7] * 100
test_cases.append(("19", [tc19]))

# TC 20: Alternating big positive, small negative (answer = sum of all)
tc20 = []
for i in range(50):
    tc20.append(500)
    tc20.append(-1)
test_cases.append(("20", [tc20]))

# Now write all test cases
for tc_id, cases in test_cases:
    in_lines = []
    out_lines = []
    for bets in cases:
        n = len(bets)
        in_lines.append(str(n))
        in_lines.append(" ".join(map(str, bets)))
        result = solve_case(bets)
        out_lines.append(format_output(result))
    in_lines.append("0")

    in_path = os.path.join(TESTCASE_DIR, f"{tc_id}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{tc_id}.out")

    with open(in_path, "w") as f:
        f.write("\n".join(in_lines) + "\n")
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")

print(f"Generated {len(test_cases)} test cases.")
