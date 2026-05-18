#!/usr/bin/env python3
"""
Generate test cases for Problem 10600: Network Connections
"""

import random
import os

# ---- Solver (Union-Find) ----

def solve(input_text):
    lines = input_text.strip().split('\n')
    idx = 0

    while idx < len(lines) and lines[idx].strip() == '':
        idx += 1
    T = int(lines[idx].strip())
    idx += 1

    results = []

    for t in range(T):
        while idx < len(lines) and lines[idx].strip() == '':
            idx += 1

        n = int(lines[idx].strip())
        idx += 1

        parent = list(range(n + 1))
        rank = [0] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1

        successful = 0
        unsuccessful = 0

        while idx < len(lines):
            line = lines[idx].strip()
            if line == '':
                idx += 1
                break
            parts = line.split()
            if len(parts) < 3:
                idx += 1
                continue
            cmd = parts[0]
            a, b = int(parts[1]), int(parts[2])
            if cmd == 'c':
                union(a, b)
            elif cmd == 'q':
                if find(a) == find(b):
                    successful += 1
                else:
                    unsuccessful += 1
            idx += 1

        results.append(f"{successful},{unsuccessful}")

    return '\n\n'.join(results)


def write_test(test_id, input_text, outdir):
    input_text = input_text.rstrip('\n') + '\n'
    output_text = solve(input_text)
    if not output_text.endswith('\n'):
        output_text += '\n'

    in_path = os.path.join(outdir, f"{test_id:02d}.in")
    out_path = os.path.join(outdir, f"{test_id:02d}.out")
    with open(in_path, 'w') as f:
        f.write(input_text)
    with open(out_path, 'w') as f:
        f.write(output_text)
    print(f"  Written {test_id:02d}.in / {test_id:02d}.out")


def make_dataset(n, commands):
    """Build one dataset block: n on first line, then command lines."""
    lines = [str(n)]
    for cmd, a, b in commands:
        lines.append(f"{cmd} {a} {b}")
    return '\n'.join(lines)


def make_input(datasets):
    """Wrap multiple dataset blocks into a full input (with T and blank lines)."""
    T = len(datasets)
    parts = [str(T), '']  # T followed by blank line
    for i, ds in enumerate(datasets):
        parts.append(ds)
        if i < T - 1:
            parts.append('')  # blank line between datasets
    return '\n'.join(parts)


outdir = '/Users/lambert/Documents/GPE-Helper/judge/problems/10600/testcases'
os.makedirs(outdir, exist_ok=True)
test_id = 1

# -------------------------------------------------------
# TC 01: Sample from problem statement
# -------------------------------------------------------
print(f"TC {test_id:02d}: Sample test case")
inp = "1\n\n10\nc 1 5\nc 2 7\nq 7 1\nc 3 9\nq 9 6\nc 2 5\nq 7 5"
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 02: Single computer, only queries (all unsuccessful since querying same node?
#         Actually q i i => same node => successful; q i j => unsuccessful)
#         Let's do n=1 with q 1 1
# -------------------------------------------------------
print(f"TC {test_id:02d}: Single computer, query itself")
ds = make_dataset(1, [('q', 1, 1)])
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 03: Two computers, no connection, query them
# -------------------------------------------------------
print(f"TC {test_id:02d}: Two computers, no connection, one query")
ds = make_dataset(2, [('q', 1, 2)])
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 04: Two computers, connect then query
# -------------------------------------------------------
print(f"TC {test_id:02d}: Two computers, connect then query")
ds = make_dataset(2, [('c', 1, 2), ('q', 1, 2)])
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 05: Only connections, no queries
# -------------------------------------------------------
print(f"TC {test_id:02d}: Only connections, no queries")
ds = make_dataset(5, [('c', 1, 2), ('c', 2, 3), ('c', 4, 5)])
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 06: Only queries, no connections (all unsuccessful except self-queries)
# -------------------------------------------------------
print(f"TC {test_id:02d}: Only queries, no connections")
cmds = [('q', 1, 2), ('q', 3, 4), ('q', 5, 5), ('q', 1, 5), ('q', 2, 2)]
ds = make_dataset(5, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 07: Chain connection: 1-2-3-4-5, queries along chain
# -------------------------------------------------------
print(f"TC {test_id:02d}: Chain connection with queries")
cmds = [
    ('c', 1, 2), ('c', 2, 3), ('c', 3, 4), ('c', 4, 5),
    ('q', 1, 5), ('q', 1, 3), ('q', 2, 4),
    ('q', 1, 1),  # self
]
ds = make_dataset(5, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 08: Multiple datasets (3 datasets)
# -------------------------------------------------------
print(f"TC {test_id:02d}: Multiple datasets (3)")
ds1 = make_dataset(3, [('c', 1, 2), ('q', 1, 2), ('q', 1, 3)])
ds2 = make_dataset(4, [('q', 1, 4), ('c', 1, 4), ('q', 1, 4)])
ds3 = make_dataset(2, [('q', 1, 2), ('c', 1, 2), ('q', 1, 2)])
inp = make_input([ds1, ds2, ds3])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 09: All computers connected into one component, all queries successful
# -------------------------------------------------------
print(f"TC {test_id:02d}: All connected, all queries successful")
cmds = []
for i in range(1, 10):
    cmds.append(('c', i, i + 1))
for i in range(1, 11):
    for j in range(i + 1, 11):
        if random.random() < 0.3:
            cmds.append(('q', i, j))
# Ensure at least a few queries
cmds.append(('q', 1, 10))
cmds.append(('q', 5, 8))
ds = make_dataset(10, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 10: Interleaved connect and query — order matters
# -------------------------------------------------------
print(f"TC {test_id:02d}: Interleaved connect/query, order matters")
cmds = [
    ('q', 1, 2),   # not connected yet => unsuccessful
    ('c', 1, 2),
    ('q', 1, 2),   # now connected => successful
    ('q', 2, 3),   # not connected => unsuccessful
    ('c', 2, 3),
    ('q', 1, 3),   # now connected via 2 => successful
    ('q', 4, 5),   # not connected => unsuccessful
    ('c', 4, 5),
    ('q', 1, 5),   # not connected => unsuccessful
    ('c', 3, 4),
    ('q', 1, 5),   # now connected 1-2-3-4-5 => successful
]
ds = make_dataset(5, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 11: Large-ish test, many computers, random operations
# -------------------------------------------------------
print(f"TC {test_id:02d}: Medium random test (n=100, 500 ops)")
random.seed(42)
n = 100
cmds = []
for _ in range(500):
    op = random.choice(['c', 'q'])
    a = random.randint(1, n)
    b = random.randint(1, n)
    cmds.append((op, a, b))
ds = make_dataset(n, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 12: Large test, many computers (n=1000, 5000 ops)
# -------------------------------------------------------
print(f"TC {test_id:02d}: Large random test (n=1000, 5000 ops)")
random.seed(123)
n = 1000
cmds = []
for _ in range(5000):
    op = random.choice(['c', 'q'])
    a = random.randint(1, n)
    b = random.randint(1, n)
    cmds.append((op, a, b))
ds = make_dataset(n, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 13: Duplicate connections (connect same pair multiple times)
# -------------------------------------------------------
print(f"TC {test_id:02d}: Duplicate connections")
cmds = [
    ('c', 1, 2), ('c', 1, 2), ('c', 1, 2),
    ('q', 1, 2),  # successful
    ('c', 3, 4), ('c', 3, 4),
    ('q', 1, 4),  # unsuccessful
    ('c', 2, 3),
    ('q', 1, 4),  # now successful
]
ds = make_dataset(4, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 14: Star topology — all connected to node 1
# -------------------------------------------------------
print(f"TC {test_id:02d}: Star topology")
n = 20
cmds = []
for i in range(2, n + 1):
    cmds.append(('c', 1, i))
# Query all pairs through center
for i in range(2, n + 1):
    for j in range(i + 1, n + 1):
        if random.random() < 0.15:
            cmds.append(('q', i, j))
cmds.append(('q', 2, n))
cmds.append(('q', 10, 15))
ds = make_dataset(n, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 15: Multiple disconnected components, queries across them
# -------------------------------------------------------
print(f"TC {test_id:02d}: Multiple disconnected components")
# Component A: {1,2,3}, Component B: {4,5,6}, Component C: {7,8,9}, isolated: {10}
cmds = [
    ('c', 1, 2), ('c', 2, 3),
    ('c', 4, 5), ('c', 5, 6),
    ('c', 7, 8), ('c', 8, 9),
    ('q', 1, 3),  # same component => successful
    ('q', 4, 6),  # same component => successful
    ('q', 7, 9),  # same component => successful
    ('q', 1, 4),  # different => unsuccessful
    ('q', 4, 7),  # different => unsuccessful
    ('q', 1, 10), # different => unsuccessful
    ('q', 10, 10),# same node => successful
    ('q', 3, 5),  # different => unsuccessful
]
ds = make_dataset(10, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 16: Merging components over time
# -------------------------------------------------------
print(f"TC {test_id:02d}: Merging components over time")
cmds = [
    ('c', 1, 2), ('c', 3, 4), ('c', 5, 6),
    ('q', 1, 3),  # different
    ('q', 5, 6),  # same
    ('c', 2, 3),  # merge {1,2} and {3,4}
    ('q', 1, 4),  # now same
    ('q', 1, 5),  # different
    ('c', 4, 5),  # merge all
    ('q', 1, 6),  # now same
    ('q', 2, 5),  # same
]
ds = make_dataset(6, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 17: Large test with multiple datasets
# -------------------------------------------------------
print(f"TC {test_id:02d}: Multiple large datasets")
random.seed(999)
datasets = []
for _ in range(5):
    n = random.randint(50, 200)
    num_ops = random.randint(100, 500)
    cmds = []
    for _ in range(num_ops):
        op = random.choice(['c', 'q'])
        a = random.randint(1, n)
        b = random.randint(1, n)
        cmds.append((op, a, b))
    datasets.append(make_dataset(n, cmds))
inp = make_input(datasets)
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 18: Edge case — connect a node to itself
# -------------------------------------------------------
print(f"TC {test_id:02d}: Connect node to itself")
cmds = [
    ('c', 1, 1),
    ('c', 2, 2),
    ('q', 1, 2),  # unsuccessful
    ('q', 1, 1),  # successful
    ('c', 1, 2),
    ('q', 1, 2),  # successful
]
ds = make_dataset(3, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 19: Stress test — n=10000, 50000 ops, single dataset
# -------------------------------------------------------
print(f"TC {test_id:02d}: Stress test (n=10000, 50000 ops)")
random.seed(7777)
n = 10000
cmds = []
for _ in range(50000):
    op = random.choice(['c', 'q'])
    a = random.randint(1, n)
    b = random.randint(1, n)
    cmds.append((op, a, b))
ds = make_dataset(n, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

# -------------------------------------------------------
# TC 20: Only self-queries
# -------------------------------------------------------
print(f"TC {test_id:02d}: Only self-queries (all successful)")
cmds = []
for i in range(1, 11):
    cmds.append(('q', i, i))
ds = make_dataset(10, cmds)
inp = make_input([ds])
write_test(test_id, inp, outdir)
test_id += 1

print(f"\nGenerated {test_id - 1} test cases total.")
