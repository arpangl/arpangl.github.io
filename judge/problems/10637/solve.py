#!/usr/bin/env python3
"""
Tight words solver.

Given alphabet {0, 1, ..., k} and word length n,
compute percentage of tight words (consecutive digits differ by at most 1).

DP approach:
  dp[i][d] = number of tight words of length i that end with digit d
  dp[1][d] = 1 for all d in {0..k}
  dp[i][d] = sum of dp[i-1][d'] for d' such that |d - d'| <= 1

  Total tight words of length n = sum(dp[n][d] for d in 0..k)
  Total words of length n = (k+1)^n
  Percentage = tight / total * 100
"""

import sys
from decimal import Decimal, getcontext

getcontext().prec = 50

def solve(k, n):
    # k+1 digits: 0, 1, ..., k
    alpha = k + 1

    # dp[d] = number of tight words of current length ending with digit d
    dp = [Decimal(1)] * alpha

    for length in range(2, n + 1):
        new_dp = [Decimal(0)] * alpha
        for d in range(alpha):
            for dd in range(max(0, d - 1), min(alpha - 1, d + 1) + 1):
                new_dp[d] += dp[dd]
        dp = new_dp

    tight = sum(dp)
    total = Decimal(alpha) ** n
    percentage = tight / total * 100

    # Format to 5 decimal places
    return format(percentage, '.5f')


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        k, n = int(parts[0]), int(parts[1])
        print(solve(k, n))


if __name__ == '__main__':
    main()
