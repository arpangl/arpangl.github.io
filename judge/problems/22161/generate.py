#!/usr/bin/env python3
"""
Euclid Problem (22161) - Test case generator and solver.

Problem: Given positive integers A, B (< 1000000001), find X, Y, D such that
  AX + BY = D, where D = gcd(A, B).
  Among all valid (X, Y), pick the one with minimal |X|+|Y| (primary),
  and X <= Y (secondary tie-break).
"""

import math
import os

def extended_gcd(a, b):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, a // b * y1 - x1  # wait, let me redo this carefully
    # Actually: standard extended gcd
    # if b == 0: return (a, 1, 0)
    # g, x1, y1 = extended_gcd(b, a % b)
    # x = y1
    # y = x1 - (a // b) * y1
    # return g, x, y

# Let me rewrite cleanly:
def extended_gcd(a, b):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def solve(a, b):
    """
    Find X, Y, D such that A*X + B*Y = D = gcd(A, B),
    minimizing |X|+|Y| first, then requiring X <= Y as tie-break.
    """
    d = math.gcd(a, b)
    g, x0, y0 = extended_gcd(a, b)
    assert g == d
    assert a * x0 + b * y0 == d

    # General solution: X = x0 + k*(b/d), Y = y0 - k*(a/d)
    # |X| + |Y| = |x0 + k*B'| + |y0 - k*A'| where A' = a/d, B' = b/d
    bd = b // d
    ad = a // d

    # We need to find integer k that minimizes |x0 + k*bd| + |y0 - k*ad|
    # Let's try a range of candidate k values.
    # The optimal k is near where one of the terms is zero:
    #   k ~ -x0/bd  or  k ~ y0/ad

    best = None
    best_sum = float('inf')

    candidates = set()

    # k that makes X = 0: k = -x0 / bd
    if bd != 0:
        k_center1 = -x0 / bd
        for k in range(int(math.floor(k_center1)) - 2, int(math.ceil(k_center1)) + 3):
            candidates.add(k)

    # k that makes Y = 0: k = y0 / ad
    if ad != 0:
        k_center2 = y0 / ad
        for k in range(int(math.floor(k_center2)) - 2, int(math.ceil(k_center2)) + 3):
            candidates.add(k)

    # Also consider k=0
    candidates.add(0)

    for k in candidates:
        x = x0 + k * bd
        y = y0 - k * ad
        assert a * x + b * y == d, f"a={a}, b={b}, x={x}, y={y}, d={d}, k={k}"
        s = abs(x) + abs(y)
        if s < best_sum or (s == best_sum and (best is None or (x, y) < (best[0], best[1]))):
            # tie-break: X <= Y, so we prefer smaller X (i.e. x <= y)
            best_sum = s
            best = (x, y)

    # Among all solutions with same |X|+|Y|, pick X <= Y.
    # There might be two solutions with same sum but different (x,y).
    # Check: if (x, y) has same sum as (-x, -y) reflected... no, that changes d sign.
    # Actually the pair (x + bd, y - ad) vs (x, y). If both have same |.|+|.|,
    # we pick the one with x <= y.
    # Let's also collect ALL candidates with best_sum and pick the one with x <= y.
    all_best = []
    for k in candidates:
        x = x0 + k * bd
        y = y0 - k * ad
        s = abs(x) + abs(y)
        if s == best_sum:
            all_best.append((x, y))

    # Among all best, pick the one where X <= Y; if multiple, pick smallest X
    # "X <= Y (secondarily)" means among minimal |X|+|Y| solutions, pick X <= Y.
    # If there are solutions with X<=Y and X>Y with same sum, pick X<=Y.
    # Among those with X<=Y, if multiple, pick by smallest X? The problem just says X<=Y.
    valid = [(x, y) for x, y in all_best if x <= y]
    if valid:
        # If multiple valid, pick smallest |X|+|Y| (already guaranteed), then smallest X
        valid.sort(key=lambda p: (abs(p[0]) + abs(p[1]), p[0]))
        best = valid[0]
    else:
        # No solution with X<=Y at this sum -- pick the one closest to X<=Y
        # Actually, let's broaden search
        all_best.sort(key=lambda p: (p[0], -p[1]))
        best = all_best[0]

    return best[0], best[1], d


def verify(a, b, x, y, d):
    """Verify the solution."""
    assert a * x + b * y == d, f"FAIL: {a}*{x} + {b}*{y} = {a*x+b*y} != {d}"
    assert d == math.gcd(a, b), f"FAIL: gcd({a},{b}) = {math.gcd(a,b)} != {d}"


# Verify against sample
x, y, d = solve(4, 6)
assert (x, y, d) == (-1, 1, 2), f"Sample 1 failed: got {(x, y, d)}"
x, y, d = solve(17, 17)
assert (x, y, d) == (0, 1, 17), f"Sample 2 failed: got {(x, y, d)}"
print("Sample verification passed!")

# Define test cases
test_cases = [
    # Sample cases
    [(4, 6), (17, 17)],
    # Edge: both 1
    [(1, 1)],
    # Edge: A=1, B=large
    [(1, 1000000000)],
    # Edge: A=large, B=1
    [(1000000000, 1)],
    # Edge: A=B (equal, large)
    [(999999999, 999999999)],
    # Coprime pair
    [(7, 11)],
    # One divides the other
    [(6, 3), (3, 6)],
    # Large coprime
    [(999999937, 999999929)],
    # Fibonacci-like (worst case for Euclidean algorithm)
    [(832040, 514229)],
    # Power of 2 cases
    [(536870912, 268435456)],
    # Large with small gcd
    [(999999998, 999999994)],
    # Primes
    [(2, 3), (3, 5), (5, 7)],
    # A=2, B=large even
    [(2, 1000000000)],
    # Large coprime with big difference
    [(999999999, 2)],
    # GCD > 1, non-trivial
    [(12, 8), (100, 75)],
    # Near-max with gcd=1
    [(1000000000, 999999999)],
    # A=B=1
    [(1, 1)],
    # Mixed sizes
    [(1000000000, 3), (3, 1000000000)],
    # Additional edge cases
    [(7, 1), (1, 7)],
]

# Flatten and deduplicate while preserving grouping for files
all_pairs = []
for group in test_cases:
    for pair in group:
        all_pairs.append(pair)

# Limit to ~18 test files, each can have multiple lines
# Let's organize them into individual test files
cases_for_files = [
    # 00: Sample
    [(4, 6), (17, 17)],
    # 01: Both equal to 1
    [(1, 1)],
    # 02: A=1 with large B
    [(1, 1000000000)],
    # 03: Large A with B=1
    [(1000000000, 1)],
    # 04: A equals B (large)
    [(999999999, 999999999)],
    # 05: Small coprime pair
    [(7, 11)],
    # 06: One divides the other
    [(6, 3), (3, 6)],
    # 07: Large coprime primes
    [(999999937, 999999929)],
    # 08: Fibonacci numbers (worst case for extended GCD recursion depth)
    [(832040, 514229)],
    # 09: Powers of 2
    [(536870912, 268435456)],
    # 10: Large numbers, small gcd
    [(999999998, 999999994)],
    # 11: Small primes
    [(2, 3), (3, 5), (5, 7), (7, 11), (11, 13)],
    # 12: Even numbers
    [(2, 1000000000)],
    # 13: Large odd, small even
    [(999999999, 2)],
    # 14: Non-trivial GCD
    [(12, 8), (100, 75), (48, 36)],
    # 15: Near-max coprime
    [(1000000000, 999999999)],
    # 16: Large with small factor
    [(1000000000, 3), (3, 1000000000)],
    # 17: A=1 or B=1 variants
    [(7, 1), (1, 7)],
]

outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/22161/testcases"

for i, group in enumerate(cases_for_files):
    in_lines = []
    out_lines = []
    for a, b in group:
        in_lines.append(f"{a} {b}")
        x, y, d = solve(a, b)
        verify(a, b, x, y, d)
        out_lines.append(f"{x} {y} {d}")

    fname = f"{i:02d}"
    with open(os.path.join(outdir, f"{fname}.in"), "w") as f:
        f.write("\n".join(in_lines) + "\n")
    with open(os.path.join(outdir, f"{fname}.out"), "w") as f:
        f.write("\n".join(out_lines) + "\n")
    print(f"  {fname}: {len(group)} case(s) OK")

print(f"\nGenerated {len(cases_for_files)} test files.")
print("All verifications passed!")
