import math
import os
import json
import random

def solve_testcase(hangar_coords, streets):
    total_length = 0.0
    for x1, y1, x2, y2 in streets:
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        total_length += length

    plow_dist_km = 2 * total_length / 1000.0
    time_hours = plow_dist_km / 20.0
    hours = int(time_hours)
    minutes = round((time_hours - hours) * 60)
    if minutes == 60:
        hours += 1
        minutes = 0
    return f"{hours}:{minutes:02d}"

def format_input(test_cases):
    lines = [str(len(test_cases))]
    for i, (hangar, streets) in enumerate(test_cases):
        lines.append('')
        lines.append(f"{hangar[0]} {hangar[1]}")
        for s in streets:
            lines.append(f"{s[0]} {s[1]} {s[2]} {s[3]}")
    return '\n'.join(lines) + '\n'

def format_output(test_cases):
    results = []
    for hangar, streets in test_cases:
        results.append(solve_testcase(hangar, streets))
    return '\n\n'.join(results) + '\n'

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10732/testcases'
os.makedirs(TESTDIR, exist_ok=True)

all_tests = []

# Case 1: Sample
all_tests.append([
    ((0, 0), [(0, 0, 10000, 10000), (5000, -10000, 5000, 10000), (5000, 10000, 10000, 10000)])
])

# Case 2: Single street
all_tests.append([
    ((0, 0), [(0, 0, 10000, 0)])
])

# Case 3: Single very short street
all_tests.append([
    ((0, 0), [(0, 0, 1, 0)])
])

# Case 4: Two test cases
all_tests.append([
    ((0, 0), [(0, 0, 10000, 0)]),
    ((100, 100), [(0, 0, 3000, 4000)])
])

# Case 5: Grid-like streets
streets = []
for i in range(5):
    streets.append((i*1000, 0, i*1000, 4000))
for j in range(5):
    streets.append((0, j*1000, 4000, j*1000))
all_tests.append([
    ((0, 0), streets)
])

# Case 6: Single diagonal
all_tests.append([
    ((0, 0), [(0, 0, 3000, 4000)])
])

# Case 7: Many parallel streets
streets = []
for i in range(20):
    streets.append((0, i*500, 10000, i*500))
all_tests.append([
    ((0, 0), streets)
])

# Case 8: Star pattern
streets = []
for angle_deg in range(0, 360, 45):
    angle = math.radians(angle_deg)
    x2 = int(5000 * math.cos(angle))
    y2 = int(5000 * math.sin(angle))
    streets.append((0, 0, x2, y2))
all_tests.append([
    ((0, 0), streets)
])

# Case 9: Multiple test cases with varying sizes
tc1 = ((0, 0), [(0, 0, 1000, 0)])
tc2 = ((0, 0), [(0, 0, 1000, 0), (1000, 0, 1000, 1000)])
tc3 = ((0, 0), [(0, 0, 5000, 5000), (5000, 5000, 10000, 5000)])
all_tests.append([tc1, tc2, tc3])

# Case 10: Large coordinates
all_tests.append([
    ((0, 0), [(0, 0, 100000, 100000), (-100000, 0, 100000, 0)])
])

# Case 11: Many streets (near 100)
random.seed(42)
streets = []
for _ in range(80):
    x1 = random.randint(-50000, 50000)
    y1 = random.randint(-50000, 50000)
    x2 = random.randint(-50000, 50000)
    y2 = random.randint(-50000, 50000)
    streets.append((x1, y1, x2, y2))
all_tests.append([
    ((0, 0), streets)
])

# Case 12: Zero-length streets? No, that doesn't make sense. Very small streets.
streets = [(0, 0, 1, 1), (1, 1, 2, 2), (2, 2, 3, 3)]
all_tests.append([
    ((0, 0), streets)
])

# Case 13: Exactly 100 streets
random.seed(123)
streets = []
for _ in range(100):
    x1 = random.randint(-10000, 10000)
    y1 = random.randint(-10000, 10000)
    x2 = random.randint(-10000, 10000)
    y2 = random.randint(-10000, 10000)
    streets.append((x1, y1, x2, y2))
all_tests.append([
    ((5000, 5000), streets)
])

# Case 14: Hangar not at origin
all_tests.append([
    ((9999, 9999), [(0, 0, 10000, 0), (0, 0, 0, 10000)])
])

# Case 15: Multiple test cases
random.seed(999)
tcs = []
for _ in range(5):
    hx, hy = random.randint(-1000, 1000), random.randint(-1000, 1000)
    ns = random.randint(1, 20)
    streets = []
    for _ in range(ns):
        x1 = random.randint(-10000, 10000)
        y1 = random.randint(-10000, 10000)
        x2 = random.randint(-10000, 10000)
        y2 = random.randint(-10000, 10000)
        streets.append((x1, y1, x2, y2))
    tcs.append(((hx, hy), streets))
all_tests.append(tcs)

for i, test_group in enumerate(all_tests):
    inp = format_input(test_group)
    out = format_output(test_group)

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    print(f"Case {i+1:02d}: OK ({len(test_group)} test case(s))")

problem = {
    "pid": "10732",
    "name": "Snow Clearing",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

print("All test cases generated!")
