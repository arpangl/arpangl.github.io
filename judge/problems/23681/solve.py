#!/usr/bin/env python3
"""
Bachet's Game solver using dynamic programming (Sprague-Grundy).

For each game:
  - n stones, m move sizes in set S
  - dp[i] = True if the player whose turn it is (with i stones left) can win
  - dp[0] = False (no stones left = current player loses)
  - dp[i] = True if any s in S with s <= i and dp[i-s] == False

Stan moves first. If dp[n] is True, Stan wins; otherwise Ollie wins.
"""
import sys

def solve(input_text):
    results = []
    for line in input_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        tokens = list(map(int, line.split()))
        n = tokens[0]
        m = tokens[1]
        moves = tokens[2:2+m]

        # dp[i] = True means the current player (with i stones) wins
        dp = [False] * (n + 1)
        for i in range(1, n + 1):
            for s in moves:
                if s <= i and not dp[i - s]:
                    dp[i] = True
                    break

        if dp[n]:
            results.append("Stan wins")
        else:
            results.append("Ollie wins")
    return '\n'.join(results)

if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text))
