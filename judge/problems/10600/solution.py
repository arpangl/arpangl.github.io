import sys

def solve():
    input_data = sys.stdin.read().split('\n')
    idx = 0

    # Number of datasets
    while idx < len(input_data) and input_data[idx].strip() == '':
        idx += 1
    T = int(input_data[idx].strip())
    idx += 1

    results = []

    for t in range(T):
        # Skip blank lines
        while idx < len(input_data) and input_data[idx].strip() == '':
            idx += 1

        if idx >= len(input_data):
            break

        n = int(input_data[idx].strip())
        idx += 1

        # Union-Find
        parent = list(range(n + 1))
        rank = [0] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1

        successful = 0
        unsuccessful = 0

        while idx < len(input_data):
            line = input_data[idx].strip()
            if line == '':
                idx += 1
                break
            parts = line.split()
            if len(parts) < 3:
                idx += 1
                if idx >= len(input_data):
                    break
                continue
            cmd = parts[0]
            a, b = int(parts[1]), int(parts[2])
            if cmd == 'c':
                union(a, b)
            elif cmd == 'q':
                if find(a) == find(b):
                    successful += 1
                else:
                    unsuccessful += 1
            idx += 1

        results.append(f"{successful},{unsuccessful}")

    print('\n\n'.join(results))

solve()
