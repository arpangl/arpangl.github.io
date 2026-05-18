import sys

def build_spiral(max_n):
    """Build mapping from Willi's number to Maja's (x, y) coordinates."""
    coords = {}
    coords[1] = (0, 0)
    if max_n <= 1:
        return coords

    # 6 hex directions for ring traversal (counterclockwise)
    dirs = [(-1, 1), (-1, 0), (0, -1), (1, -1), (1, 0), (0, 1)]

    x, y = 0, 0
    n = 2

    for ring in range(1, max_n):  # ring number
        # Transition step to start of this ring: move (0, 1)
        x, y = x, y + 1
        coords[n] = (x, y)
        n += 1
        if n > max_n:
            return coords

        # Traverse 6 sides of the hexagonal ring
        for side in range(6):
            steps = ring - 1 if side == 0 else ring
            dx, dy = dirs[side]
            for _ in range(steps):
                x, y = x + dx, y + dy
                coords[n] = (x, y)
                n += 1
                if n > max_n:
                    return coords

    return coords


def solve(input_text):
    """Solve the problem: convert Willi numbers to Maja coordinates."""
    lines = input_text.strip().split('\n')
    numbers = [int(line.strip()) for line in lines if line.strip()]

    max_n = max(numbers) if numbers else 0
    coords = build_spiral(max_n)

    results = []
    for n in numbers:
        x, y = coords[n]
        results.append(f"{x} {y}")
    return '\n'.join(results)


if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text))
