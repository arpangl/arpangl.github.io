#!/usr/bin/env python3
"""
Generate test cases for problem 10644 - The Tourist Guide.

Problem summary:
- Undirected graph with N cities and R roads.
- Each road has a passenger capacity P (P > 1).
- Mr. G must ride with each group, so each trip carries at most (bottleneck - 1) tourists.
- Find the path from S to D maximizing the minimum edge capacity (widest path / bottleneck path).
- Answer = ceil(T / (bottleneck - 1)).

Input format per test case:
  N R
  C1 C2 P  (R lines)
  S D T
Terminated by: 0 0

Output format:
  Scenario #X
  Minimum Number of Trips = Y
  (blank line)
"""

import os
import random
import math
import heapq

TESTCASES_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10644/testcases"

def compute_answer(scenarios):
    """Compute answers for a list of scenarios."""
    results = []
    for sc_idx, (N, edges, S, D, T) in enumerate(scenarios, 1):
        adj = [[] for _ in range(N + 1)]
        for c1, c2, p in edges:
            adj[c1].append((c2, p))
            adj[c2].append((c1, p))

        # Modified Dijkstra: maximize minimum capacity
        dist = [0] * (N + 1)
        dist[S] = float('inf')
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
        if bottleneck <= 1:
            trips = T
        else:
            trips = math.ceil(T / (bottleneck - 1))

        results.append((sc_idx, trips))
    return results


def format_input(scenarios):
    """Format scenarios into input string."""
    lines = []
    for N, edges, S, D, T in scenarios:
        lines.append(f"{N} {len(edges)}")
        for c1, c2, p in edges:
            lines.append(f"{c1} {c2} {p}")
        lines.append(f"{S} {D} {T}")
    lines.append("0 0")
    return "\n".join(lines) + "\n"


def format_output(results):
    """Format results into output string."""
    lines = []
    for sc_idx, trips in results:
        lines.append(f"Scenario #{sc_idx}")
        lines.append(f"Minimum Number of Trips = {trips}")
        lines.append("")
    return "\n".join(lines) + "\n"


def write_test(test_id, scenarios):
    """Write a test case file pair."""
    inp = format_input(scenarios)
    results = compute_answer(scenarios)
    out = format_output(results)

    in_path = os.path.join(TESTCASES_DIR, f"{test_id:02d}.in")
    out_path = os.path.join(TESTCASES_DIR, f"{test_id:02d}.out")

    with open(in_path, "w") as f:
        f.write(inp)
    with open(out_path, "w") as f:
        f.write(out)

    print(f"Test {test_id:02d}: {len(scenarios)} scenario(s)")


def gen_random_connected_graph(N, R, min_cap=2, max_cap=100):
    """Generate a random connected graph with N nodes and R edges."""
    # First, create a spanning tree to ensure connectivity
    edges = set()
    nodes = list(range(1, N + 1))
    random.shuffle(nodes)
    tree_edges = []
    for i in range(1, N):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        a, b = min(u, v), max(u, v)
        edges.add((a, b))
        tree_edges.append((a, b))

    # Add remaining edges
    max_edges = N * (N - 1) // 2
    R = min(R, max_edges)
    attempts = 0
    while len(edges) < R and attempts < R * 10:
        u = random.randint(1, N)
        v = random.randint(1, N)
        if u != v:
            a, b = min(u, v), max(u, v)
            edges.add((a, b))
        attempts += 1

    result = []
    for a, b in edges:
        p = random.randint(min_cap, max_cap)
        result.append((a, b, p))

    return result


# ============================================================
# TEST CASES
# ============================================================

test_id = 0

# ------ Test 01: Sample test case ------
test_id += 1
scenarios = [(
    7,
    [(1,2,30),(1,3,15),(1,4,10),(2,4,25),(2,5,60),(3,4,40),(3,6,20),(4,7,35),(5,7,20),(6,7,30)],
    1, 7, 99
)]
write_test(test_id, scenarios)

# ------ Test 02: Minimal graph - 2 nodes, 1 edge ------
test_id += 1
scenarios = [(2, [(1, 2, 2)], 1, 2, 1)]
write_test(test_id, scenarios)

# ------ Test 03: Minimal with exactly 1 trip needed ------
test_id += 1
# capacity=10, so 9 tourists per trip. T=9 => 1 trip
scenarios = [(2, [(1, 2, 10)], 1, 2, 9)]
write_test(test_id, scenarios)

# ------ Test 04: Capacity=2 means only 1 tourist per trip ------
test_id += 1
scenarios = [(2, [(1, 2, 2)], 1, 2, 100)]
write_test(test_id, scenarios)

# ------ Test 05: Linear path, bottleneck is the minimum edge ------
test_id += 1
# 1--2--3--4--5, capacities: 10, 5, 20, 3
# bottleneck = 3, trips = ceil(50 / 2) = 25
scenarios = [(5, [(1,2,10),(2,3,5),(3,4,20),(4,5,3)], 1, 5, 50)]
write_test(test_id, scenarios)

# ------ Test 06: Two parallel paths, choose the one with higher bottleneck ------
test_id += 1
# Path 1: 1->2->4 caps 10, 10 => bottleneck 10
# Path 2: 1->3->4 caps 5, 100 => bottleneck 5
# Best: path 1, bottleneck=10, trips = ceil(99/9) = 11
scenarios = [(4, [(1,2,10),(2,4,10),(1,3,5),(3,4,100)], 1, 4, 99)]
write_test(test_id, scenarios)

# ------ Test 07: Multiple scenarios in one test case ------
test_id += 1
scenarios = [
    (3, [(1,2,5),(2,3,10),(1,3,3)], 1, 3, 20),  # path 1-2-3 bottleneck=5, trips=ceil(20/4)=5
    (4, [(1,2,100),(2,3,50),(3,4,25)], 1, 4, 100),  # bottleneck=25, trips=ceil(100/24)=5
    (2, [(1,2,2)], 1, 2, 1),  # bottleneck=2, trips=1
]
write_test(test_id, scenarios)

# ------ Test 08: Star graph ------
test_id += 1
# Center node 1, connected to 2,3,4,5 with different capacities
# Want to go from 2 to 5: must go through center
# Path: 2->1->5, bottleneck = min(cap(2,1), cap(1,5))
scenarios = [(5, [(1,2,20),(1,3,15),(1,4,30),(1,5,10)], 2, 5, 99)]
# bottleneck of 2->1->5 = min(20,10) = 10, trips = ceil(99/9) = 11
write_test(test_id, scenarios)

# ------ Test 09: Complete graph K5 ------
test_id += 1
edges = []
caps = {}
nodes = range(1, 6)
for i in nodes:
    for j in nodes:
        if i < j:
            c = random.randint(2, 50)
            edges.append((i, j, c))
            caps[(i,j)] = c
scenarios = [(5, edges, 1, 5, 200)]
write_test(test_id, scenarios)

# ------ Test 10: Large T value ------
test_id += 1
# bottleneck path capacity = 100, trips = ceil(1000000 / 99)
scenarios = [(3, [(1,2,100),(2,3,100)], 1, 3, 1000000)]
write_test(test_id, scenarios)

# ------ Test 11: T = 1 (single tourist) ------
test_id += 1
scenarios = [(3, [(1,2,50),(2,3,30),(1,3,20)], 1, 3, 1)]
write_test(test_id, scenarios)

# ------ Test 12: All edges same capacity ------
test_id += 1
# All caps = 5, so bottleneck = 5, trips = ceil(T/4)
scenarios = [(4, [(1,2,5),(2,3,5),(3,4,5),(1,3,5),(2,4,5),(1,4,5)], 1, 4, 17)]
# ceil(17/4) = 5
write_test(test_id, scenarios)

# ------ Test 13: Medium random graph ------
test_id += 1
random.seed(42)
N = 50
R = 150
edges = gen_random_connected_graph(N, R, 2, 100)
S, D = 1, N
T = 500
scenarios = [(N, edges, S, D, T)]
write_test(test_id, scenarios)

# ------ Test 14: Larger random graph ------
test_id += 1
random.seed(123)
N = 100
R = 500
edges = gen_random_connected_graph(N, R, 2, 1000)
S, D = 1, N
T = 99999
scenarios = [(N, edges, S, D, T)]
write_test(test_id, scenarios)

# ------ Test 15: Graph where direct edge is NOT the best path ------
test_id += 1
# Direct 1->4 has cap 3, but 1->2->3->4 has bottleneck min(10,10,10)=10
scenarios = [(4, [(1,4,3),(1,2,10),(2,3,10),(3,4,10)], 1, 4, 27)]
# bottleneck=10, trips=ceil(27/9)=3
write_test(test_id, scenarios)

# ------ Test 16: Trips exactly divide ------
test_id += 1
# bottleneck = 11, per trip = 10, T=30, trips=3 exactly
scenarios = [(2, [(1,2,11)], 1, 2, 30)]
write_test(test_id, scenarios)

# ------ Test 17: Trips with remainder 1 ------
test_id += 1
# bottleneck = 11, per trip = 10, T=31, trips=ceil(31/10)=4
scenarios = [(2, [(1,2,11)], 1, 2, 31)]
write_test(test_id, scenarios)

# ------ Test 18: Multiple scenarios, varied sizes ------
test_id += 1
random.seed(777)
scenarios = []
for _ in range(5):
    N = random.randint(3, 20)
    R = random.randint(N - 1, min(N * (N - 1) // 2, N + 10))
    edges = gen_random_connected_graph(N, R, 2, 50)
    S = 1
    D = N
    T = random.randint(1, 10000)
    scenarios.append((N, edges, S, D, T))
write_test(test_id, scenarios)

# ------ Test 19: Large graph stress test ------
test_id += 1
random.seed(999)
N = 200
R = 1000
edges = gen_random_connected_graph(N, R, 2, 500)
S, D = 1, N
T = 999999
scenarios = [(N, edges, S, D, T)]
write_test(test_id, scenarios)

# ------ Test 20: S == D (source equals destination, T tourists, 0 trips needed?) ------
# Actually, the problem says "from one city to another", but let's test S != D edge.
# Instead: long chain with very small capacity
test_id += 1
N = 10
edges = [(i, i+1, 2) for i in range(1, N)]
# All caps = 2, bottleneck = 2, per trip = 1
# T = 999, trips = 999
scenarios = [(N, edges, 1, N, 999)]
write_test(test_id, scenarios)

print(f"\nGenerated {test_id} test cases.")
