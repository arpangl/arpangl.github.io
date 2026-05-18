#!/usr/bin/env python3
"""Generate test cases for Smith Numbers problem (23571)."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from solution import is_smith, next_smith

TESTCASE_DIR = os.path.join(os.path.dirname(__file__), 'testcases')

def write_test(idx, inputs, outputs):
    """Write a test case pair."""
    in_path = os.path.join(TESTCASE_DIR, f'{idx:02d}.in')
    out_path = os.path.join(TESTCASE_DIR, f'{idx:02d}.out')

    in_lines = [str(len(inputs))] + [str(x) for x in inputs]
    out_lines = [str(x) for x in outputs]

    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f'Test {idx:02d}: {len(inputs)} queries written')

def gen():
    test_idx = 1

    # --- Test 01: Sample test case ---
    inputs = [4937774, 456456]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 02: Very small values (n=1,2,3) -> first smith is 4 ---
    inputs = [1, 2, 3]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 03: n just below known small Smith numbers ---
    inputs = [3, 21, 26, 57, 84, 93, 120, 165]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 04: n = Smith number itself (should return NEXT smith) ---
    inputs = [4, 22, 27, 58, 85, 94, 121, 166]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 05: n = prime numbers (primes are NOT smith) ---
    inputs = [2, 5, 7, 11, 13, 17, 23, 29, 97, 101]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 06: n = non-smith composites ---
    inputs = [6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 07: Medium values ---
    inputs = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 08: Larger medium values ---
    inputs = [9999, 12345, 54321, 99999, 100000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 09: Values around 1 million ---
    inputs = [999999, 1000000, 1000001, 999000, 500000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 10: Values around 4937775 (the famous number) ---
    inputs = [4937770, 4937774, 4937775, 4937776, 4937780]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 11: Large values near 10^7 ---
    inputs = [9999990, 9999995, 9999999, 10000000, 5000000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 12: Large values near 10^8 ---
    inputs = [99999990, 99999999, 100000000, 50000000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 13: Values near 10^9 (upper boundary) ---
    inputs = [999999900, 999999950, 999999990]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 14: Various large scattered values ---
    inputs = [123456789, 987654321, 111111111, 222222222, 333333333]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 15: Powers of 2 and 10 ---
    inputs = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 10, 100, 1000, 10000, 100000, 1000000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 16: Consecutive small values to stress correctness ---
    inputs = list(range(1, 21))
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 17: Single large value near boundary ---
    inputs = [999999999]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    # --- Test 18: Mix of small, medium, large ---
    inputs = [1, 50, 500, 5000, 50000, 500000, 5000000, 50000000, 500000000]
    outputs = [next_smith(n) for n in inputs]
    write_test(test_idx, inputs, outputs); test_idx += 1

    print(f'\nTotal test cases generated: {test_idx - 1}')

if __name__ == '__main__':
    gen()
