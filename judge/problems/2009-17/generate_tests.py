#!/usr/bin/env python3
"""
Generate test cases for 2009-17: Binary tree traversals.

Generates 18 test cases covering:
- Single node
- Two nodes (left child only, right child only)
- Left-skewed tree (all left children)
- Right-skewed tree (all right children)
- Complete/full binary trees
- Perfect binary tree
- Random trees of various sizes
- Maximum size (n=26)
- Zigzag (alternating left-right) trees
- Sample from problem statement
- Multiple test cases in one input
"""

import random
import os

random.seed(42)

def build_postorder(preorder, inorder):
    if not preorder:
        return []
    root = preorder[0]
    root_idx = inorder.index(root)
    left_inorder = inorder[:root_idx]
    right_inorder = inorder[root_idx + 1:]
    left_size = len(left_inorder)
    left_preorder = preorder[1:1 + left_size]
    right_preorder = preorder[1 + left_size:]
    left_post = build_postorder(left_preorder, left_inorder)
    right_post = build_postorder(right_preorder, right_inorder)
    return left_post + right_post + [root]


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def preorder_trav(node):
    if not node:
        return []
    return [node.val] + preorder_trav(node.left) + preorder_trav(node.right)


def inorder_trav(node):
    if not node:
        return []
    return inorder_trav(node.left) + [node.val] + inorder_trav(node.right)


def postorder_trav(node):
    if not node:
        return []
    return postorder_trav(node.left) + postorder_trav(node.right) + [node.val]


def build_left_skewed(labels):
    """All nodes are left children."""
    if not labels:
        return None
    root = TreeNode(labels[0])
    cur = root
    for i in range(1, len(labels)):
        cur.left = TreeNode(labels[i])
        cur = cur.left
    return root


def build_right_skewed(labels):
    """All nodes are right children."""
    if not labels:
        return None
    root = TreeNode(labels[0])
    cur = root
    for i in range(1, len(labels)):
        cur.right = TreeNode(labels[i])
        cur = cur.right
    return root


def build_zigzag(labels):
    """Alternating left-right children."""
    if not labels:
        return None
    root = TreeNode(labels[0])
    cur = root
    for i in range(1, len(labels)):
        if i % 2 == 1:
            cur.left = TreeNode(labels[i])
            cur = cur.left
        else:
            cur.right = TreeNode(labels[i])
            cur = cur.right
    return root


def build_complete_tree(labels):
    """Build a complete binary tree (level order)."""
    if not labels:
        return None
    nodes = [TreeNode(l) for l in labels]
    for i in range(len(nodes)):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < len(nodes):
            nodes[i].left = nodes[left_idx]
        if right_idx < len(nodes):
            nodes[i].right = nodes[right_idx]
    return nodes[0]


def build_random_tree(labels):
    """Insert labels one by one into random positions."""
    if not labels:
        return None
    root = TreeNode(labels[0])
    for i in range(1, len(labels)):
        node = root
        while True:
            if random.random() < 0.5:
                if node.left is None:
                    node.left = TreeNode(labels[i])
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(labels[i])
                    break
                node = node.right
    return root


def tree_to_case(tree):
    """Return (n, preorder_str, inorder_str, postorder_str)."""
    pre = preorder_trav(tree)
    ino = inorder_trav(tree)
    post = postorder_trav(tree)
    n = len(pre)
    return (n, ' '.join(pre), ' '.join(ino), ' '.join(post))


def make_case_from_tree(tree):
    n, pre_s, ino_s, post_s = tree_to_case(tree)
    # Verify with solution
    pre_list = pre_s.split()
    ino_list = ino_s.split()
    computed_post = build_postorder(pre_list, ino_list)
    assert ' '.join(computed_post) == post_s, f"Mismatch! Expected {post_s}, got {' '.join(computed_post)}"
    return (n, pre_s, ino_s, post_s)


def write_test(test_num, cases, outdir):
    """Write a single test file. cases = list of (n, pre_str, ino_str, post_str)."""
    in_lines = [str(len(cases))]
    out_lines = []
    for (n, pre_s, ino_s, post_s) in cases:
        in_lines.append(str(n))
        in_lines.append(pre_s)
        in_lines.append(ino_s)
        out_lines.append(post_s)

    in_path = os.path.join(outdir, f"{test_num:02d}.in")
    out_path = os.path.join(outdir, f"{test_num:02d}.out")
    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')


def main():
    outdir = '/Users/lambert/Documents/GPE-Helper/judge/problems/2009-17/testcases'
    os.makedirs(outdir, exist_ok=True)

    ALL_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    test_num = 0

    # ---- Test 01: Sample from problem statement ----
    test_num += 1
    cases = [
        (7, 'A B D E F C G', 'D B F E A G C', 'D F E B G C A'),
        (12, 'A B C D E F G H I J K L', 'L K J I H G F E D C B A', 'L K J I H G F E D C B A'),
        (17, 'Z A G H U Y B T F D W X C R S E V', 'A G H U Z T W D F B Y C R S V E X', 'U H G A W D F T B V E S R C X Y Z'),
    ]
    # Verify sample cases
    for (n, pre_s, ino_s, post_s) in cases:
        computed = build_postorder(pre_s.split(), ino_s.split())
        assert ' '.join(computed) == post_s
    write_test(test_num, cases, outdir)

    # ---- Test 02: Single node ----
    test_num += 1
    tree = TreeNode('A')
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 03: Two nodes, left child only ----
    test_num += 1
    tree = TreeNode('A')
    tree.left = TreeNode('B')
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 04: Two nodes, right child only ----
    test_num += 1
    tree = TreeNode('A')
    tree.right = TreeNode('B')
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 05: Three nodes - root with both children ----
    test_num += 1
    tree = TreeNode('A')
    tree.left = TreeNode('B')
    tree.right = TreeNode('C')
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 06: Left-skewed tree n=5 ----
    test_num += 1
    tree = build_left_skewed(ALL_LETTERS[:5])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 07: Right-skewed tree n=5 ----
    test_num += 1
    tree = build_right_skewed(ALL_LETTERS[:5])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 08: Left-skewed tree n=26 (maximum) ----
    test_num += 1
    tree = build_left_skewed(ALL_LETTERS[:26])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 09: Right-skewed tree n=26 (maximum) ----
    test_num += 1
    tree = build_right_skewed(ALL_LETTERS[:26])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 10: Zigzag tree n=6 ----
    test_num += 1
    tree = build_zigzag(ALL_LETTERS[:6])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 11: Complete binary tree n=7 (perfect) ----
    test_num += 1
    tree = build_complete_tree(ALL_LETTERS[:7])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 12: Complete binary tree n=15 (perfect, 4 levels) ----
    test_num += 1
    tree = build_complete_tree(ALL_LETTERS[:15])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 13: Complete binary tree n=10 (not perfect) ----
    test_num += 1
    tree = build_complete_tree(ALL_LETTERS[:10])
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 14: Random tree n=26 (max) ----
    test_num += 1
    labels = ALL_LETTERS[:]
    random.shuffle(labels)
    tree = build_random_tree(labels)
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 15: Random tree n=20 ----
    test_num += 1
    labels = ALL_LETTERS[:20]
    random.shuffle(labels)
    tree = build_random_tree(labels)
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 16: Zigzag tree n=26 (max) ----
    test_num += 1
    labels = ALL_LETTERS[:]
    random.shuffle(labels)
    tree = build_zigzag(labels)
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    # ---- Test 17: Multiple small test cases in one file ----
    test_num += 1
    multi_cases = []
    # Single node Z
    t = TreeNode('Z')
    multi_cases.append(make_case_from_tree(t))
    # 3-node left chain
    t = build_left_skewed(['X', 'Y', 'Z'])
    multi_cases.append(make_case_from_tree(t))
    # 3-node right chain
    t = build_right_skewed(['P', 'Q', 'R'])
    multi_cases.append(make_case_from_tree(t))
    # Complete 7
    t = build_complete_tree(['M', 'N', 'O', 'P', 'Q', 'R', 'S'])
    multi_cases.append(make_case_from_tree(t))
    # Random 10
    lbl = ALL_LETTERS[:10]
    random.shuffle(lbl)
    t = build_random_tree(lbl)
    multi_cases.append(make_case_from_tree(t))
    write_test(test_num, multi_cases, outdir)

    # ---- Test 18: Another random tree n=26 (different shape) ----
    test_num += 1
    labels = ALL_LETTERS[:]
    random.shuffle(labels)
    tree = build_random_tree(labels)
    cases = [make_case_from_tree(tree)]
    write_test(test_num, cases, outdir)

    print(f"Generated {test_num} test cases in {outdir}")


if __name__ == '__main__':
    main()
