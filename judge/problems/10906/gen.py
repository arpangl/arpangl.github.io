import sys
import os
import json
import random
from collections import defaultdict, deque

def max_flow_solve(graph, source, sink):
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
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = u
        total_flow += path_flow
    return total_flow

def solve_matrix(R, C, cum_row, cum_col):
    row_sums = []
    for i in range(R):
        row_sums.append(cum_row[i] if i == 0 else cum_row[i] - cum_row[i-1])
    col_sums = []
    for j in range(C):
        col_sums.append(cum_col[j] if j == 0 else cum_col[j] - cum_col[j-1])

    adj_row = [row_sums[i] - C for i in range(R)]
    adj_col = [col_sums[j] - R for j in range(C)]

    source = 0
    sink = R + C + 1

    graph = defaultdict(lambda: defaultdict(int))
    for i in range(R):
        graph[source][i + 1] = adj_row[i]
    for i in range(R):
        for j in range(C):
            graph[i + 1][R + 1 + j] = 19
    for j in range(C):
        graph[R + 1 + j][sink] = adj_col[j]

    max_flow_solve(graph, source, sink)

    matrix = []
    for i in range(R):
        row = []
        for j in range(C):
            used = 19 - graph[i + 1][R + 1 + j]
            row.append(used + 1)
        matrix.append(row)
    return matrix

def verify(R, C, cum_row, cum_col, matrix):
    for i in range(R):
        for j in range(C):
            assert 1 <= matrix[i][j] <= 20
    row_sums = [sum(r) for r in matrix]
    col_sums = [sum(matrix[i][j] for i in range(R)) for j in range(C)]
    cr = []
    s = 0
    for r in row_sums:
        s += r
        cr.append(s)
    cc = []
    s = 0
    for c in col_sums:
        s += c
        cc.append(s)
    assert cr == list(cum_row), f"Row sums mismatch: {cr} != {list(cum_row)}"
    assert cc == list(cum_col), f"Col sums mismatch: {cc} != {list(cum_col)}"

def gen_valid_case(R, C, rng):
    """Generate a valid matrix and compute cumulative sums."""
    matrix = [[rng.randint(1, 20) for _ in range(C)] for _ in range(R)]
    row_sums = [sum(r) for r in matrix]
    col_sums = [sum(matrix[i][j] for i in range(R)) for j in range(C)]
    cum_row = []
    s = 0
    for r in row_sums:
        s += r
        cum_row.append(s)
    cum_col = []
    s = 0
    for c in col_sums:
        s += c
        cum_col.append(s)
    return cum_row, cum_col

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10906/testcases'
os.makedirs(TESTDIR, exist_ok=True)

all_tests = []

# Case 1: Sample
all_tests.append([
    (3, 4, [10, 31, 58], [10, 20, 37, 58]),
    (3, 4, [10, 31, 58], [10, 20, 37, 58]),
])

# Case 2: 1x1
all_tests.append([(1, 1, [5], [5])])

# Case 3: 1xC
all_tests.append([(1, 5, [15], [3, 6, 9, 12, 15])])

# Case 4: Rx1
all_tests.append([(4, 1, [5, 10, 15, 20], [20])])

# Case 5: 2x2 all ones
all_tests.append([(2, 2, [2, 4], [2, 4])])

# Case 6: 2x2 all 20s
all_tests.append([(2, 2, [40, 80], [40, 80])])

# Generate random cases
rng = random.Random(42)

# Case 7: 3x3
R, C = 3, 3
cr, cc = gen_valid_case(R, C, rng)
all_tests.append([(R, C, cr, cc)])

# Case 8: 5x5
R, C = 5, 5
cr, cc = gen_valid_case(R, C, rng)
all_tests.append([(R, C, cr, cc)])

# Case 9: 10x10
R, C = 10, 10
cr, cc = gen_valid_case(R, C, rng)
all_tests.append([(R, C, cr, cc)])

# Case 10: 20x20
R, C = 20, 20
cr, cc = gen_valid_case(R, C, rng)
all_tests.append([(R, C, cr, cc)])

# Case 11: 1x20
R, C = 1, 20
cr, cc = gen_valid_case(R, C, rng)
all_tests.append([(R, C, cr, cc)])

# Case 12: 20x1
R, C = 20, 1
cr, cc = gen_valid_case(R, C, rng)
all_tests.append([(R, C, cr, cc)])

# Case 13: Multiple test cases
cases13 = []
for _ in range(5):
    R = rng.randint(1, 10)
    C = rng.randint(1, 10)
    cr, cc = gen_valid_case(R, C, rng)
    cases13.append((R, C, cr, cc))
all_tests.append(cases13)

# Case 14: All entries = 1
R, C = 5, 5
cum_row = [C * (i+1) for i in range(R)]
cum_col = [R * (j+1) for j in range(C)]
all_tests.append([(R, C, cum_row, cum_col)])

# Case 15: Larger multiple
cases15 = []
for _ in range(3):
    R = rng.randint(5, 15)
    C = rng.randint(5, 15)
    cr, cc = gen_valid_case(R, C, rng)
    cases15.append((R, C, cr, cc))
all_tests.append(cases15)

for i, cases in enumerate(all_tests):
    lines_in = [str(len(cases))]
    lines_out = []

    for ci, (R, C, cr, cc) in enumerate(cases):
        lines_in.append(f"{R} {C}")
        lines_in.append(' '.join(map(str, cr)))
        lines_in.append(' '.join(map(str, cc)))

        matrix = solve_matrix(R, C, cr, cc)
        verify(R, C, cr, cc, matrix)

        lines_out.append(f"Matrix {ci+1}")
        for row in matrix:
            lines_out.append(' '.join(map(str, row)))

    inp = '\n'.join(lines_in) + '\n'
    out = '\n'.join(lines_out) + '\n'

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    print(f"Case {i+1:02d}: OK ({len(cases)} test case(s))")

problem = {
    "pid": "10906",
    "name": "Matrix Decompressing",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

print("All test cases generated and verified!")
