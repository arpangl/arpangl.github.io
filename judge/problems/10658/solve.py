import sys

def solve(input_data):
    lines = input_data.strip().split('\n')
    elephants = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            w, s = int(parts[0]), int(parts[1])
            elephants.append((w, s))

    n = len(elephants)
    if n == 0:
        return "0\n"

    # Sort by weight ascending, then by IQ descending (for tie-breaking)
    indexed = list(range(n))
    indexed.sort(key=lambda i: (elephants[i][0], -elephants[i][1]))

    # LIS on decreasing IQ with strictly increasing weight
    dp = [1] * n
    parent = [-1] * n

    for i in range(n):
        for j in range(i):
            ii, jj = indexed[i], indexed[j]
            if elephants[jj][0] < elephants[ii][0] and elephants[jj][1] > elephants[ii][1]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

    # Find the best
    best_len = max(dp)
    best_idx = dp.index(best_len)

    # Reconstruct
    seq = []
    idx = best_idx
    while idx != -1:
        seq.append(indexed[idx] + 1)  # 1-indexed
        idx = parent[idx]
    seq.reverse()

    result = [str(best_len)]
    for s in seq:
        result.append(str(s))
    return '\n'.join(result) + '\n'

if __name__ == '__main__':
    data = sys.stdin.read()
    print(solve(data), end='')
