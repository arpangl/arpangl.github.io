#!/usr/bin/env python3
"""
Solver for Problem 10621: Luggage
Subset sum / partition problem: can we split suitcases into two equal-weight groups?

Input: first line = m (number of test cases), then m lines each with space-separated weights.
Output: for each test case, "YES" or "NO".
"""
import sys

def can_partition(weights):
    total = sum(weights)
    if total % 2 != 0:
        return False
    target = total // 2
    # DP subset sum
    dp = [False] * (target + 1)
    dp[0] = True
    for w in weights:
        # iterate backwards to avoid reusing the same item
        for j in range(target, w - 1, -1):
            if dp[j - w]:
                dp[j] = True
    return dp[target]

def solve(input_text):
    lines = input_text.strip().split('\n')
    m = int(lines[0].strip())
    results = []
    for i in range(1, m + 1):
        weights = list(map(int, lines[i].strip().split()))
        if can_partition(weights):
            results.append("YES")
        else:
            results.append("NO")
    return '\n'.join(results)

if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text))
