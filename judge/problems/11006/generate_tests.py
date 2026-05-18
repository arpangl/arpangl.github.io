import random
import os
from collections import deque

def solve_case(H, W, grid):
    visited = [[False]*W for _ in range(H)]
    lang_count = {}
    for r in range(H):
        for c in range(W):
            if not visited[r][c]:
                ch = grid[r][c]
                lang_count[ch] = lang_count.get(ch, 0) + 1
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
    sorted_langs = sorted(lang_count.items(), key=lambda x: (-x[1], x[0]))
    return sorted_langs

def write_test(test_id, cases, base_dir):
    """cases is a list of (H, W, grid_lines)"""
    in_path = os.path.join(base_dir, f"{test_id:02d}.in")
    out_path = os.path.join(base_dir, f"{test_id:02d}.out")

    in_lines = [str(len(cases))]
    out_lines = []

    for case_num, (H, W, grid) in enumerate(cases, 1):
        in_lines.append(f"{H} {W}")
        for row in grid:
            in_lines.append(row)
        out_lines.append(f"World #{case_num}")
        result = solve_case(H, W, grid)
        for lang, count in result:
            out_lines.append(f"{lang}: {count}")

    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/11006/testcases"

test_id = 1

# Test 1: Sample test case
write_test(test_id, [
    (4, 8, ["ttuuttdd","ttuuttdd","uuttuudd","uuttuudd"]),
    (9, 9, ["bbbbbbbbb","aaaaaaaab","bbbbbbbab","baaaaacab","bacccccab","bacbbbcab","bacccccab","baaaaaaab","bbbbbbbbb"]),
], base_dir)
test_id += 1

# Test 2: Minimum size 1x1 single cell
write_test(test_id, [
    (1, 1, ["a"]),
], base_dir)
test_id += 1

# Test 3: 1x1 with multiple test cases, single letter each
write_test(test_id, [
    (1, 1, ["z"]),
    (1, 1, ["a"]),
    (1, 1, ["m"]),
], base_dir)
test_id += 1

# Test 4: Single row
write_test(test_id, [
    (1, 20, ["abababababababababab"]),
], base_dir)
test_id += 1

# Test 5: Single column
write_test(test_id, [
    (20, 1, ["a","b","a","b","a","b","a","b","a","b","a","b","a","b","a","b","a","b","a","b"]),
], base_dir)
test_id += 1

# Test 6: All same letter (one big connected component)
write_test(test_id, [
    (5, 5, ["aaaaa"]*5),
], base_dir)
test_id += 1

# Test 7: Checkerboard pattern (maximum components for 2 letters)
H, W = 10, 10
grid = []
for r in range(H):
    row = ""
    for c in range(W):
        if (r + c) % 2 == 0:
            row += "a"
        else:
            row += "b"
    grid.append(row)
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

# Test 8: Spiral pattern - one language wrapping around another
write_test(test_id, [
    (7, 7, [
        "aaaaaaa",
        "abbbbba",
        "abababa",
        "abababa",
        "abababa",
        "abbbbba",
        "aaaaaaa",
    ]),
], base_dir)
test_id += 1

# Test 9: Multiple languages with tie-breaking (alphabetical order)
write_test(test_id, [
    (4, 4, [
        "aabb",
        "aabb",
        "ccdd",
        "ccdd",
    ]),
], base_dir)
test_id += 1

# Test 10: Horizontal stripes
write_test(test_id, [
    (6, 10, [
        "aaaaaaaaaa",
        "bbbbbbbbbb",
        "cccccccccc",
        "aaaaaaaaaa",
        "bbbbbbbbbb",
        "cccccccccc",
    ]),
], base_dir)
test_id += 1

# Test 11: Vertical stripes
write_test(test_id, [
    (6, 8, [
        "aabbccdd",
        "aabbccdd",
        "aabbccdd",
        "aabbccdd",
        "aabbccdd",
        "aabbccdd",
    ]),
], base_dir)
test_id += 1

# Test 12: L-shaped regions and complex connectivity
write_test(test_id, [
    (5, 5, [
        "aabba",
        "aabba",
        "bbbba",
        "ccaaa",
        "ccaaa",
    ]),
], base_dir)
test_id += 1

# Test 13: All 26 letters appear (each exactly once in a single row)
write_test(test_id, [
    (1, 20, ["abcdefghijklmnopqrst"]),
], base_dir)
test_id += 1

# Test 14: Max size 20x20, random with few letters (creates many components)
random.seed(42)
H, W = 20, 20
grid = []
for r in range(H):
    row = ''.join(random.choice("abc") for _ in range(W))
    grid.append(row)
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

# Test 15: Max size 20x20, random with many letters (26 letters)
random.seed(123)
H, W = 20, 20
grid = []
for r in range(H):
    row = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(W))
    grid.append(row)
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

# Test 16: Border frame pattern
H, W = 10, 10
grid = []
for r in range(H):
    row = ""
    for c in range(W):
        if r == 0 or r == H-1 or c == 0 or c == W-1:
            row += "x"
        else:
            row += "y"
    grid.append(row)
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

# Test 17: Diagonal-ish pattern creating many isolated components
H, W = 10, 10
grid = []
for r in range(H):
    row = ""
    for c in range(W):
        if (r + c) % 3 == 0:
            row += "a"
        elif (r + c) % 3 == 1:
            row += "b"
        else:
            row += "c"
    grid.append(row)
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

# Test 18: Multiple test cases with varying sizes
write_test(test_id, [
    (1, 1, ["z"]),
    (2, 2, ["ab","ba"]),
    (3, 3, ["aaa","bbb","aaa"]),
    (20, 20, ["a"*20]*20),
    (5, 5, ["abcde","fghij","klmno","pqrst","uvwxy"]),
], base_dir)
test_id += 1

# Test 19: Snake-like pattern (one connected region winding through the grid)
H, W = 10, 10
grid_arr = [['b']*W for _ in range(H)]
# Create a snake path of 'a'
r, c = 0, 0
direction = 1  # 1 = right, -1 = left
for row in range(H):
    if direction == 1:
        for col in range(W):
            grid_arr[row][col] = 'a'
    else:
        for col in range(W-1, -1, -1):
            grid_arr[row][col] = 'a'
    direction *= -1
# Actually this fills everything with 'a'. Let me make it a thin snake.
grid_arr = [['b']*W for _ in range(H)]
r = 0
direction = 1
for row in range(0, H, 2):
    if direction == 1:
        for col in range(W):
            grid_arr[row][col] = 'a'
        if row + 1 < H:
            grid_arr[row+1][W-1] = 'a'  # connect to next row
    else:
        for col in range(W):
            grid_arr[row][col] = 'a'
        if row + 1 < H:
            grid_arr[row+1][0] = 'a'  # connect to next row
    direction *= -1
grid = [''.join(row) for row in grid_arr]
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

# Test 20: Islands - many small isolated components of different letters
H, W = 20, 20
grid_arr = [['.']*W for _ in range(H)]
# Fill with 'z' as background
for r in range(H):
    for c in range(W):
        grid_arr[r][c] = 'z'
# Place isolated single-cell islands at every other position
letters = "abcdefghijklmnopqrst"
li = 0
for r in range(0, H, 2):
    for c in range(0, W, 2):
        grid_arr[r][c] = letters[li % len(letters)]
        li += 1
grid = [''.join(row) for row in grid_arr]
write_test(test_id, [(H, W, grid)], base_dir)
test_id += 1

print(f"Generated {test_id - 1} test cases.")
