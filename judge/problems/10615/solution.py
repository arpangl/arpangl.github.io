import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    M = int(input_data[idx]); idx += 1
    results = []
    for _ in range(M):
        N = int(input_data[idx]); idx += 1
        K = int(input_data[idx]); idx += 1
        nums = []
        for i in range(N):
            nums.append(int(input_data[idx])); idx += 1

        # DP: dp[i] is a set of possible remainders mod K after considering first i+1 numbers
        # The first number is always taken as-is (positive sign)
        dp = set()
        dp.add(nums[0] % K)

        for i in range(1, N):
            new_dp = set()
            v = nums[i] % K
            for r in dp:
                new_dp.add((r + v) % K)
                new_dp.add((r - v) % K)
            dp = new_dp

        if 0 in dp:
            results.append("Divisible")
        else:
            results.append("Not divisible")

    print('\n'.join(results))

solve()
