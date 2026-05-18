import sys
import heapq
import math

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    scenario = 0

    results = []

    while True:
        N = int(input_data[idx]); idx += 1
        R = int(input_data[idx]); idx += 1

        if N == 0 and R == 0:
            break

        scenario += 1

        # Adjacency list: node -> [(neighbor, capacity)]
        adj = [[] for _ in range(N + 1)]

        for _ in range(R):
            c1 = int(input_data[idx]); idx += 1
            c2 = int(input_data[idx]); idx += 1
            p = int(input_data[idx]); idx += 1
            adj[c1].append((c2, p))
            adj[c2].append((c1, p))

        S = int(input_data[idx]); idx += 1
        D = int(input_data[idx]); idx += 1
        T = int(input_data[idx]); idx += 1

        # Modified Dijkstra to find the path that maximizes the minimum edge capacity
        # Use a max-heap (negate values for Python's min-heap)
        # dist[v] = maximum possible minimum capacity on any path from S to v
        dist = [0] * (N + 1)
        dist[S] = float('inf')
        # (-capacity, node)
        pq = [(-float('inf'), S)]

        while pq:
            neg_cap, u = heapq.heappop(pq)
            cap = -neg_cap
            if cap < dist[u]:
                continue
            if u == D:
                break
            for v, w in adj[u]:
                new_cap = min(cap, w)
                if new_cap > dist[v]:
                    dist[v] = new_cap
                    heapq.heappush(pq, (-new_cap, v))

        bottleneck = dist[D]
        # Mr. G rides with each group, so each trip carries (bottleneck - 1) tourists
        if bottleneck <= 1:
            # Should not happen given P > 1, but safety
            trips = T  # or impossible
        else:
            trips = math.ceil(T / (bottleneck - 1))

        results.append(f"Scenario #{scenario}")
        results.append(f"Minimum Number of Trips = {trips}")
        results.append("")

    print("\n".join(results))

solve()
