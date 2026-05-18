import sys
import math

def solve():
    data = sys.stdin.read().split('\n')
    idx = 0
    # Number of test cases
    while idx < len(data) and data[idx].strip() == '':
        idx += 1
    T = int(data[idx].strip())
    idx += 1

    results = []
    for t in range(T):
        # Skip blank lines
        while idx < len(data) and data[idx].strip() == '':
            idx += 1

        # Hangar coordinates (not needed for computation)
        parts = data[idx].strip().split()
        idx += 1

        total_length = 0.0
        while idx < len(data) and data[idx].strip() != '':
            parts = data[idx].strip().split()
            if len(parts) == 4:
                x1, y1, x2, y2 = map(int, parts)
                length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                total_length += length
            idx += 1

        # Each road has 2 lanes, plow at 20 km/h
        plow_dist_km = 2 * total_length / 1000.0
        time_hours = plow_dist_km / 20.0
        hours = int(time_hours)
        minutes = round((time_hours - hours) * 60)
        if minutes == 60:
            hours += 1
            minutes = 0
        results.append(f"{hours}:{minutes:02d}")

    print('\n\n'.join(results))

solve()
