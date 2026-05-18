#!/usr/bin/env python3
"""Generate test cases for Bee Maja (UVA 10182 / problem 10551)."""

import os
import sys

# Add solution
sys.path.insert(0, os.path.dirname(__file__))
from solution import solve

TESTCASE_DIR = os.path.join(os.path.dirname(__file__), 'testcases')
os.makedirs(TESTCASE_DIR, exist_ok=True)

test_cases = []

# TC 01: Sample input
test_cases.append(("01", "1\n2\n3\n4\n5"))

# TC 02: Just cell 1 (center)
test_cases.append(("02", "1"))

# TC 03: End of ring 1 (cells 6 and 7)
test_cases.append(("03", "6\n7"))

# TC 04: Start of ring 2 (cell 8) and first few ring 2 cells
test_cases.append(("04", "7\n8\n9\n10\n11"))

# TC 05: Complete ring 2 (cells 8-19)
test_cases.append(("05", "8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19"))

# TC 06: Ring transitions - last cell of ring r and first cell of ring r+1
# Ring 1: 2-7, Ring 2: 8-19, Ring 3: 20-37, Ring 4: 38-61
test_cases.append(("06", "7\n8\n19\n20\n37\n38\n61\n62"))

# TC 07: Single large number near max
test_cases.append(("07", "99999"))

# TC 08: Maximum value
test_cases.append(("08", "99999\n100000"))

# TC 09: Small sequential (cells 1-10)
test_cases.append(("09", "\n".join(str(i) for i in range(1, 11))))

# TC 10: Powers of 2 within range
test_cases.append(("10", "\n".join(str(2**i) for i in range(0, 17) if 2**i < 100000)))

# TC 11: First cells of each ring (ring starts)
# Ring r starts at cell: 3r^2 - 3r + 2
ring_starts = []
for r in range(0, 20):
    cell = 3 * r * r - 3 * r + 2
    if cell >= 1 and cell < 100000 and cell not in ring_starts:
        ring_starts.append(cell)
test_cases.append(("11", "\n".join(str(c) for c in ring_starts)))

# TC 12: Last cells of each ring
# Ring r has 6r cells (r>=1), ring 0 has 1 cell
# Last cell of ring r: 3r^2 + 3r + 1
ring_ends = []
for r in range(0, 20):
    cell = 3 * r * r + 3 * r + 1
    if cell >= 1 and cell < 100000:
        ring_ends.append(cell)
test_cases.append(("12", "\n".join(str(c) for c in ring_ends)))

# TC 13: Corner positions of each ring (6 corners per ring)
# For ring r, corner positions along each side
corner_cells = set()
for r in range(1, 10):
    start = 3 * r * r - 3 * r + 2
    for side in range(6):
        if side == 0:
            # Corner at end of side 0
            corner = start + (r - 1)
        else:
            corner = start + (r - 1) + side * r
        if corner < 100000:
            corner_cells.add(corner)
corner_list = sorted(corner_cells)[:20]
test_cases.append(("13", "\n".join(str(c) for c in corner_list)))

# TC 14: Multiples of 1000
test_cases.append(("14", "\n".join(str(i) for i in range(1000, 100000, 10000))))

# TC 15: Random-looking but deterministic spread across range
import random
random.seed(42)
vals = sorted(random.sample(range(1, 100000), 20))
test_cases.append(("15", "\n".join(str(v) for v in vals)))

# TC 16: Consecutive cells around a ring boundary (ring 10)
# Ring 10 starts at 3*100-30+2 = 272
ring10_start = 3 * 10 * 10 - 3 * 10 + 2
cells_16 = list(range(ring10_start - 3, ring10_start + 5))
test_cases.append(("16", "\n".join(str(c) for c in cells_16)))

# TC 17: Very small numbers (1, 2, 3)
test_cases.append(("17", "1\n2\n3"))

# TC 18: Middle of large rings
# Ring 50 starts at 3*2500-150+2 = 7352
# Middle of ring 50 is about 7352 + 150 = 7502
test_cases.append(("18", "7352\n7502\n7652"))

# TC 19: Stress test - many numbers
vals_19 = list(range(1, 51))  # cells 1-50
test_cases.append(("19", "\n".join(str(v) for v in vals_19)))

# TC 20: Near-maximum values
test_cases.append(("20", "99990\n99991\n99992\n99993\n99994\n99995\n99996\n99997\n99998\n99999"))

# Generate all test case files
for tc_id, input_text in test_cases:
    in_path = os.path.join(TESTCASE_DIR, f"{tc_id}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{tc_id}.out")

    output_text = solve(input_text)

    with open(in_path, 'w') as f:
        f.write(input_text + '\n')
    with open(out_path, 'w') as f:
        f.write(output_text + '\n')

    # Verify by re-reading and solving
    with open(in_path, 'r') as f:
        verify_input = f.read()
    verify_output = solve(verify_input)
    assert verify_output == output_text, f"Verification failed for test case {tc_id}!"

    print(f"Test case {tc_id}: {len(input_text.strip().split(chr(10)))} inputs")
    # Show first few lines of output
    out_lines = output_text.split('\n')
    for line in out_lines[:3]:
        print(f"  {line}")
    if len(out_lines) > 3:
        print(f"  ... ({len(out_lines)} lines total)")

print(f"\nGenerated {len(test_cases)} test cases in {TESTCASE_DIR}")
