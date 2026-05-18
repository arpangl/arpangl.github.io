import sys

def solve(segments):
    """
    Given a list of (left, right) segments, compute the sum of overlap lengths
    over all pairs (i, j) where i < j.

    Approach (O(n log n)):
    For each pair of segments [a,b] and [c,d], the overlap is max(0, min(b,d) - max(a,c)).

    We can compute the total pairwise overlap using a sweep line / event-based approach:

    Sort all endpoints. Use events: +1 at left endpoint, -1 at right endpoint.
    As we sweep, if the current "coverage count" is k, then there are C(k,2) = k*(k-1)/2
    pairs overlapping in this interval. Multiply by the interval length.

    But we must be careful: we need the sum of pairwise overlaps, not just the union.

    Sweep line approach:
    - Create events: for each segment [l, r], add (l, +1) and (r, -1).
    - Sort events by x-coordinate. For ties, process +1 before -1 (opening before closing).
    - Sweep from left to right. Between consecutive x-values, if coverage count is k,
      add k*(k-1)//2 * (x_next - x_curr) to the answer.
    """
    if len(segments) <= 1:
        return 0

    events = []
    for l, r in segments:
        if l > r:
            l, r = r, l
        events.append((l, 0))   # 0 = open (process first)
        events.append((r, 1))   # 1 = close (process second)

    # Sort by x, then by type (open before close at same x)
    events.sort()

    total = 0
    count = 0
    prev_x = None

    for x, typ in events:
        if prev_x is not None and x > prev_x and count >= 2:
            total += count * (count - 1) // 2 * (x - prev_x)
        prev_x = x
        if typ == 0:
            count += 1
        else:
            count -= 1

    return total


def brute_force(segments):
    """O(n^2) brute force for verification."""
    total = 0
    n = len(segments)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = segments[i]
            c, d = segments[j]
            if a > b:
                a, b = b, a
            if c > d:
                c, d = d, c
            overlap = max(0, min(b, d) - max(a, c))
            total += overlap
    return total


def read_and_solve(input_text):
    lines = input_text.strip().split('\n')
    segments = []
    for line in lines:
        line = line.strip()
        if line == '.':
            break
        parts = line.split()
        if len(parts) >= 2:
            segments.append((int(parts[0]), int(parts[1])))
    return solve(segments)


if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(read_and_solve(input_text))
