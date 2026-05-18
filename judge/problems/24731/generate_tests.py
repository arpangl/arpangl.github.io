#!/usr/bin/env python3
"""
Generate test cases for 24731 - Roads in the North (Tree Diameter).

The problem:
- Input: multiple test cases separated by blank lines
- Each test case: edges of a tree (u v w), find diameter (longest path)
- Up to 10,000 villages, numbered from 1
- All weights are positive integers
"""

import random
import os

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/24731/testcases"

def gen_random_tree(n, max_weight=1000):
    """Generate a random tree with n nodes (1-indexed). Returns list of (u, v, w)."""
    edges = []
    for i in range(2, n + 1):
        parent = random.randint(1, i - 1)
        w = random.randint(1, max_weight)
        edges.append((i, parent, w))
    # Shuffle edges and randomize order of u,v within each edge
    random.shuffle(edges)
    result = []
    for u, v, w in edges:
        if random.random() < 0.5:
            u, v = v, u
        result.append((u, v, w))
    return result

def gen_line_tree(n, max_weight=1000):
    """Generate a line/path tree: 1-2-3-...-n."""
    edges = []
    nodes = list(range(1, n + 1))
    random.shuffle(nodes)
    for i in range(len(nodes) - 1):
        w = random.randint(1, max_weight)
        edges.append((nodes[i], nodes[i + 1], w))
    random.shuffle(edges)
    return edges

def gen_star_tree(n, max_weight=1000):
    """Generate a star tree: node 1 connected to all others."""
    center = random.randint(1, n)
    edges = []
    for i in range(1, n + 1):
        if i != center:
            w = random.randint(1, max_weight)
            if random.random() < 0.5:
                edges.append((center, i, w))
            else:
                edges.append((i, center, w))
    random.shuffle(edges)
    return edges

def gen_caterpillar_tree(spine_len, max_legs_per_node=3, max_weight=1000):
    """Generate a caterpillar tree: a spine with legs hanging off."""
    edges = []
    node_id = spine_len + 1
    # Spine: 1-2-3-...-spine_len
    for i in range(1, spine_len):
        w = random.randint(1, max_weight)
        edges.append((i, i + 1, w))
    # Legs
    for i in range(1, spine_len + 1):
        num_legs = random.randint(0, max_legs_per_node)
        for _ in range(num_legs):
            w = random.randint(1, max_weight)
            edges.append((i, node_id, w))
            node_id += 1
    random.shuffle(edges)
    return edges

def gen_binary_tree(n, max_weight=1000):
    """Generate a nearly complete binary tree with n nodes."""
    edges = []
    for i in range(2, n + 1):
        parent = i // 2
        w = random.randint(1, max_weight)
        edges.append((parent, i, w))
    random.shuffle(edges)
    return edges

def edges_to_input(edges):
    """Convert edge list to input string."""
    lines = []
    for u, v, w in edges:
        lines.append(f"{u} {v} {w}")
    return '\n'.join(lines)

def write_test(test_id, input_str, output_str):
    """Write input/output files."""
    in_path = os.path.join(TESTCASE_DIR, f"{test_id:02d}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{test_id:02d}.out")
    with open(in_path, 'w') as f:
        f.write(input_str)
        if not input_str.endswith('\n'):
            f.write('\n')
    with open(out_path, 'w') as f:
        f.write(output_str)
        if not output_str.endswith('\n'):
            f.write('\n')

# ============================================================
# Solve function (same as solution.py)
# ============================================================
from collections import defaultdict, deque

def solve(lines):
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
    start = next(iter(nodes))
    far1, _ = bfs(start)
    far2, diameter = bfs(far1)
    return diameter

def compute_output(input_str):
    raw_lines = input_str.split('\n')
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
    return '\n'.join(results)

# ============================================================
# Generate test cases
# ============================================================

random.seed(42)
test_id = 1

# --- Test 01: Sample test case ---
inp = "5 1 6\n1 4 5\n6 3 9\n2 6 8\n6 1 7"
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 02: Minimal tree - 2 nodes, single edge ---
inp = "1 2 10"
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 03: 3 nodes, path ---
inp = "1 2 5\n2 3 7"
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 04: Star tree with 5 nodes (diameter = sum of two largest edge weights) ---
inp = "1 2 3\n1 3 5\n1 4 7\n1 5 2"
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 05: Line tree, 10 nodes ---
edges = gen_line_tree(10, max_weight=100)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 06: All edges weight 1, line tree 20 nodes ---
edges = []
nodes = list(range(1, 21))
random.shuffle(nodes)
for i in range(len(nodes) - 1):
    edges.append((nodes[i], nodes[i+1], 1))
random.shuffle(edges)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 07: Binary tree, 15 nodes ---
edges = gen_binary_tree(15, max_weight=50)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 08: Star tree, 100 nodes ---
edges = gen_star_tree(100, max_weight=500)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 09: Caterpillar tree, spine=20 ---
edges = gen_caterpillar_tree(20, max_legs_per_node=2, max_weight=100)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 10: Large line tree, 1000 nodes, large weights ---
edges = gen_line_tree(1000, max_weight=10000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 11: Large random tree, 5000 nodes ---
edges = gen_random_tree(5000, max_weight=1000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 12: Large random tree, 10000 nodes (max) ---
edges = gen_random_tree(10000, max_weight=10000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 13: Large star, 10000 nodes ---
edges = gen_star_tree(10000, max_weight=10000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 14: Large line tree, 10000 nodes (worst case for diameter) ---
edges = gen_line_tree(10000, max_weight=10000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 15: Large binary tree, 10000 nodes ---
edges = gen_binary_tree(10000, max_weight=5000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 16: Multiple test cases in one input ---
tc1_edges = gen_random_tree(50, max_weight=100)
tc2_edges = gen_line_tree(30, max_weight=200)
tc3_edges = gen_star_tree(20, max_weight=500)
inp = edges_to_input(tc1_edges) + "\n\n" + edges_to_input(tc2_edges) + "\n\n" + edges_to_input(tc3_edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 17: Multiple test cases, various sizes ---
parts = []
for _ in range(5):
    n = random.randint(3, 100)
    edges = gen_random_tree(n, max_weight=500)
    parts.append(edges_to_input(edges))
inp = "\n\n".join(parts)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 18: Edge case - 2 nodes with weight 1 ---
inp = "1 2 1"
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 19: Large caterpillar tree ---
edges = gen_caterpillar_tree(3000, max_legs_per_node=2, max_weight=5000)
inp = edges_to_input(edges)
write_test(test_id, inp, compute_output(inp))
test_id += 1

# --- Test 20: Multiple test cases with varying complexity ---
parts = []
# A single edge
parts.append("1 2 42")
# A medium random tree
edges = gen_random_tree(500, max_weight=1000)
parts.append(edges_to_input(edges))
# A medium line tree
edges = gen_line_tree(200, max_weight=500)
parts.append(edges_to_input(edges))
inp = "\n\n".join(parts)
write_test(test_id, inp, compute_output(inp))
test_id += 1

print(f"Generated {test_id - 1} test cases.")
