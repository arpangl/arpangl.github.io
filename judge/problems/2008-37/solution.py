import sys

def solve(line):
    """Evaluate a prefix expression. Returns the integer result or 'illegal'."""
    tokens = line.split()
    if not tokens:
        return "illegal"

    ops = {'+', '-', '*', '/', '%'}
    idx = 0

    def parse():
        nonlocal idx
        if idx >= len(tokens):
            return None  # not enough tokens

        token = tokens[idx]
        idx += 1

        if token in ops:
            left = parse()
            if left is None:
                return None
            right = parse()
            if right is None:
                return None

            if token == '+':
                return left + right
            elif token == '-':
                return left - right
            elif token == '*':
                return left * right
            elif token == '/':
                if right == 0:
                    return None  # division by zero -> illegal
                # Integer division: in C, truncates toward zero
                # Python's // floors, so we need to handle differently
                if (left < 0) ^ (right < 0):
                    return -(abs(left) // abs(right))
                else:
                    return abs(left) // abs(right)
            elif token == '%':
                if right == 0:
                    return None
                # C-style remainder: sign follows dividend
                result = abs(left) % abs(right)
                if left < 0:
                    result = -result
                return result
        else:
            # Should be a positive integer
            try:
                val = int(token)
                return val
            except ValueError:
                return None

    result = parse()

    # Check: result must be valid AND all tokens must be consumed
    if result is None or idx != len(tokens):
        return "illegal"

    return str(result)


def main():
    for line in sys.stdin:
        line = line.strip()
        if line == '.':
            break
        print(solve(line))

if __name__ == '__main__':
    main()
