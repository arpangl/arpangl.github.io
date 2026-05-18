"""
Generate test cases for 11041 - Children's Game
"""
import os
import random
from functools import cmp_to_key

TESTCASE_DIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/11041/testcases'

def compare(a, b):
    ab = a + b
    ba = b + a
    if ab > ba:
        return -1
    elif ab < ba:
        return 1
    else:
        return 0

def solve(numbers):
    nums = sorted(numbers, key=cmp_to_key(compare))
    return ''.join(nums)

def build_input(test_cases):
    """Build a complete input string from a list of test cases (each is a list of string numbers)."""
    lines = []
    for tc in test_cases:
        n = len(tc)
        lines.append(str(n))
        lines.append(' '.join(tc))
    lines.append('0')
    return '\n'.join(lines) + '\n'

def build_output(test_cases):
    """Compute outputs for all test cases."""
    results = []
    for tc in test_cases:
        results.append(solve(tc))
    return '\n'.join(results) + '\n'

def write_case(case_num, test_cases):
    fname = f"{case_num:02d}"
    inp = build_input(test_cases)
    out = build_output(test_cases)
    with open(os.path.join(TESTCASE_DIR, fname + '.in'), 'w') as f:
        f.write(inp)
    with open(os.path.join(TESTCASE_DIR, fname + '.out'), 'w') as f:
        f.write(out)

def random_number(max_digits=6):
    """Generate a random positive integer as string."""
    d = random.randint(1, max_digits)
    if d == 1:
        return str(random.randint(1, 9))
    first = str(random.randint(1, 9))
    rest = ''.join(str(random.randint(0, 9)) for _ in range(d - 1))
    return first + rest

# ============================================================
# Test case definitions
# ============================================================

case_num = 1

# TC01: Sample input (3 test cases in one file)
write_case(case_num, [
    ['123', '124', '56', '90'],
    ['123', '124', '56', '90', '9'],
    ['9', '9', '9', '9', '9'],
])
case_num += 1

# TC02: Single number
write_case(case_num, [
    ['42'],
])
case_num += 1

# TC03: Single number (large)
write_case(case_num, [
    ['999999999'],
])
case_num += 1

# TC04: Two numbers, basic ordering
write_case(case_num, [
    ['9', '1'],
    ['30', '3'],
    ['3', '30'],
    ['34', '3'],
    ['3', '34'],
])
case_num += 1

# TC05: All same digits
write_case(case_num, [
    ['5', '5', '5', '5', '5', '5', '5', '5', '5', '5'],
    ['1', '1', '1'],
    ['99', '99', '99'],
])
case_num += 1

# TC06: All single digits
write_case(case_num, [
    ['9', '8', '7', '6', '5', '4', '3', '2', '1'],
    ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
])
case_num += 1

# TC07: Numbers with same prefix - tricky cases
write_case(case_num, [
    ['12', '121'],
    ['12', '128'],
    ['12', '120'],
    ['56', '564'],
    ['56', '562'],
])
case_num += 1

# TC08: Classic tricky case: 30 vs 3, 9 vs 90
write_case(case_num, [
    ['3', '30', '34', '5', '9'],
    ['90', '9', '99', '998'],
])
case_num += 1

# TC09: All same multi-digit number
write_case(case_num, [
    ['12', '12', '12', '12', '12'],
    ['100', '100', '100'],
])
case_num += 1

# TC10: Prefix overlap stress
write_case(case_num, [
    ['1', '10', '100', '1000'],
    ['9', '90', '900', '9000'],
    ['5', '50', '500', '54', '540', '56'],
])
case_num += 1

# TC11: N=50 (max), random numbers
random.seed(42)
tc = [random_number(4) for _ in range(50)]
write_case(case_num, [tc])
case_num += 1

# TC12: N=50, all have same first digit
random.seed(123)
tc = ['9' + ''.join(str(random.randint(0, 9)) for _ in range(random.randint(0, 4))) for _ in range(50)]
write_case(case_num, [tc])
case_num += 1

# TC13: Mix of 1-digit and multi-digit
write_case(case_num, [
    ['1', '2', '3', '10', '20', '30', '100', '200', '300'],
])
case_num += 1

# TC14: Numbers that are prefixes of each other in complex ways
write_case(case_num, [
    ['121', '12', '1212', '12121'],
    ['21', '212', '2121', '2'],
    ['9', '98', '989', '9899'],
])
case_num += 1

# TC15: Large numbers (many digits)
random.seed(999)
tc = [random_number(8) for _ in range(30)]
write_case(case_num, [tc])
case_num += 1

# TC16: Multiple test cases in one input, varied sizes
random.seed(2026)
cases = []
for _ in range(5):
    n = random.randint(5, 20)
    tc = [random_number(5) for _ in range(n)]
    cases.append(tc)
write_case(case_num, cases)
case_num += 1

# TC17: Edge - all 1s and 10s
write_case(case_num, [
    ['1', '10', '1', '10', '1', '10'],
    ['10', '1'],
    ['1', '10'],
])
case_num += 1

# TC18: Decreasing length numbers
write_case(case_num, [
    ['99999', '9999', '999', '99', '9'],
    ['11111', '1111', '111', '11', '1'],
    ['54321', '5432', '543', '54', '5'],
])
case_num += 1

# TC19: N=50, numbers with lots of zeros
random.seed(7777)
tc = []
for _ in range(50):
    first = str(random.randint(1, 9))
    rest = ''.join(str(random.choice([0, 0, 0, random.randint(1,9)])) for _ in range(random.randint(0, 5)))
    tc.append(first + rest)
write_case(case_num, [tc])
case_num += 1

# TC20: Stress test - multiple test cases, each with N=50
random.seed(31415)
cases = []
for _ in range(3):
    tc = [random_number(6) for _ in range(50)]
    cases.append(tc)
write_case(case_num, cases)
case_num += 1

print(f"Generated {case_num - 1} test cases.")
