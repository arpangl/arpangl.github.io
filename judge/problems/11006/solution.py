import sys
from collections import deque

def solve(input_data):
    lines = input_data.strip().split('\n')
    idx = 0
    N = int(lines[idx]); idx += 1
    results = []
    for case_num in range(1, N + 1):
        parts = lines[idx].split(); idx += 1
        H, W = int(parts[0]), int(parts[1])
        grid = []
        for i in range(H):
            grid.append(lines[idx]); idx += 1

        visited = [[False]*W for _ in range(H)]
        lang_count = {}

        for r in range(H):
            for c in range(W):
                if not visited[r][c]:
                    ch = grid[r][c]
                    lang_count[ch] = lang_count.get(ch, 0) + 1
                    # BFS
                    queue = deque()
                    queue.append((r, c))
                    visited[r][c] = True
                    while queue:
                        cr, cc = queue.popleft()
                        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nr, nc = cr+dr, cc+dc
                            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc] and grid[nr][nc] == ch:
                                visited[nr][nc] = True
                                queue.append((nr, nc))

        # Sort: descending by count, then alphabetically by language
        sorted_langs = sorted(lang_count.items(), key=lambda x: (-x[1], x[0]))

        results.append(f"World #{case_num}")
        for lang, count in sorted_langs:
            results.append(f"{lang}: {count}")

    return '\n'.join(results)

if __name__ == '__main__':
    data = sys.stdin.read()
    print(solve(data))
