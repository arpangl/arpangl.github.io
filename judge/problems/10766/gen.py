import os
import json
import random

def solve_case(n, m, trees):
    if m == 0:
        return 0

    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            mask = 0
            dx = trees[j][0] - trees[i][0]
            dy = trees[j][1] - trees[i][1]
            for k in range(n):
                dxk = trees[k][0] - trees[i][0]
                dyk = trees[k][1] - trees[i][1]
                if dx * dyk - dy * dxk == 0:
                    mask |= (1 << k)
            lines.add(mask)

    for i in range(n):
        lines.add(1 << i)

    lines = list(lines)

    INF = n + 1
    dp = [INF] * (1 << n)
    dp[0] = 0

    popcount = [bin(x).count('1') for x in range(1 << n)]

    best = INF
    for mask in range(1 << n):
        if dp[mask] >= best:
            continue
        if popcount[mask] >= m:
            best = min(best, dp[mask])
            continue
        for line in lines:
            new_mask = mask | line
            if dp[mask] + 1 < dp[new_mask]:
                dp[new_mask] = dp[mask] + 1

    for mask in range(1 << n):
        if popcount[mask] >= m:
            best = min(best, dp[mask])

    return best

def format_test(cases):
    lines = [str(len(cases))]
    for n, m, trees in cases:
        lines.append(str(n))
        lines.append(str(m))
        for x, y in trees:
            lines.append(f"{x} {y}")
    return '\n'.join(lines) + '\n'

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10766/testcases'
os.makedirs(TESTDIR, exist_ok=True)

all_tests = []

# Case 1: Sample
all_tests.append([
    (4, 4, [(0,0),(0,1),(1,0),(1,1)]),
    (9, 7, [(0,0),(1,1),(0,2),(2,0),(2,2),(3,0),(3,1),(3,2),(3,4)])
])

# Case 2: Single tree, m=1
all_tests.append([(1, 1, [(0, 0)])])

# Case 3: Single tree, m=0
all_tests.append([(1, 0, [(5, 5)])])

# Case 4: All collinear
all_tests.append([(5, 5, [(i, i) for i in range(5)])])

# Case 5: All collinear, m < n
all_tests.append([(6, 3, [(i*2, 0) for i in range(6)])])

# Case 6: Grid 3x3
all_tests.append([(9, 9, [(i, j) for i in range(3) for j in range(3)])])

# Case 7: Grid 4x4
all_tests.append([(16, 16, [(i, j) for i in range(4) for j in range(4)])])

# Case 8: No three collinear (triangle + points)
all_tests.append([(3, 3, [(0,0),(1,0),(0,1)])])

# Case 9: m = 1 (always answer 1)
random.seed(42)
trees = [(random.randint(-100,100), random.randint(-100,100)) for _ in range(10)]
# Ensure unique
trees = list(set(trees))[:10]
all_tests.append([(len(trees), 1, trees)])

# Case 10: Random n=12
random.seed(100)
n = 12
trees = set()
while len(trees) < n:
    trees.add((random.randint(-50, 50), random.randint(-50, 50)))
trees = list(trees)
m = 8
all_tests.append([(n, m, trees)])

# Case 11: Two parallel lines
trees = [(0, i) for i in range(5)] + [(1, i) for i in range(5)]
all_tests.append([(10, 10, trees)])

# Case 12: Star from origin
import math
trees = [(0, 0)]
for angle_deg in range(0, 360, 30):
    a = math.radians(angle_deg)
    trees.append((int(100 * math.cos(a)), int(100 * math.sin(a))))
n = len(trees)
# Remove duplicates
trees = list(set(trees))
n = len(trees)
all_tests.append([(n, n, trees)])

# Case 13: Random n=14
random.seed(200)
n = 14
trees = set()
while len(trees) < n:
    trees.add((random.randint(-100, 100), random.randint(-100, 100)))
trees = list(trees)
m = 10
all_tests.append([(n, m, trees)])

# Case 14: Two test cases mixed
random.seed(300)
cases14 = []
for _ in range(2):
    n = random.randint(3, 10)
    trees = set()
    while len(trees) < n:
        trees.add((random.randint(-50, 50), random.randint(-50, 50)))
    trees = list(trees)
    m = random.randint(1, n)
    cases14.append((n, m, trees))
all_tests.append(cases14)

# Case 15: Edge - n=16, m=16
random.seed(400)
n = 16
trees = set()
while len(trees) < n:
    trees.add((random.randint(-1000, 1000), random.randint(-1000, 1000)))
trees = list(trees)
all_tests.append([(n, n, trees)])

for i, cases in enumerate(all_tests):
    inp = format_test(cases)
    out_lines = []
    for ci, (n, m, trees) in enumerate(cases):
        ans = solve_case(n, m, trees)
        out_lines.append(f"Case #{ci+1}:\n{ans}")
    out = '\n\n'.join(out_lines) + '\n'

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    print(f"Case {i+1:02d}: OK")

problem = {
    "pid": "10766",
    "name": "Antimatter Ray Clearcutting",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

print("All test cases generated!")
