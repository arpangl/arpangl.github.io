import random
import os
from math import gcd

def solve(points):
    n = len(points)
    if n < 2:
        return 0
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            a = y2 - y1
            b = x1 - x2
            c = x2 * y1 - x1 * y2
            g = gcd(gcd(abs(a), abs(b)), abs(c))
            if g != 0:
                a //= g
                b //= g
                c //= g
            if a < 0 or (a == 0 and b < 0) or (a == 0 and b == 0 and c < 0):
                a, b, c = -a, -b, -c
            lines.add((a, b, c))
    return len(lines)


def format_testcase(cases):
    """cases is a list of point-lists. Returns (input_str, output_str)."""
    inp_lines = [str(len(cases))]
    out_lines = []
    for points in cases:
        tokens = [str(len(points))]
        for x, y in points:
            tokens.append(str(x))
            tokens.append(str(y))
        inp_lines.append(' '.join(tokens))
        out_lines.append(str(solve(points)))
    return '\n'.join(inp_lines) + '\n', '\n'.join(out_lines) + '\n'


def write_test(idx, cases, outdir):
    inp, out = format_testcase(cases)
    with open(os.path.join(outdir, f'{idx:02d}.in'), 'w') as f:
        f.write(inp)
    with open(os.path.join(outdir, f'{idx:02d}.out'), 'w') as f:
        f.write(out)
    # Print summary
    print(f"Test {idx:02d}: {len(cases)} case(s)")
    for i, points in enumerate(cases):
        print(f"  Case {i+1}: {len(points)} points -> {solve(points)} unique lines")


def gen_random_points(n, lo=-1000, hi=1000):
    """Generate n distinct random points."""
    pts = set()
    while len(pts) < n:
        pts.add((random.randint(lo, hi), random.randint(lo, hi)))
    return list(pts)


def gen_collinear_points(n, dx=1, dy=1, x0=0, y0=0):
    """Generate n collinear points."""
    pts = []
    for i in range(n):
        pts.append((x0 + i * dx, y0 + i * dy))
    return pts


outdir = '/Users/lambert/Documents/GPE-Helper/judge/problems/2009-24/testcases'
os.makedirs(outdir, exist_ok=True)

random.seed(42)
test_idx = 1

# --- Test 1: Sample test case ---
write_test(test_idx, [
    [(0,0),(1,1),(2,2),(3,3),(4,4),(6,6),(0,3)],
    [(0,0),(1,1),(1,-1),(-1,1),(-1,-1)],
], outdir)
test_idx += 1

# --- Test 2: Minimum - 2 points (one line) ---
write_test(test_idx, [
    [(0,0),(1,1)],
], outdir)
test_idx += 1

# --- Test 3: 3 collinear points -> 1 line ---
write_test(test_idx, [
    [(0,0),(1,1),(2,2)],
], outdir)
test_idx += 1

# --- Test 4: 3 non-collinear points -> 3 lines ---
write_test(test_idx, [
    [(0,0),(1,0),(0,1)],
], outdir)
test_idx += 1

# --- Test 5: All points on x-axis (horizontal line) ---
write_test(test_idx, [
    [(i, 0) for i in range(10)],
], outdir)
test_idx += 1

# --- Test 6: All points on y-axis (vertical line) ---
write_test(test_idx, [
    [(0, i) for i in range(10)],
], outdir)
test_idx += 1

# --- Test 7: Points on a grid - many collinear lines ---
# 4x4 grid
grid_pts = [(i, j) for i in range(4) for j in range(4)]
write_test(test_idx, [grid_pts], outdir)
test_idx += 1

# --- Test 8: Points forming a square + center ---
write_test(test_idx, [
    [(0,0),(10,0),(10,10),(0,10),(5,5)],
], outdir)
test_idx += 1

# --- Test 9: Large collinear set - all on y=2x+3 ---
write_test(test_idx, [
    [(i, 2*i+3) for i in range(50)],
], outdir)
test_idx += 1

# --- Test 10: Two sets of collinear points (two parallel lines) ---
write_test(test_idx, [
    [(i, 0) for i in range(5)] + [(i, 1) for i in range(5)],
], outdir)
test_idx += 1

# --- Test 11: Star pattern - points at angles from center ---
# Center + points on axes and diagonals
write_test(test_idx, [
    [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1),
     (2,0),(-2,0),(0,2),(0,-2),(2,2),(-2,-2),(2,-2),(-2,2)],
], outdir)
test_idx += 1

# --- Test 12: Random 20 points ---
write_test(test_idx, [gen_random_points(20)], outdir)
test_idx += 1

# --- Test 13: Random 50 points ---
write_test(test_idx, [gen_random_points(50)], outdir)
test_idx += 1

# --- Test 14: Near-max N=99 random points ---
write_test(test_idx, [gen_random_points(99)], outdir)
test_idx += 1

# --- Test 15: Multiple test cases in one input ---
write_test(test_idx, [
    [(0,0),(1,0)],                       # 1 line
    [(0,0),(1,0),(0,1)],                 # 3 lines
    [(0,0),(1,1),(2,2),(3,3)],           # 1 line
    [(0,0),(1,0),(0,1),(1,1)],           # 6 lines (square corners)
], outdir)
test_idx += 1

# --- Test 16: Negative coordinates ---
write_test(test_idx, [
    [(-5,-5),(-3,-3),(-1,-1),(1,1),(3,3),(5,5),(-5,5)],
], outdir)
test_idx += 1

# --- Test 17: Large coordinate values ---
write_test(test_idx, [
    [(1000,1000),(-1000,-1000),(1000,-1000),(-1000,1000),(0,0)],
], outdir)
test_idx += 1

# --- Test 18: 5x5 grid (25 points, many collinearities) ---
grid5 = [(i, j) for i in range(5) for j in range(5)]
write_test(test_idx, [grid5], outdir)
test_idx += 1

# --- Test 19: Multiple large random cases ---
write_test(test_idx, [
    gen_random_points(80, -500, 500),
    gen_random_points(90, -500, 500),
], outdir)
test_idx += 1

# --- Test 20: Points forming a regular pattern - triangle vertices + edge midpoints + centroid ---
write_test(test_idx, [
    [(0,0),(6,0),(3,6),(3,0),(0,3),(3,3),(2,2)],  # not exact midpoints, just interesting geometry
], outdir)
test_idx += 1

print(f"\nGenerated {test_idx - 1} test cases.")
