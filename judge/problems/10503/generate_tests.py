#!/usr/bin/env python3
"""Generate test cases for problem 10503 - Show the Sequence"""

import subprocess
import os

TESTCASES_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10503/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/10503/solution.py"

test_cases = []

# Test 01: Sample input 1 - simple additive
test_cases.append(("[2+[1]] 3", "Sample: simple additive"))

# Test 02: Sample input 2 - multiply with nested add
test_cases.append(("[2*[5+[-2]]] 7", "Sample: multiply with nested add negative"))

# Test 03: Constant sequence
test_cases.append(("[5] 10", "Constant sequence"))

# Test 04: Constant negative
test_cases.append(("[-3] 5", "Constant negative sequence"))

# Test 05: Constant zero
test_cases.append(("[0] 4", "Constant zero"))

# Test 06: Simple additive with constant 0 increment
test_cases.append(("[10+[0]] 6", "Additive with zero increment (constant)"))

# Test 07: Arithmetic sequence (additive with constant step)
test_cases.append(("[1+[3]] 8", "Arithmetic sequence step 3"))

# Test 08: Additive with negative step
test_cases.append(("[100+[-5]] 10", "Additive with negative step"))

# Test 09: Triangular numbers (nested add)
test_cases.append(("[1+[2+[1]]] 10", "Triangular numbers"))

# Test 10: Multiply with constant
test_cases.append(("[1*[2]] 10", "Geometric: multiply by 2"))

# Test 11: Multiply with constant 1 (stays same after first)
test_cases.append(("[3*[1]] 5", "Multiply by 1"))

# Test 12: Deep nesting - triple nested add
test_cases.append(("[0+[0+[0+[1]]]] 10", "Deep nesting triple add"))

# Test 13: Large N = 50 with simple sequence
test_cases.append(("[1+[1]] 50", "N=50 natural numbers"))

# Test 14: Multiply with nested additive (produces large numbers)
test_cases.append(("[2*[1+[2+[1]]]] 8", "Multiply with triangular"))

# Test 15: Additive starting from 0
test_cases.append(("[0+[1]] 7", "Additive from 0"))

# Test 16: Multiply with negative constant
test_cases.append(("[1*[-1]] 8", "Multiply by -1 alternating"))

# Test 17: N=2 minimal
test_cases.append(("[1+[1]] 2", "Minimal N=2"))

# Test 18: Large constant
test_cases.append(("[999+[1]] 5", "Large starting value"))

# Test 19: Nested multiply in add
test_cases.append(("[0+[1*[2]]] 8", "Add with inner multiply (powers of 2 as increments)"))

# Test 20: Complex nested: multiply with deeply nested
test_cases.append(("[1*[1+[1+[1]]]] 10", "Multiply with double-nested add"))

os.makedirs(TESTCASES_DIR, exist_ok=True)

for i, (inp, desc) in enumerate(test_cases, 1):
    in_file = os.path.join(TESTCASES_DIR, f"{i:02d}.in")
    out_file = os.path.join(TESTCASES_DIR, f"{i:02d}.out")

    # Write input
    with open(in_file, 'w') as f:
        f.write(inp + '\n')

    # Run solution to get output
    result = subprocess.run(
        ['python3', SOLUTION],
        input=inp + '\n',
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"ERROR on test {i:02d} ({desc}): {result.stderr}")
        continue

    output = result.stdout.strip()

    with open(out_file, 'w') as f:
        f.write(output + '\n')

    print(f"Test {i:02d}: {desc}")
    print(f"  Input:  {inp}")
    print(f"  Output: {output}")
    print()

print(f"Generated {len(test_cases)} test cases in {TESTCASES_DIR}")
