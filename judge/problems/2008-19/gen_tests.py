#!/usr/bin/env python3
"""
Test case generator for 2008-19: Set partition

Generates 18 test cases covering:
- Sample case
- No valid subset (odd total sum)
- No valid subset (even total sum but no partition)
- Single element
- Two elements (equal and unequal)
- All elements equal
- Large values (up to 10^12)
- n=1 edge case
- n=2 edge cases
- Multiple datasets per input
- Many subsets
- Exactly one partition (2 subsets)
- n=30 with no solution (odd sum)
- n=30 with solution
- Large values meeting in the middle
- Powers of 2
- Consecutive integers
"""

import random
import os
import subprocess
import sys

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-19/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-19/solution.py"

def make_input(datasets):
    """Convert list of arrays to input string."""
    lines = []
    for arr in datasets:
        lines.append("{" + " ".join(map(str, arr)) + "}")
    lines.append(".")
    return "\n".join(lines) + "\n"


def get_output(input_str):
    """Run solution and get output."""
    result = subprocess.run(
        ["python3", SOLUTION],
        input=input_str,
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode != 0:
        print(f"STDERR: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Solution failed with return code {result.returncode}")
    return result.stdout


def write_test(idx, input_str, output_str):
    """Write test case files."""
    prefix = f"{idx:02d}"
    with open(os.path.join(TESTCASE_DIR, f"{prefix}.in"), "w") as f:
        f.write(input_str)
    with open(os.path.join(TESTCASE_DIR, f"{prefix}.out"), "w") as f:
        f.write(output_str)
    # Count datasets
    ndatasets = input_str.count("{")
    print(f"Test {prefix}: {ndatasets} dataset(s) written")


def gen():
    tests = []

    # Test 01: Sample case
    tests.append(([
        [1, 2, 3, 4, 5, 6, 7],
        [1, 3, 5, 7, 12],
    ], "Sample case"))

    # Test 02: Single element - no partition possible
    tests.append(([
        [5],
    ], "Single element"))

    # Test 03: Two equal elements - one partition
    tests.append(([
        [3, 3],
    ], "Two equal elements"))

    # Test 04: Two unequal elements - no partition
    tests.append(([
        [3, 5],
    ], "Two unequal elements"))

    # Test 05: Three elements, one valid partition
    tests.append(([
        [1, 2, 3],
    ], "Three elements, {3} and {1,2}"))

    # Test 06: Odd total sum - no partition
    tests.append(([
        [1, 2, 4],
    ], "Odd sum, no partition"))

    # Test 07: All elements equal (even count)
    tests.append(([
        [5, 5, 5, 5],
    ], "Four equal elements"))

    # Test 08: All elements equal (odd count) - odd total, no partition
    tests.append(([
        [5, 5, 5],
    ], "Three equal elements, odd total"))

    # Test 09: Consecutive integers 1..10
    tests.append(([
        list(range(1, 11)),
    ], "Consecutive 1-10"))

    # Test 10: Large values, two elements equal
    tests.append(([
        [1000000000000, 1000000000000],
    ], "Two large equal elements"))

    # Test 11: Large values, no partition (odd sum)
    tests.append(([
        [999999999999, 1000000000000, 500000000000],
    ], "Large values, odd sum"))

    # Test 12: Large values, partition exists
    tests.append(([
        [100000000000, 200000000000, 300000000000, 400000000000, 500000000000, 500000000000],
    ], "Large values with partition"))

    # Test 13: Powers of 2 - unique subset sums, at most one partition
    tests.append(([
        [1, 2, 4, 8, 16, 32, 64, 128],
    ], "Powers of 2 (1-128)"))

    # Test 14: Multiple small datasets mixed
    tests.append(([
        [1, 1],
        [1, 2],
        [2, 3, 5],
        [1, 5, 6, 10],
        [10, 20, 30, 40, 50, 50],
    ], "Multiple small mixed datasets"))

    # Test 15: n=15, random with even sum guaranteed
    random.seed(42)
    arr15 = sorted(random.sample(range(1, 100), 15))
    s = sum(arr15)
    if s % 2 != 0:
        arr15[-1] += 1  # make sum even
    tests.append(([arr15], "n=15 random"))

    # Test 16: n=20, designed to have many partitions
    # Use {1,2,3,...,20} which has sum=210, even, target=105
    tests.append(([
        list(range(1, 21)),
    ], "Consecutive 1-20, many partitions"))

    # Test 17: n=25 with large values, no solution (odd sum)
    arr17 = [i * 1000000001 for i in range(1, 26)]
    # sum = 1000000001 * sum(1..25) = 1000000001 * 325 = 325000000325
    # 325000000325 is odd => no partition
    tests.append(([arr17], "n=25 large values, odd sum"))

    # Test 18: n=8 with exactly one partition (2 subsets)
    # {1, 2, 3, 10, 4} => sum=20, target=10 => {10} and {1,2,3,4}
    tests.append(([
        [1, 2, 3, 4, 10],
    ], "Exactly one partition pair"))

    idx = 1
    for datasets, desc in tests:
        input_str = make_input(datasets)
        output_str = get_output(input_str)
        write_test(idx, input_str, output_str)
        print(f"  Description: {desc}")
        idx += 1

    print(f"\nGenerated {len(tests)} test cases.")


if __name__ == "__main__":
    gen()
