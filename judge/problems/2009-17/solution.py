import sys

def build_postorder(preorder, inorder):
    """Given preorder and inorder lists, return postorder list."""
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

def solve(input_text):
    lines = input_text.strip().split('\n')
    idx = 0
    m = int(lines[idx]); idx += 1
    results = []
    for _ in range(m):
        n = int(lines[idx]); idx += 1
        preorder = lines[idx].split(); idx += 1
        inorder = lines[idx].split(); idx += 1
        postorder = build_postorder(preorder, inorder)
        results.append(' '.join(postorder))
    return '\n'.join(results) + '\n'

if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text), end='')
