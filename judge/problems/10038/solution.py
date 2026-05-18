import sys
from collections import defaultdict

def solve():
    n = int(input())
    # Build a trie structure
    # Each node is a dict of children
    root = {}

    for _ in range(n):
        path = input().strip()
        parts = path.split('\\')
        node = root
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]

    # Print the tree
    result = []

    def dfs(node, depth):
        for name in sorted(node.keys()):
            result.append(' ' * depth + name)
            dfs(node[name], depth + 1)

    dfs(root, 0)
    print('\n'.join(result))

solve()
