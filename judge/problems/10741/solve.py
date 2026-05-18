import sys
import heapq

def solve():
    data = sys.stdin.read().split()
    idx = 0

    results = []

    while idx < len(data):
        M = int(data[idx]); N = int(data[idx+1]); idx += 2
        if M == 0 and N == 0:
            break

        teams = []
        for i in range(M):
            teams.append(int(data[idx])); idx += 1

        tables = []
        for j in range(N):
            tables.append(int(data[idx])); idx += 1

        # Greedy: process teams in decreasing order of size
        # For each team, assign its members to the N largest-capacity tables
        # Use a max-heap (negate for min-heap)

        # We need to track original indices for output
        team_indices = list(range(M))
        team_indices.sort(key=lambda i: -teams[i])

        # table_caps[j] = remaining capacity of table j (original index j)
        # Use a max-heap of (-capacity, original_index)
        heap = []
        for j in range(N):
            heapq.heappush(heap, (-tables[j], j))

        # assignment[i] = list of table indices (1-indexed) for team i
        assignment = [[] for _ in range(M)]
        possible = True

        for ti in team_indices:
            need = teams[ti]
            if need > N:
                possible = False
                break

            # Take the top 'need' tables from heap
            taken = []
            for _ in range(need):
                if not heap:
                    possible = False
                    break
                neg_cap, tj = heapq.heappop(heap)
                cap = -neg_cap
                if cap <= 0:
                    possible = False
                    break
                assignment[ti].append(tj + 1)  # 1-indexed
                taken.append((cap - 1, tj))

            if not possible:
                break

            # Put them back
            for cap, tj in taken:
                if cap > 0:
                    heapq.heappush(heap, (-cap, tj))

        if possible:
            result_lines = ["1"]
            for i in range(M):
                assignment[i].sort()
                result_lines.append(' '.join(map(str, assignment[i])))
            results.append('\n'.join(result_lines))
        else:
            results.append("0")

    print('\n'.join(results))

solve()
