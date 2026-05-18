import sys
import re
from itertools import product as iproduct

def parse_expr(expr):
    """Parse expression into list of numbers and operators."""
    nums = []
    ops = []
    i = 0
    cur = ""
    for ch in expr:
        if ch == '+' or ch == '*':
            nums.append(int(cur))
            ops.append(ch)
            cur = ""
        else:
            cur += ch
    nums.append(int(cur))
    return nums, ops

def all_results(nums, ops):
    """
    Return set of all possible values from parenthesizing the expression.
    nums[0] op[0] nums[1] op[1] ... nums[n-1]
    Uses interval DP.
    """
    n = len(nums)
    # dp[i][j] = set of all possible values for nums[i..j]
    dp = [[set() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        dp[i][i].add(nums[i])

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for left in dp[i][k]:
                    for right in dp[k+1][j]:
                        if ops[k] == '+':
                            dp[i][j].add(left + right)
                        else:
                            dp[i][j].add(left * right)

    return dp[0][n-1]

def solve(expr):
    nums, ops = parse_expr(expr)
    results = all_results(nums, ops)
    return max(results), min(results)

def main():
    input_data = sys.stdin.read().strip().split('\n')
    n = int(input_data[0])
    for i in range(1, n + 1):
        expr = input_data[i].strip()
        mx, mn = solve(expr)
        print(f"The maximum and minimum are {mx} and {mn}.")

if __name__ == '__main__':
    main()
