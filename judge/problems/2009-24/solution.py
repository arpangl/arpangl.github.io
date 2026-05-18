import sys
from math import gcd

def solve(points):
    """
    Given a list of (x, y) points, count the number of unique lines
    determined by every pair of points.

    A line is represented by a canonical form (a, b, c) where ax + by + c = 0.
    We normalize so that:
      - gcd(|a|, |b|, |c|) = 1
      - The leading nonzero coefficient is positive.
    """
    n = len(points)
    if n < 2:
        return 0

    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            # Line through (x1,y1) and (x2,y2):
            # a = y2 - y1, b = x1 - x2, c = x2*y1 - x1*y2
            a = y2 - y1
            b = x1 - x2
            c = x2 * y1 - x1 * y2

            # Normalize: divide by gcd, make leading nonzero positive
            g = gcd(gcd(abs(a), abs(b)), abs(c))
            if g != 0:
                a //= g
                b //= g
                c //= g

            # Make leading nonzero coefficient positive
            if a < 0 or (a == 0 and b < 0) or (a == 0 and b == 0 and c < 0):
                a, b, c = -a, -b, -c

            lines.add((a, b, c))

    return len(lines)


def solve_input(input_text):
    lines = input_text.strip().split('\n')
    t = int(lines[0].strip())
    results = []
    for i in range(1, t + 1):
        tokens = list(map(int, lines[i].strip().split()))
        n = tokens[0]
        points = []
        for j in range(n):
            x = tokens[1 + 2 * j]
            y = tokens[2 + 2 * j]
            points.append((x, y))
        results.append(str(solve(points)))
    return '\n'.join(results)


if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve_input(input_text))
