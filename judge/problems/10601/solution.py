import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split('\n')
    idx = 0
    T = int(input_data[idx]); idx += 1
    for _ in range(T):
        parts = input_data[idx].split()
        R, C = int(parts[0]), int(parts[1])
        idx += 1
        grid = []
        sr = sc = er = ec = -1
        for r in range(R):
            row = input_data[idx]; idx += 1
            # Ensure row is exactly C characters (strip trailing whitespace)
            row = row.rstrip()
            grid.append(row)
            for c in range(len(row)):
                if row[c] == 'S':
                    sr, sc = r, c
                elif row[c] == 'E':
                    er, ec = r, c

        # BFS with state (row, col, phase)
        # phase 0 -> next move is 1 step
        # phase 1 -> next move is 2 steps
        # phase 2 -> next move is 3 steps
        steps = [1, 2, 3]
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E

        # dist[r][c][phase] = minimum moves to reach (r,c) with next move being phase
        INF = float('inf')
        dist = [[[INF]*3 for _ in range(C)] for _ in range(R)]
        dist[sr][sc][0] = 0

        queue = deque()
        queue.append((sr, sc, 0))  # start at S, phase 0 (next move = 1 step)

        while queue:
            r, c, phase = queue.popleft()
            d = dist[r][c][phase]
            step = steps[phase]
            next_phase = (phase + 1) % 3

            for dr, dc in dirs:
                # Try moving 'step' cells in direction (dr, dc)
                nr, nc = r, c
                ok = True
                for s in range(1, step + 1):
                    nr, nc = r + dr * s, c + dc * s
                    if nr < 0 or nr >= R or nc < 0 or nc >= C or grid[nr][nc] == '#':
                        ok = False
                        break
                if ok:
                    if dist[nr][nc][next_phase] > d + 1:
                        dist[nr][nc][next_phase] = d + 1
                        queue.append((nr, nc, next_phase))

        ans = min(dist[er][ec][0], dist[er][ec][1], dist[er][ec][2])
        if ans == INF:
            print("NO")
        else:
            print(ans)

solve()
