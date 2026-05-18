import sys
from collections import defaultdict, deque

def max_flow(graph, source, sink, n):
    """Edmonds-Karp max flow implementation."""
    def bfs(source, sink, parent):
        visited = set([source])
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in visited and graph[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    total_flow = 0
    while True:
        parent = {}
        if not bfs(source, sink, parent):
            break
        # Find min capacity along the path
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
        # Update capacities
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = u
        total_flow += path_flow
    return total_flow

def solve():
    data = sys.stdin.read().split()
    idx = 0
    T = int(data[idx]); idx += 1

    for t in range(1, T + 1):
        R = int(data[idx]); idx += 1
        C = int(data[idx]); idx += 1

        cum_row = []
        for i in range(R):
            cum_row.append(int(data[idx])); idx += 1

        cum_col = []
        for j in range(C):
            cum_col.append(int(data[idx])); idx += 1

        # Convert cumulative to actual sums
        row_sums = []
        for i in range(R):
            if i == 0:
                row_sums.append(cum_row[0])
            else:
                row_sums.append(cum_row[i] - cum_row[i-1])

        col_sums = []
        for j in range(C):
            if j == 0:
                col_sums.append(cum_col[0])
            else:
                col_sums.append(cum_col[j] - cum_col[j-1])

        # Since each entry must be between 1 and 20,
        # subtract 1 from each entry to make it 0-19
        # Then row_sums[i] -= C (since we subtract 1 from each of C entries)
        # And col_sums[j] -= R

        adj_row = [row_sums[i] - C for i in range(R)]
        adj_col = [col_sums[j] - R for j in range(C)]

        # Now entries are 0-19
        # Network flow:
        # Source -> row_i with capacity adj_row[i]
        # row_i -> col_j with capacity 19
        # col_j -> Sink with capacity adj_col[j]

        # Nodes: 0 = source, 1..R = rows, R+1..R+C = cols, R+C+1 = sink
        source = 0
        sink = R + C + 1
        num_nodes = R + C + 2

        graph = defaultdict(lambda: defaultdict(int))

        for i in range(R):
            graph[source][i + 1] = adj_row[i]

        for i in range(R):
            for j in range(C):
                graph[i + 1][R + 1 + j] = 19  # max entry - 1

        for j in range(C):
            graph[R + 1 + j][sink] = adj_col[j]

        flow = max_flow(graph, source, sink, num_nodes)

        # Extract matrix
        matrix = []
        for i in range(R):
            row = []
            for j in range(C):
                # Flow on edge from row i to col j = 19 - remaining capacity
                used = 19 - graph[i + 1][R + 1 + j]
                row.append(used + 1)  # Add back the 1
            matrix.append(row)

        print(f"Matrix {t}")
        for row in matrix:
            print(' '.join(map(str, row)))

solve()
