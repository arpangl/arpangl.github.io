#!/usr/bin/env python3
"""
Generate test cases for problem 10608 - Minimal coverage.

Problem: Given segments [Li, Ri] on the X axis, choose minimal number to cover [0, M].
Constraints: 1 <= M <= 5000, |Li|, |Ri| <= 50000, i <= 100000

IMPORTANT: Segment (0, 0) cannot be used since "0 0" is the terminator.
"""

import random
import os

def solve_case(M, segments):
    """Greedy interval covering of [0, M]. Returns (count, chosen_segments) or (0, [])."""
    segs = segments[:]
    segs.sort(key=lambda x: (x[0], -x[1]))

    chosen = []
    current_end = 0
    i = 0
    n = len(segs)

    while current_end < M:
        best_r = current_end
        best_seg = None

        while i < n and segs[i][0] <= current_end:
            if segs[i][1] > best_r:
                best_r = segs[i][1]
                best_seg = segs[i]
            i += 1

        if best_seg is None or best_r == current_end:
            return (0, [])

        chosen.append(best_seg)
        current_end = best_r

    chosen.sort(key=lambda x: (x[0], -x[1]))
    return (len(chosen), chosen)


def format_input(test_cases):
    """Format multiple test cases into input string."""
    lines = [str(len(test_cases))]
    for i, (M, segs) in enumerate(test_cases):
        lines.append("")  # blank line before each test case
        lines.append(str(M))
        for l, r in segs:
            assert not (l == 0 and r == 0), "Segment (0,0) would be confused with terminator!"
            lines.append(f"{l} {r}")
        lines.append("0 0")
    return '\n'.join(lines) + '\n'


def format_output(results):
    """Format results into output string."""
    parts = []
    for count, chosen in results:
        if count == 0:
            parts.append("0")
        else:
            lines = [str(count)]
            for seg in chosen:
                lines.append(f"{seg[0]} {seg[1]}")
            parts.append('\n'.join(lines))
    return '\n\n'.join(parts) + '\n'


def gen_test(test_id, test_cases):
    """Generate a single test file pair."""
    results = []
    for M, segs in test_cases:
        results.append(solve_case(M, segs))

    inp = format_input(test_cases)
    out = format_output(results)
    return inp, out


def write_test(base_dir, test_id, inp, out):
    fname = f"{test_id:02d}"
    with open(os.path.join(base_dir, f"{fname}.in"), 'w') as f:
        f.write(inp)
    with open(os.path.join(base_dir, f"{fname}.out"), 'w') as f:
        f.write(out)


def rand_segment(lo_l, hi_l, lo_r_offset=0, hi_r_offset=None):
    """Generate a random segment that is NOT (0, 0)."""
    while True:
        l = random.randint(lo_l, hi_l)
        if hi_r_offset is not None:
            r = random.randint(l + lo_r_offset, min(l + hi_r_offset, 50000))
        else:
            r = random.randint(l, 50000)
        if not (l == 0 and r == 0):
            return (l, r)


def main():
    base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10608/testcases"
    os.makedirs(base_dir, exist_ok=True)
    random.seed(42)
    test_id = 1

    # ---- Test 1: Sample test case ----
    cases = [
        (1, [(-1, 0), (-5, -3), (2, 5)]),
        (1, [(-1, 0), (0, 1)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 2: Single segment covers exactly [0, M] ----
    cases = [
        (5, [(0, 5)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 3: Single segment that extends beyond M ----
    cases = [
        (3, [(-2, 10)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 4: Impossible - gap at 0 ----
    cases = [
        (5, [(1, 5), (2, 6)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 5: Impossible - gap in middle ----
    cases = [
        (10, [(0, 3), (5, 10)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 6: Multiple overlapping segments, minimal selection ----
    cases = [
        (10, [(0, 4), (1, 6), (3, 8), (5, 10), (7, 12)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 7: M = 1, minimal ----
    cases = [
        (1, [(0, 1)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 8: All negative segments - impossible ----
    cases = [
        (5, [(-10, -1), (-5, -2), (-3, -1)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 9: Touching segments (end of one = start of next) ----
    cases = [
        (6, [(0, 2), (2, 4), (4, 6)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 10: Many redundant segments ----
    cases = [
        (10, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 10), (8, 10), (9, 10)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 11: Segments with negative starts covering [0, M] ----
    cases = [
        (5, [(-3, 2), (-1, 4), (1, 5), (3, 7)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 12: Large M with unit segments ----
    M = 100
    segs = [(i, i+1) for i in range(M)]
    cases = [(M, segs)]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 13: Multiple test cases, mix of solvable and impossible ----
    cases = [
        (5, [(0, 3), (2, 5)]),
        (5, [(0, 2), (3, 5)]),
        (3, [(-1, 1), (0, 2), (1, 3)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 14: Large random test - solvable ----
    M = 5000
    segs = []
    # Ensure coverage by placing a backbone
    pos = 0
    while pos < M:
        step = random.randint(1, 50)
        segs.append((pos - random.randint(0, 10), pos + step))
        pos += step
    # Add lots of random noise segments (filter out (0,0))
    for _ in range(5000):
        l = random.randint(-50000, 50000)
        r = random.randint(l, min(l + 500, 50000))
        if l == 0 and r == 0:
            r = 1  # avoid terminator
        segs.append((l, r))
    random.shuffle(segs)
    cases = [(M, segs)]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 15: Large random test - impossible ----
    M = 5000
    segs = []
    # Create segments that leave a gap around position 2500
    for _ in range(3000):
        l = random.randint(-50000, 2495)
        r = random.randint(l, min(l + 200, 2498))
        if l == 0 and r == 0:
            r = 1
        segs.append((l, r))
    for _ in range(3000):
        l = random.randint(2502, 50000)
        r = random.randint(l, min(l + 200, 50000))
        segs.append((l, r))
    random.shuffle(segs)
    cases = [(M, segs)]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 16: M = 5000 with one single segment covering all ----
    cases = [
        (5000, [(-100, 50000)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 17: Duplicate segments ----
    cases = [
        (4, [(0, 2), (0, 2), (0, 2), (2, 4), (2, 4), (2, 4)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 18: Segments all starting at 0 with different ends ----
    cases = [
        (10, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 19: Multiple random test cases (10 sub-cases) ----
    cases = []
    for _ in range(10):
        M_val = random.randint(1, 50)
        segs_case = []
        n_segs = random.randint(1, 20)
        for _ in range(n_segs):
            l = random.randint(-10, M_val)
            r = random.randint(l, M_val + 10)
            if l == 0 and r == 0:
                r = 1  # avoid terminator
            segs_case.append((l, r))
        cases.append((M_val, segs_case))
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    # ---- Test 20: Edge - segments exactly touching but barely covering ----
    # Note: (0,0) cannot be used as it's the terminator
    cases = [
        (5, [(-5, 0), (0, 1), (1, 1), (1, 2), (2, 3), (3, 3), (3, 4), (4, 5)]),
    ]
    inp, out = gen_test(test_id, cases)
    write_test(base_dir, test_id, inp, out)
    test_id += 1

    print(f"Generated {test_id - 1} test cases.")


if __name__ == '__main__':
    main()
