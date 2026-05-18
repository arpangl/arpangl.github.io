#!/usr/bin/env python3
"""
Test case generator for 2009-02: Line Overlap Problem

Constraints:
  - N < 200000 segments
  - Coordinates i, j < 100000 (the problem says i < 100000 and j < 100000)
  - Output may exceed 32-bit int

Edge cases to cover:
  01: Sample input
  02: Single segment (no pairs => 0)
  03: Two identical segments (full overlap)
  04: Two non-overlapping segments
  05: Two segments that touch at a single point (overlap = 0)
  06: One segment fully inside another
  07: Multiple segments all identical
  08: Multiple segments, no overlaps at all
  09: All segments share the same left endpoint
  10: All segments share the same right endpoint
  11: Segments with left > right (reversed endpoints - problem says left and right, but let's handle)
  12: Many overlapping segments to get large output (stress for 64-bit)
  13: Large N, random segments
  14: Large N, many overlapping segments (stress test)
  15: Large N, segments clustered in small range
  16: All segments are length 0 (point segments, l == r)
  17: Mix of point segments and real segments
  18: Two segments with partial overlap
  19: Large N with segments that are all nested
  20: Coordinates at boundary (0 and 99999)
"""

import random
import os

# Import solution
from solution import solve, brute_force


def make_input(segments):
    """Format segments into input string."""
    lines = []
    for l, r in segments:
        # Use variable spacing to match problem statement
        lines.append(f"{l}  {r}")
    lines.append(".")
    return "\n".join(lines) + "\n"


def generate_tests():
    test_cases = []

    # 01: Sample input
    test_cases.append(("01", [(75, 325), (5, 120), (100, 255), (325, 500)]))

    # 02: Single segment
    test_cases.append(("02", [(10, 50)]))

    # 03: Two identical segments
    test_cases.append(("03", [(100, 500), (100, 500)]))

    # 04: Two non-overlapping segments
    test_cases.append(("04", [(10, 20), (30, 40)]))

    # 05: Two segments touching at a point
    test_cases.append(("05", [(10, 20), (20, 30)]))

    # 06: One segment fully inside another
    test_cases.append(("06", [(10, 100), (30, 70)]))

    # 07: Multiple identical segments (5 identical)
    test_cases.append(("07", [(50, 200)] * 5))

    # 08: Multiple non-overlapping segments
    test_cases.append(("08", [(0, 10), (20, 30), (40, 50), (60, 70), (80, 90)]))

    # 09: All share the same left endpoint
    test_cases.append(("09", [(0, 10), (0, 20), (0, 30), (0, 40), (0, 50)]))

    # 10: All share the same right endpoint
    test_cases.append(("10", [(10, 100), (20, 100), (30, 100), (40, 100), (50, 100)]))

    # 11: Three segments with various overlaps
    test_cases.append(("11", [(0, 99999), (0, 99999), (0, 99999)]))

    # 12: Many overlapping segments for large output (need 64-bit)
    # 1000 segments all [0, 99999], each pair overlaps by 99999
    # C(1000,2) * 99999 = 499500 * 99999 = 49,949,500,500 > 2^32
    segs_12 = [(0, 99999)] * 1000
    test_cases.append(("12", segs_12))

    # 13: Large random test
    random.seed(42)
    segs_13 = []
    for _ in range(50000):
        a = random.randint(0, 99998)
        b = random.randint(a + 1, 99999)
        segs_13.append((a, b))
    test_cases.append(("13", segs_13))

    # 14: Large N, many overlapping (stress)
    random.seed(123)
    segs_14 = []
    for _ in range(100000):
        a = random.randint(0, 50000)
        b = random.randint(a + 1, min(a + 1000, 99999))
        segs_14.append((a, b))
    test_cases.append(("14", segs_14))

    # 15: Large N, segments clustered in small range
    random.seed(456)
    segs_15 = []
    for _ in range(100000):
        a = random.randint(100, 200)
        b = random.randint(a + 1, min(a + 50, 300))
        segs_15.append((a, b))
    test_cases.append(("15", segs_15))

    # 16: All point segments (length 0)
    test_cases.append(("16", [(5, 5), (5, 5), (10, 10), (10, 10)]))

    # 17: Mix of point segments and real segments
    test_cases.append(("17", [(10, 10), (5, 15), (10, 20), (0, 10)]))

    # 18: Two segments with partial overlap
    test_cases.append(("18", [(10, 30), (20, 40)]))

    # 19: Nested segments (each inside the previous)
    segs_19 = []
    for i in range(100):
        segs_19.append((i, 99999 - i))
    test_cases.append(("19", segs_19))

    # 20: Boundary coordinates
    test_cases.append(("20", [(0, 99999), (0, 1), (99998, 99999), (50000, 50001)]))

    return test_cases


def main():
    base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/2009-02/testcases"
    os.makedirs(base_dir, exist_ok=True)

    test_cases = generate_tests()

    for name, segments in test_cases:
        input_text = make_input(segments)
        answer = solve(segments)

        # For small test cases, verify with brute force
        if len(segments) <= 1000:
            bf_answer = brute_force(segments)
            assert answer == bf_answer, f"Test {name}: solve={answer}, brute_force={bf_answer}"
            print(f"Test {name}: N={len(segments):>6d}, answer={answer} (verified with brute force)")
        else:
            print(f"Test {name}: N={len(segments):>6d}, answer={answer} (large test, brute force skipped)")

        in_path = os.path.join(base_dir, f"{name}.in")
        out_path = os.path.join(base_dir, f"{name}.out")

        with open(in_path, "w") as f:
            f.write(input_text)
        with open(out_path, "w") as f:
            f.write(f"{answer}\n")

    print(f"\nGenerated {len(test_cases)} test cases in {base_dir}")


if __name__ == "__main__":
    main()
