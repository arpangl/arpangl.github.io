#!/usr/bin/env python3
"""
Euclid Problem (UVa 10104 / 10645)

Given positive integers A and B (< 1000000001), find X, Y, D such that:
  A*X + B*Y = D, where D = gcd(A, B)

Among all valid (X, Y):
  - Minimize |X| + |Y| (primary)
  - If tied, choose X <= Y (secondary)

Extended GCD gives one particular solution (x0, y0).
General solution:  X = x0 + k*(B/D),  Y = y0 - k*(A/D)

We search for the k that minimizes |X| + |Y|, then apply the tiebreak.
"""

import math
import os

def extended_gcd(a, b):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def solve(A, B):
    """Find X, Y, D for the Euclid Problem."""
    D, x0, y0 = extended_gcd(A, B)

    # General solution: X = x0 + k*(B/D), Y = y0 - k*(A/D)
    step_x = B // D   # step for X per unit k
    step_y = A // D   # step for Y per unit k (subtracted)

    # We want to minimize f(k) = |x0 + k*step_x| + |y0 - k*step_y|
    # This is a sum of two absolute value functions of k, which is convex.
    # The minimum is achieved at or near the zeros of each term:
    #   k1 = -x0 / step_x  (makes X = 0)
    #   k2 =  y0 / step_y  (makes Y = 0)

    # We check a range of candidate k values around these zeros.
    candidates_k = set()

    if step_x != 0:
        k1 = -x0 / step_x
        for dk in range(-2, 3):
            candidates_k.add(math.floor(k1) + dk)
            candidates_k.add(math.ceil(k1) + dk)

    if step_y != 0:
        k2 = y0 / step_y
        for dk in range(-2, 3):
            candidates_k.add(math.floor(k2) + dk)
            candidates_k.add(math.ceil(k2) + dk)

    # Always include k=0
    candidates_k.add(0)

    best = None
    for k in candidates_k:
        X = x0 + k * step_x
        Y = y0 - k * step_y
        cost = abs(X) + abs(Y)
        # Tiebreak: minimize |X|+|Y|, then X <= Y
        if best is None or (cost < best[0]) or (cost == best[0] and X <= best[1]):
            best = (cost, X, Y)

    return best[1], best[2], D


def verify(A, B, X, Y, D):
    """Verify that AX + BY = D and D = gcd(A, B)."""
    assert A * X + B * Y == D, f"Failed: {A}*{X} + {B}*{Y} = {A*X+B*Y} != {D}"
    assert D == math.gcd(A, B), f"GCD mismatch: {D} != {math.gcd(A, B)}"


# ---------- Test cases ----------
test_cases = [
    # Sample cases from problem
    (4, 6),
    (17, 17),

    # Edge: both 1
    (1, 1),

    # Edge: one is 1
    (1, 1000000000),
    (1000000000, 1),

    # Edge: A == B
    (999999999, 999999999),

    # Coprime pair
    (7, 13),

    # One divides the other
    (6, 3),
    (3, 6),

    # Large coprime pair
    (999999937, 999999929),  # two large primes

    # Powers of 2
    (512, 1024),

    # GCD is large but not equal
    (123456789, 987654321),

    # Consecutive integers (always coprime)
    (999999999, 1000000000),

    # A = 1, B = 2 (smallest nontrivial)
    (1, 2),
    (2, 1),

    # Large with moderate GCD
    (500000000, 750000000),

    # Prime and composite sharing factor
    (6, 10),

    # Stress: both near max
    (999999998, 999999999),

    # One is prime, one is its multiple
    (7, 49),

    # Large GCD, small quotients
    (100000000, 200000000),
]

# Ensure we have 15-20 test cases
assert 15 <= len(test_cases) <= 20, f"Have {len(test_cases)} test cases"

outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10645/testcases"

for idx, (A, B) in enumerate(test_cases, start=1):
    X, Y, D = solve(A, B)
    verify(A, B, X, Y, D)

    fname = f"{idx:02d}"
    in_path = os.path.join(outdir, f"{fname}.in")
    out_path = os.path.join(outdir, f"{fname}.out")

    with open(in_path, "w") as f:
        f.write(f"{A} {B}\n")
    with open(out_path, "w") as f:
        f.write(f"{X} {Y} {D}\n")

    print(f"TC {fname}: A={A}, B={B} => X={X}, Y={Y}, D={D}  "
          f"(|X|+|Y|={abs(X)+abs(Y)}, check: {A*X+B*Y}=={D})")

print(f"\nGenerated {len(test_cases)} test cases. All verified.")
