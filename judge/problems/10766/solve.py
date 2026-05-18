import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1

    results = []
    for case_num in range(1, N + 1):
        n = int(data[idx]); idx += 1
        m = int(data[idx]); idx += 1

        trees = []
        for i in range(n):
            x = int(data[idx]); idx += 1
            y = int(data[idx]); idx += 1
            trees.append((x, y))

        if m == 0:
            results.append(f"Case #{case_num}:\n0")
            continue

        # Precompute all line masks
        lines = set()
        for i in range(n):
            for j in range(i + 1, n):
                mask = 0
                dx = trees[j][0] - trees[i][0]
                dy = trees[j][1] - trees[i][1]
                for k in range(n):
                    dxk = trees[k][0] - trees[i][0]
                    dyk = trees[k][1] - trees[i][1]
                    if dx * dyk - dy * dxk == 0:
                        mask |= (1 << k)
                lines.add(mask)

        for i in range(n):
            lines.add(1 << i)

        lines = list(lines)

        # Bitmask DP
        full = (1 << n) - 1
        INF = n + 1
        dp = [INF] * (1 << n)
        dp[0] = 0

        # popcount cache
        popcount = [bin(x).count('1') for x in range(1 << n)]

        best = INF
        for mask in range(1 << n):
            if dp[mask] >= best:
                continue
            if popcount[mask] >= m:
                best = min(best, dp[mask])
                continue
            for line in lines:
                new_mask = mask | line
                if dp[mask] + 1 < dp[new_mask]:
                    dp[new_mask] = dp[mask] + 1

        # Check all masks with enough bits
        for mask in range(1 << n):
            if popcount[mask] >= m:
                best = min(best, dp[mask])

        results.append(f"Case #{case_num}:\n{best}")

    print('\n\n'.join(results))

solve()
