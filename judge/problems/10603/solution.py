import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    results = []

    while idx < len(input_data):
        l = int(input_data[idx]); idx += 1
        if l == 0:
            break
        n = int(input_data[idx]); idx += 1
        cuts = []
        for i in range(n):
            cuts.append(int(input_data[idx])); idx += 1

        # Add endpoints
        pts = [0] + cuts + [l]
        m = len(pts)  # m = n + 2

        # dp[i][j] = minimum cost to cut the sub-stick from pts[i] to pts[j]
        # We need at least 2 apart (i.e., j - i >= 2) to have a cut
        INF = float('inf')
        dp = [[0] * m for _ in range(m)]

        # length of chain
        for length in range(2, m):  # j - i = length
            for i in range(m - length):
                j = i + length
                dp[i][j] = INF
                cost = pts[j] - pts[i]  # cost of this cut
                for k in range(i + 1, j):
                    val = dp[i][k] + dp[k][j] + cost
                    if val < dp[i][j]:
                        dp[i][j] = val

        results.append(f"The minimum cutting is {dp[0][m-1]}.")

    print('\n'.join(results))

solve()
