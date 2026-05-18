#!/usr/bin/env python3
"""
Generate test cases for 10642 - Marbles.

Problem: Given n marbles and two box types (cost c1, capacity n1) and (cost c2, capacity n2),
find non-negative m1, m2 such that m1*n1 + m2*n2 = n, minimizing m1*c1 + m2*c2.
Input ends with n=0. Constraints: n up to 2e9, c1/c2/n1/n2 up to 2e9.
"""

import os

test_cases = []

# ---- Test 1: Sample test case ----
test_cases.append([
    (43, 1, 3, 2, 4),
    (40, 5, 9, 5, 12),
])

# ---- Test 2: n=1 with boxes of size 1, different costs ----
test_cases.append([
    (1, 3, 1, 5, 1),   # m1=1, m2=0 (type1 cheaper)
])

# ---- Test 3: n not divisible by gcd(n1,n2) -> failed ----
test_cases.append([
    (7, 3, 4, 5, 6),   # gcd(4,6)=2, 7%2!=0 -> failed
])

# ---- Test 4: Only box type 1 used ----
test_cases.append([
    (12, 1, 3, 100, 5),  # Using type1 is much cheaper; 12 = 4*3 + 0*5, cost=4
])

# ---- Test 5: Only box type 2 used ----
test_cases.append([
    (15, 100, 3, 1, 5),  # Using type2 is much cheaper; 15 = 0*3 + 3*5, cost=3
])

# ---- Test 6: Large n, coprime n1, n2 ----
test_cases.append([
    (2000000000, 3, 7, 5, 11),  # gcd=1, solution exists
])

# ---- Test 7: Large n, large n1/n2 values ----
test_cases.append([
    (1999999998, 100, 999999999, 200, 999999999),  # n = 2 * n1, so m1=2, m2=0
])

# ---- Test 8: n1 = n2, different costs (cheaper is type 1) ----
test_cases.append([
    (100, 3, 10, 5, 10),  # same capacity, pick cheaper one: m1=10, m2=0
])

# ---- Test 9: Large n, large coprime capacities, has solution ----
test_cases.append([
    (1999999866, 2, 999999937, 3, 999999929),  # m1=1, m2=1 is optimal
])

# ---- Test 10: gcd > 1, solution exists ----
test_cases.append([
    (60, 2, 6, 3, 10),  # gcd(6,10)=2, 60%2=0
])

# ---- Test 11: Very large values, failed case (odd n, even capacities) ----
test_cases.append([
    (1999999999, 1, 2, 1, 4),  # gcd(2,4)=2, 1999999999 is odd -> failed
])

# ---- Test 12: n = n1, trivial ----
test_cases.append([
    (7, 3, 7, 5, 11),  # m1=1, m2=0 costs 3
])

# ---- Test 13: n = n2, trivial ----
test_cases.append([
    (11, 5, 7, 3, 11),  # m1=0, m2=1 costs 3
])

# ---- Test 14: Large coprime, big costs ----
test_cases.append([
    (1000000000, 1999999999, 3, 1999999998, 7),
])

# ---- Test 15: n=1 with n1=1, n2=large ----
test_cases.append([
    (1, 5, 1, 1000000000, 1000000000),  # m1=1, m2=0
])

# ---- Test 16: Multiple test cases, mix of failed and success ----
test_cases.append([
    (24, 5, 6, 3, 8),   # gcd(6,8)=2, 24%2=0
    (25, 5, 6, 3, 8),   # 25%2!=0 -> failed
    (100, 3, 1, 7, 1),  # n1=n2=1, different costs, m1=100, m2=0
])

# ---- Test 17: n1=1, should always have solution ----
test_cases.append([
    (1999999937, 7, 1, 3, 1000000000),  # n1=1, so we can always solve
])

# ---- Test 18: Large with coprime capacities ----
test_cases.append([
    (1000000007, 10, 17, 20, 29),  # gcd(17,29)=1, solution exists
])

# ---- Test 19: Both capacities are 1, different costs ----
test_cases.append([
    (500000000, 3, 1, 7, 1),  # pick cheaper: all type1, m1=500000000, m2=0
])

# ---- Test 20: Edge - large n, large coprime capacities, no feasible solution ----
test_cases.append([
    (1999999999, 5, 999999937, 8, 999999929),  # gcd=1 but no non-neg solution
])

# Now write the test case files
outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10642/testcases"

for i, tc in enumerate(test_cases, 1):
    fname = f"{i:02d}"
    lines = []
    for (n, c1, n1, c2, n2) in tc:
        lines.append(str(n))
        lines.append(f"{c1} {n1}")
        lines.append(f"{c2} {n2}")
    lines.append("0")
    input_text = '\n'.join(lines) + '\n'

    with open(os.path.join(outdir, f"{fname}.in"), 'w') as f:
        f.write(input_text)

    print(f"Generated {fname}.in with {len(tc)} sub-case(s)")

print(f"\nTotal: {len(test_cases)} test files generated.")
