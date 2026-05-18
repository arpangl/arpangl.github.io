import sys
from collections import defaultdict

def solve(input_data):
    lines = input_data.strip().split('\n')
    idx = 0
    case_num = 0
    results = []

    while idx < len(lines):
        n = int(lines[idx].strip())
        idx += 1
        if n == 0:
            break
        case_num += 1
        s = int(lines[idx].strip())
        idx += 1

        adj = defaultdict(list)
        while idx < len(lines):
            parts = lines[idx].strip().split()
            p, q = int(parts[0]), int(parts[1])
            idx += 1
            if p == 0 and q == 0:
                break
            adj[p].append(q)

        # BFS/DFS with memoization to find longest path from s
        # memo[node] = (max_length_from_node, end_node)
        memo = {}

        def dfs(u):
            if u in memo:
                return memo[u]
            best_len = 0
            best_end = u  # if no outgoing edges, length 0, end at u itself
            for v in sorted(adj[u]):  # sort to handle tie-breaking
                vlen, vend = dfs(v)
                candidate_len = 1 + vlen
                if candidate_len > best_len:
                    best_len = candidate_len
                    best_end = vend
                elif candidate_len == best_len and vend < best_end:
                    best_end = vend
            memo[u] = (best_len, best_end)
            return memo[u]

        sys.setrecursionlimit(10000)
        length, end = dfs(s)
        results.append(f"Case {case_num}: The longest path from {s} has length {length}, finishing at {end}.")
        results.append("")  # blank line after each case

    return '\n'.join(results)


if __name__ == '__main__':
    input_data = sys.stdin.read()
    print(solve(input_data), end='')
