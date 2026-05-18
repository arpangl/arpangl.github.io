import sys
import bisect

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(input_data):
        n = int(input_data[idx]); idx += 1
        a = []
        for i in range(n):
            a.append(int(input_data[idx])); idx += 1

        if n == 0:
            results.append("1")
            continue

        # LIS ending at each position (from left)
        lis = [0] * n
        tails = []
        for i in range(n):
            pos = bisect.bisect_left(tails, a[i])
            if pos == len(tails):
                tails.append(a[i])
            else:
                tails[pos] = a[i]
            lis[i] = pos + 1

        # LDS ending at each position (from right) = LIS from right
        lds = [0] * n
        tails = []
        for i in range(n - 1, -1, -1):
            pos = bisect.bisect_left(tails, a[i])
            if pos == len(tails):
                tails.append(a[i])
            else:
                tails[pos] = a[i]
            lds[i] = pos + 1

        # For each position, wavio length = 2 * min(lis[i], lds[i]) - 1
        ans = 1
        for i in range(n):
            w = 2 * min(lis[i], lds[i]) - 1
            if w > ans:
                ans = w
        results.append(str(ans))

    print('\n'.join(results))

solve()
