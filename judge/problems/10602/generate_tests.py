#!/usr/bin/env python3
"""
Generate test cases for Problem 10602: Longest Paths
DAG longest path from a given starting node.
n up to 100, graph is a DAG (no cycles), edges are directed.
"""

import random
import os
import sys

# We'll generate each test case as a list of "sub-cases" (each file can have multiple cases ending with 0).

def make_case(n, s, edges):
    """Return lines for one case (without trailing 0 for end-of-input)."""
    lines = [str(n), str(s)]
    for p, q in edges:
        lines.append(f"{p} {q}")
    lines.append("0 0")
    return lines


def generate_all_tests():
    tests = []

    # ===================== Test 01: Sample input =====================
    lines = []
    # Case 1: simple 2-node
    lines += make_case(2, 1, [(1, 2)])
    # Case 2: 5-node
    lines += make_case(5, 3, [(1, 2), (3, 5), (3, 1), (2, 4), (4, 5)])
    # Case 3: 5-node starting at 5
    lines += make_case(5, 5, [(5, 1), (5, 2), (5, 3), (5, 4), (4, 1), (4, 2)])
    lines.append("0")
    tests.append(("01", '\n'.join(lines)))

    # ===================== Test 02: Minimal - 2 nodes, no edges from start =====================
    lines = []
    lines += make_case(2, 2, [(1, 2)])  # start at 2, no outgoing edges from 2
    lines.append("0")
    tests.append(("02", '\n'.join(lines)))

    # ===================== Test 03: Single edge, start has no outgoing =====================
    lines = []
    lines += make_case(2, 1, [(1, 2)])
    lines += make_case(3, 2, [(1, 2), (1, 3)])  # start at 2, no outgoing from 2
    lines.append("0")
    tests.append(("03", '\n'.join(lines)))

    # ===================== Test 04: Linear chain (longest path = n-1) =====================
    lines = []
    n = 10
    edges = [(i, i+1) for i in range(1, n)]
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("04", '\n'.join(lines)))

    # ===================== Test 05: Linear chain reversed order, start at end =====================
    lines = []
    n = 10
    edges = [(i, i+1) for i in range(1, n)]
    lines += make_case(n, n, edges)  # start at node n, which has no outgoing
    lines.append("0")
    tests.append(("05", '\n'.join(lines)))

    # ===================== Test 06: Star graph - one center, many leaves =====================
    lines = []
    n = 20
    edges = [(1, i) for i in range(2, n+1)]
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("06", '\n'.join(lines)))

    # ===================== Test 07: Binary tree-like DAG =====================
    lines = []
    n = 15
    edges = []
    for i in range(1, n+1):
        if 2*i <= n:
            edges.append((i, 2*i))
        if 2*i+1 <= n:
            edges.append((i, 2*i+1))
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("07", '\n'.join(lines)))

    # ===================== Test 08: Tie-breaking - multiple paths same length =====================
    # Diamond: 1->2, 1->3, 2->4, 3->4. Start at 1. Both paths length 2, end at 4.
    lines = []
    lines += make_case(4, 1, [(1, 2), (1, 3), (2, 4), (3, 4)])
    # Another: 1->2, 1->3, 2->5, 3->4. Both length 2. End at 4 < 5, so answer should be 4.
    lines += make_case(5, 1, [(1, 2), (1, 3), (2, 5), (3, 4)])
    lines.append("0")
    tests.append(("08", '\n'.join(lines)))

    # ===================== Test 09: Disconnected - start node isolated =====================
    lines = []
    # Node 3 has no outgoing edges and the graph has other edges
    lines += make_case(5, 3, [(1, 2), (2, 4), (4, 5)])
    lines.append("0")
    tests.append(("09", '\n'.join(lines)))

    # ===================== Test 10: Large linear chain n=100 =====================
    lines = []
    n = 100
    edges = [(i, i+1) for i in range(1, n)]
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("10", '\n'.join(lines)))

    # ===================== Test 11: Large dense DAG n=100 =====================
    lines = []
    n = 100
    edges = []
    for i in range(1, n+1):
        for j in range(i+1, min(i+6, n+1)):  # each node connects to next 5
            edges.append((i, j))
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("11", '\n'.join(lines)))

    # ===================== Test 12: Multiple cases in one input, various sizes =====================
    lines = []
    # Case a: n=3, chain
    lines += make_case(3, 1, [(1, 2), (2, 3)])
    # Case b: n=4, fork
    lines += make_case(4, 1, [(1, 2), (1, 3), (3, 4)])
    # Case c: n=6
    lines += make_case(6, 2, [(2, 3), (3, 4), (4, 5), (2, 6), (6, 5)])
    lines.append("0")
    tests.append(("12", '\n'.join(lines)))

    # ===================== Test 13: Tie-breaking with many equal-length paths =====================
    lines = []
    # 1 -> 2,3,4,5,6. All leaves. Length 1. Smallest end = 2.
    n = 6
    edges = [(1, i) for i in range(2, 7)]
    lines += make_case(n, 1, edges)
    # Also: 1->2->7, 1->3->8, 1->4->9, 1->5->10, 1->6->11. All length 2. Smallest end = 7.
    n = 11
    edges = [(1, i) for i in range(2, 7)]
    edges += [(2, 7), (3, 8), (4, 9), (5, 10), (6, 11)]
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("13", '\n'.join(lines)))

    # ===================== Test 14: Start not at node 1, complex DAG =====================
    lines = []
    n = 8
    edges = [
        (5, 1), (5, 2), (5, 6),
        (6, 7), (7, 8),
        (2, 3), (3, 4),
        (1, 4),
    ]
    lines += make_case(n, 5, edges)
    lines.append("0")
    tests.append(("14", '\n'.join(lines)))

    # ===================== Test 15: Random DAG n=50 =====================
    random.seed(42)
    lines = []
    n = 50
    edges = set()
    # Generate a random DAG: for each pair i < j, add edge with some probability
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if random.random() < 0.08:
                edges.add((i, j))
    # Ensure at least some edges from node 1
    edges.add((1, 2))
    edges.add((2, 10))
    lines += make_case(n, 1, sorted(edges))
    lines.append("0")
    tests.append(("15", '\n'.join(lines)))

    # ===================== Test 16: Random DAG n=100 with higher density =====================
    random.seed(123)
    lines = []
    n = 100
    edges = set()
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if random.random() < 0.05:
                edges.add((i, j))
    lines += make_case(n, 1, sorted(edges))
    lines.append("0")
    tests.append(("16", '\n'.join(lines)))

    # ===================== Test 17: Two nodes, start=2, edge 2->1 =====================
    lines = []
    lines += make_case(2, 2, [(2, 1)])
    lines.append("0")
    tests.append(("17", '\n'.join(lines)))

    # ===================== Test 18: Wide DAG - many parallel paths of different lengths =====================
    lines = []
    n = 20
    edges = [
        (1, 2), (2, 3), (3, 4), (4, 5),         # path of length 4 ending at 5
        (1, 6), (6, 7), (7, 8),                   # path of length 3 ending at 8
        (1, 9), (9, 10), (10, 11), (11, 12), (12, 13),  # path of length 5 ending at 13
        (1, 14), (14, 15),                         # path of length 2 ending at 15
        (1, 16),                                   # path of length 1 ending at 16
        (13, 17), (17, 18), (18, 19), (19, 20),   # extends longest path
    ]
    lines += make_case(n, 1, edges)
    lines.append("0")
    tests.append(("18", '\n'.join(lines)))

    # ===================== Test 19: Multiple cases, start at different nodes =====================
    lines = []
    n = 7
    edges = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(1,7)]
    lines += make_case(n, 1, edges)
    lines += make_case(n, 4, edges)
    lines += make_case(n, 7, edges)  # node 7 has no outgoing
    lines.append("0")
    tests.append(("19", '\n'.join(lines)))

    # ===================== Test 20: Larger random DAG, start in middle =====================
    random.seed(999)
    lines = []
    n = 80
    edges = set()
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if random.random() < 0.04:
                edges.add((i, j))
    s = 30  # start from middle
    lines += make_case(n, s, sorted(edges))
    lines.append("0")
    tests.append(("20", '\n'.join(lines)))

    return tests


def main():
    base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10602/testcases"
    os.makedirs(base_dir, exist_ok=True)

    tests = generate_all_tests()

    # Import solver
    sys.path.insert(0, "/Users/lambert/Documents/GPE-Helper/judge/problems/10602")
    from solve import solve

    for test_id, input_data in tests:
        in_path = os.path.join(base_dir, f"{test_id}.in")
        out_path = os.path.join(base_dir, f"{test_id}.out")

        # Write input
        with open(in_path, 'w') as f:
            f.write(input_data + '\n')

        # Compute output
        output = solve(input_data)

        # Write output
        with open(out_path, 'w') as f:
            f.write(output + '\n')

        print(f"Test {test_id}: generated ({in_path})")

    print(f"\nTotal: {len(tests)} test cases generated.")


if __name__ == '__main__':
    main()
