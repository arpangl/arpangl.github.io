#!/usr/bin/env python3
"""Generate test cases for Bangla Numbers (10414)."""

import subprocess
import os

TESTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10414/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/10414/solution.py"

# Define test cases: list of lists of numbers (each list = one test file)
test_cases = [
    # 01: Sample input
    [23764, 45897458973958],

    # 02: Zero
    [0],

    # 03: Single digit numbers
    [0, 1, 5, 9],

    # 04: Two digit numbers
    [10, 42, 99],

    # 05: Exact boundaries - shata
    [100, 200, 999],

    # 06: Exact boundaries - hajar
    [1000, 5000, 99999],

    # 07: Exact boundaries - lakh
    [100000, 500000, 9999999],

    # 08: Exact boundaries - kuti
    [10000000, 50000000, 99999999],

    # 09: Large numbers with kuti
    [100000000, 999999999, 9999999999999],

    # 10: Maximum value
    [999999999999999],

    # 11: Powers of 10
    [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000, 100000000000, 1000000000000, 10000000000000, 100000000000000],

    # 12: Numbers with zeros in various positions
    [101, 1001, 10001, 100001, 1000001, 10000001, 100000001],

    # 13: Numbers that test each unit individually
    [50, 300, 7000, 600000, 80000000],

    # 14: Numbers with all parts populated
    [1234567, 12345678, 123456789, 1234567890],

    # 15: Edge near kuti boundaries
    [9999999, 10000000, 10000001, 99999999, 100000000],

    # 16: Multiple kuti levels
    [100000000000000, 200000000000000, 999999999999999, 10000000],

    # 17: Numbers with trailing zeros
    [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000],

    # 18: Stress test with many cases
    [
        0, 1, 2, 3, 99, 100, 101, 999, 1000, 1001, 9999,
        10000, 99999, 100000, 999999, 1000000, 9999999,
        10000000, 99999999, 100000000, 999999999,
        1000000000, 9999999999, 10000000000, 99999999999,
        100000000000, 999999999999, 1000000000000,
        9999999999999, 10000000000000, 99999999999999,
        100000000000000, 999999999999999
    ],

    # 19: Numbers that test nested kuti (kuti within kuti part)
    [
        70000000000000,   # 70 lakh kuti
        10100000000000,   # 10 lakh 10 hajar kuti
        300000070000000,  # wait, this exceeds max? no, 3*10^14 = 300000000000000 > max? no, max is 999999999999999 (15 digits)
        # Let's recompute: 300000070000000 = 3*10^14 + 7*10^7 = 300000070000000 (15 digits, OK)
        300000070000000,
        99999990000000,   # 9999999 kuti 0 = 99999990000000 (14 digits)
    ],

    # 20: Mixed small and large
    [0, 999999999999999, 1, 500000000000000, 42, 12345678901234],
]

def bangla(n):
    """Convert a non-negative integer to Bangla number text."""
    if n == 0:
        return "0"
    parts = []
    if n >= 10**7:
        parts.append(bangla(n // 10**7))
        parts.append("kuti")
        n = n % 10**7
    if n >= 10**5:
        parts.append(str(n // 10**5))
        parts.append("lakh")
        n = n % 10**5
    if n >= 10**3:
        parts.append(str(n // 10**3))
        parts.append("hajar")
        n = n % 10**3
    if n >= 10**2:
        parts.append(str(n // 10**2))
        parts.append("shata")
        n = n % 10**2
    if n > 0:
        parts.append(str(n))
    return " ".join(parts)


for idx, nums in enumerate(test_cases, 1):
    fname_in = os.path.join(TESTDIR, f"{idx:02d}.in")
    fname_out = os.path.join(TESTDIR, f"{idx:02d}.out")

    # Validate all numbers are within range
    for n in nums:
        assert 0 <= n <= 999999999999999, f"Number {n} out of range"

    input_text = "\n".join(str(n) for n in nums) + "\n"

    # Generate expected output
    output_lines = []
    for case_num, n in enumerate(nums, 1):
        result = bangla(n)
        output_lines.append(f"{case_num:>4}. {result}")
    output_text = "\n".join(output_lines) + "\n"

    with open(fname_in, "w") as f:
        f.write(input_text)
    with open(fname_out, "w") as f:
        f.write(output_text)

    print(f"Generated {idx:02d}.in / {idx:02d}.out ({len(nums)} cases)")

# Verify all test cases by running solution.py
print("\nVerifying all test cases...")
all_ok = True
for idx, nums in enumerate(test_cases, 1):
    fname_in = os.path.join(TESTDIR, f"{idx:02d}.in")
    fname_out = os.path.join(TESTDIR, f"{idx:02d}.out")

    result = subprocess.run(
        ["python3", SOLUTION],
        stdin=open(fname_in),
        capture_output=True,
        text=True,
    )

    with open(fname_out) as f:
        expected = f.read()

    if result.stdout != expected:
        print(f"MISMATCH in test {idx:02d}!")
        print(f"  Expected:\n{expected}")
        print(f"  Got:\n{result.stdout}")
        all_ok = False
    else:
        print(f"  Test {idx:02d}: OK")

if all_ok:
    print("\nAll test cases verified successfully!")
else:
    print("\nSome test cases FAILED!")
