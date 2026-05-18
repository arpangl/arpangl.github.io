#!/usr/bin/env python3
"""
Generate test cases for problem 10417: The Hotel with Infinite Rooms.

Constraints:
  1 <= S <= 10000
  1 <= D < 10^15
  All input and output integers < 10^15
"""

import math
import os

def solve(S, D):
    a = 1
    b = 2 * S - 1
    c = -2 * D
    discriminant = b * b - 4 * a * c
    m_approx = (-b + math.isqrt(discriminant)) // (2 * a)

    def cumulative(m):
        if m <= 0:
            return 0
        return m * S + m * (m - 1) // 2

    m = max(1, m_approx)
    while m > 1 and cumulative(m - 1) >= D:
        m -= 1
    while cumulative(m) < D:
        m += 1

    return S + m - 1


test_cases = []

# 1. Minimal input
test_cases.append((1, 1))

# 2. S=1, D=3 => last day of group 2 (size 2, days 2-3)
test_cases.append((1, 3))

# 3. S=1, D=4 => first day of group 3
test_cases.append((1, 4))

# 4. Sample: S=1, D=6
test_cases.append((1, 6))

# 5. Sample: S=3, D=10
test_cases.append((3, 10))

# 6. Sample: S=3, D=14
test_cases.append((3, 14))

# 7. S=10000, D=1 (first day of first large group)
test_cases.append((10000, 1))

# 8. S=10000, D=10000 (last day of first group)
test_cases.append((10000, 10000))

# 9. S=10000, D=10001 (first day of second group)
test_cases.append((10000, 10001))

# 10. S=1, D near max (~10^15)
test_cases.append((1, 999999999999999))

# 11. S=10000, D near max
test_cases.append((10000, 999999999999999))

# 12. S=1, D=55 (exact boundary: cum(10)=55, last day of group 10)
test_cases.append((1, 55))

# 13. S=1, D=56 (first day of group 11)
test_cases.append((1, 56))

# 14. S=5, D=5 (last day of first group)
test_cases.append((5, 5))

# 15. S=5, D=11 (last day of second group: 5+6=11)
test_cases.append((5, 11))

# 16. S=10000, D=20001 (last day of second group: 10000+10001=20001)
test_cases.append((10000, 20001))

# 17. S=10000, D=20002 (first day of third group)
test_cases.append((10000, 20002))

# 18. S=1, D=10 (exact boundary: cum(4)=10)
test_cases.append((1, 10))

# 19. S=9999, D near max
test_cases.append((9999, 999999999999990))

# 20. S=5000, D=500000000000000
test_cases.append((5000, 500000000000000))


print(f"Total test cases: {len(test_cases)}")

outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10417/testcases"

for i, (S, D) in enumerate(test_cases, 1):
    ans = solve(S, D)
    assert 1 <= S <= 10000, f"Test {i}: S={S} out of range"
    assert 1 <= D < 10**15, f"Test {i}: D={D} out of range"
    assert ans < 10**15, f"Test {i}: answer={ans} >= 10^15"

    fname_in = os.path.join(outdir, f"{i:02d}.in")
    fname_out = os.path.join(outdir, f"{i:02d}.out")

    with open(fname_in, "w") as f:
        f.write(f"{S} {D}\n")
    with open(fname_out, "w") as f:
        f.write(f"{ans}\n")

    print(f"Test {i:02d}: S={S}, D={D} => {ans}")

print("All test cases generated and verified.")
