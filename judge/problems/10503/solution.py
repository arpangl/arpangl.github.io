import sys
import re

def parse_sequence(expr, pos):
    """
    Parse a sequence expression starting at position pos.
    Returns (sequence_function, new_pos)
    where sequence_function takes N and returns a list of N terms.
    """
    # Expect '['
    assert expr[pos] == '[', f"Expected '[' at pos {pos}, got '{expr[pos]}'"
    pos += 1  # skip '['

    # Read the number m (possibly negative)
    num_str = ""
    if expr[pos] == '-' or expr[pos].isdigit():
        if expr[pos] == '-':
            num_str += '-'
            pos += 1
        while pos < len(expr) and expr[pos].isdigit():
            num_str += expr[pos]
            pos += 1
    m = int(num_str)

    # Check what comes next: ']', '+', or '*'
    if expr[pos] == ']':
        # Constant sequence [n]
        pos += 1  # skip ']'
        def const_seq(n, val=m):
            return [val] * n
        return const_seq, pos
    elif expr[pos] == '+':
        pos += 1  # skip '+'
        inner_seq_func, pos = parse_sequence(expr, pos)
        assert expr[pos] == ']', f"Expected ']' at pos {pos}"
        pos += 1  # skip ']'

        def add_seq(n, m_val=m, inner=inner_seq_func):
            s = inner(n)  # we need n terms of inner (indices 1..n, but we use 0..n-1)
            v = [0] * n
            v[0] = m_val
            for i in range(1, n):
                v[i] = v[i-1] + s[i-1]
            return v
        return add_seq, pos
    elif expr[pos] == '*':
        pos += 1  # skip '*'
        inner_seq_func, pos = parse_sequence(expr, pos)
        assert expr[pos] == ']', f"Expected ']' at pos {pos}"
        pos += 1  # skip ']'

        def mul_seq(n, m_val=m, inner=inner_seq_func):
            s = inner(n)
            v = [0] * n
            v[0] = m_val * s[0]
            for i in range(1, n):
                v[i] = v[i-1] * s[i]
            return v
        return mul_seq, pos
    else:
        raise ValueError(f"Unexpected character '{expr[pos]}' at pos {pos}")


def solve(line):
    line = line.strip()
    # Split into codification and N
    # The codification ends at the last ']', then there's a space and N
    last_bracket = line.rfind(']')
    expr = line[:last_bracket+1]
    n = int(line[last_bracket+1:].strip())

    seq_func, end_pos = parse_sequence(expr, 0)
    assert end_pos == len(expr), f"Didn't consume entire expression: ended at {end_pos}, len={len(expr)}"

    terms = seq_func(n)
    return ' '.join(str(t) for t in terms)


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    print(solve(line))
