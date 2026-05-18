#!/usr/bin/env python3
"""
Generate test cases for Problem 10501 - Safe Salutations

Test cases cover:
- Single values (all n from 1 to 10)
- Multiple datasets in one input
- Edge cases: minimum n=1, maximum n=10
- Various combinations
"""

import os
from math import comb

TESTCASES_DIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10501/testcases'

def catalan(n):
    return comb(2 * n, n) // (n + 1)

def make_input(datasets):
    """Create input string from a list of n values, separated by blank lines."""
    return '\n\n'.join(str(d) for d in datasets) + '\n'

def make_output(datasets):
    """Create output string from a list of n values, separated by blank lines."""
    return '\n\n'.join(str(catalan(d)) for d in datasets) + '\n'

def write_test(idx, datasets):
    """Write a test case with given index and list of dataset values."""
    in_path = os.path.join(TESTCASES_DIR, f'{idx:02d}.in')
    out_path = os.path.join(TESTCASES_DIR, f'{idx:02d}.out')

    in_text = make_input(datasets)
    out_text = make_output(datasets)

    with open(in_path, 'w') as f:
        f.write(in_text)
    with open(out_path, 'w') as f:
        f.write(out_text)

    print(f'Test {idx:02d}: datasets={datasets}')
    print(f'  Input:  {repr(in_text)}')
    print(f'  Output: {repr(out_text)}')

os.makedirs(TESTCASES_DIR, exist_ok=True)

test_id = 1

# Test 01: Sample case - single value n=4
write_test(test_id, [4]); test_id += 1

# Test 02: Minimum n=1
write_test(test_id, [1]); test_id += 1

# Test 03: Maximum n=10
write_test(test_id, [10]); test_id += 1

# Test 04: n=2
write_test(test_id, [2]); test_id += 1

# Test 05: n=3
write_test(test_id, [3]); test_id += 1

# Test 06: n=5
write_test(test_id, [5]); test_id += 1

# Test 07: n=6
write_test(test_id, [6]); test_id += 1

# Test 08: n=7
write_test(test_id, [7]); test_id += 1

# Test 09: n=8
write_test(test_id, [8]); test_id += 1

# Test 10: n=9
write_test(test_id, [9]); test_id += 1

# Test 11: Two datasets - min and max
write_test(test_id, [1, 10]); test_id += 1

# Test 12: Three datasets
write_test(test_id, [3, 5, 7]); test_id += 1

# Test 13: All values 1 through 10
write_test(test_id, list(range(1, 11))); test_id += 1

# Test 14: Descending order 10 to 1
write_test(test_id, list(range(10, 0, -1))); test_id += 1

# Test 15: Repeated same value
write_test(test_id, [5, 5, 5]); test_id += 1

# Test 16: Two datasets with small values
write_test(test_id, [1, 2]); test_id += 1

# Test 17: Mix of small and large
write_test(test_id, [1, 10, 2, 9]); test_id += 1

# Test 18: Five datasets mixed
write_test(test_id, [4, 8, 2, 6, 10]); test_id += 1

print(f'\nGenerated {test_id - 1} test cases.')
