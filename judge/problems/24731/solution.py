import sys
from collections import defaultdict, deque

def solve(lines):
    """Given lines of one test case, compute the tree diameter."""
    adj = defaultdict(list)
    nodes = set()
    for line in lines:
        parts = line.split()
        if len(parts) < 3:
            continue
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        adj[u].append((v, w))
        adj[v].append((u, w))
        nodes.add(u)
        nodes.add(v)

    if not nodes:
        return 0

    # BFS to find farthest node from start
    def bfs(start):
        dist = {start: 0}
        queue = deque([start])
        farthest = start
        max_dist = 0
        while queue:
            u = queue.popleft()
            for v, w in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + w
                    queue.append(v)
                    if dist[v] > max_dist:
                        max_dist = dist[v]
                        farthest = v
        return farthest, max_dist

    # Two BFS to find diameter
    start = next(iter(nodes))
    far1, _ = bfs(start)
    far2, diameter = bfs(far1)
    return diameter

def main():
    input_data = sys.stdin.read()
    # Split by blank lines to get separate test cases
    # A blank line is a line that is empty or contains only whitespace
    raw_lines = input_data.split('\n')

    test_cases = []
    current = []
    for line in raw_lines:
        stripped = line.strip()
        if stripped == '':
            if current:
                test_cases.append(current)
                current = []
        else:
            current.append(stripped)
    if current:
        test_cases.append(current)

    results = []
    for tc in test_cases:
        results.append(str(solve(tc)))

    print('\n'.join(results))

if __name__ == '__main__':
    main()
