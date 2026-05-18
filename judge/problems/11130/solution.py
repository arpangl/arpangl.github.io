#!/usr/bin/env python3
"""
Solver for UVa 10254 / Problem 11130: The Priest Mathematician
4-peg Tower of Hanoi (Frame-Stewart algorithm)

f(0) = 0
f(1) = 1
f(n) = min over k in [1, n-1] of (2*f(k) + 2^(n-k) - 1)

Since n can be up to 10000, and the results are big integers, we need
Python's arbitrary precision integers.

Key insight: the optimal k for f(n) increases monotonically. We can
compute f(n) incrementally. The optimal split point k* for n satisfies
a known pattern related to triangular numbers. Specifically, the number
of discs moved by the 3-peg phase (n - k) follows the sequence:
1, 2, 3, 4, ... where each value t is used exactly t times.

That is, f(n) uses (n-k) = t where t is determined by the triangular
number pattern. The values of n where t increments are at triangular
numbers: n = 1, 2, 4, 7, 11, 16, ...  i.e. n = t*(t-1)/2 + 1.

So the sequence of (n-k) values as n goes 1,2,3,4,5,6,7,... is:
n=1: t=1
n=2: t=2
n=3: t=2  (since 2+3=5 > 4=2*2+0... let me just compute it directly)

Actually, let me just use the DP approach directly. It's efficient enough.
"""

import sys

def solve():
    MAXN = 10001

    # Precompute f(n) for n from 0 to MAXN
    f = [0] * MAXN
    # f(0) = 0, f(1) = 1
    if MAXN > 1:
        f[1] = 1

    # For the Frame-Stewart algorithm, the optimal k increases as n increases.
    # We track the best k for each n.
    best_k = 0

    for n in range(2, MAXN):
        # The optimal k is non-decreasing, so we only need to check from best_k onward
        # f(n) = min over k in [1..n-1] of (2*f(k) + 2^(n-k) - 1)
        # Start from the previous best_k and check k and k+1

        # Actually, let's be safe and check from best_k to best_k+2
        # but since we know it's monotonic, this is fine.

        min_val = None
        new_best_k = best_k

        for k in range(max(1, best_k), n):
            val = 2 * f[k] + (1 << (n - k)) - 1
            if min_val is None or val < min_val:
                min_val = val
                new_best_k = k
            elif val > min_val:
                # Since 2^(n-k) decreases as k increases and f(k) increases,
                # once val starts increasing we can stop
                break

        f[n] = min_val
        best_k = new_best_k

    return f

def main():
    f = solve()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        print(f[n])

if __name__ == '__main__':
    main()
