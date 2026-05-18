#!/usr/bin/env python3
"""Generate test cases for 2008-37: Prefix expression evaluation."""

import os
import subprocess
import random

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-37/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-37/solution.py"

# Each test case is a list of expression lines (without the trailing '.')
test_cases = []

# TC 01: Sample test case
test_cases.append([
    "- * + 23 % 45 10 6 / 77 12",
    "+ * 234 56",
])

# TC 02: Single number (simplest valid expression)
test_cases.append([
    "0",
    "1",
    "42",
    "999999999",
])

# TC 03: Simple binary operations
test_cases.append([
    "+ 1 2",
    "- 10 3",
    "* 4 5",
    "/ 20 4",
    "% 17 5",
])

# TC 04: Nested expressions
test_cases.append([
    "+ + 1 2 3",
    "+ 1 + 2 3",
    "* + 2 3 - 7 4",
    "/ * 6 7 + 1 2",
])

# TC 05: Division and modulo edge cases
test_cases.append([
    "/ 10 3",
    "% 10 3",
    "/ 1 1",
    "% 1 1",
    "/ 0 5",
    "% 0 5",
    "/ 100 7",
    "% 100 7",
])

# TC 06: Illegal expressions - too few operands
test_cases.append([
    "+",
    "- 5",
    "* + 3",
    "+ * 234 56",
])

# TC 07: Illegal expressions - too many operands / tokens
test_cases.append([
    "1 2",
    "1 2 3",
    "+ 1 2 3",
    "* 3 4 5 6",
    "5 + 3 2",
])

# TC 08: Deeply nested left-leaning tree
test_cases.append([
    "+ + + + + 1 2 3 4 5 6",
    "* * * 2 2 2 2",
    "- - - 100 10 20 30",
])

# TC 09: Deeply nested right-leaning tree
test_cases.append([
    "+ 1 + 2 + 3 + 4 + 5 6",
    "* 2 * 2 * 2 * 2 2",
    "- 100 - 10 - 20 30",
])

# TC 10: Large numbers
test_cases.append([
    "+ 1000000 2000000",
    "* 100000 100000",
    "/ 999999999 1",
    "% 999999999 2",
    "- 0 0",
])

# TC 11: Extra spaces (multiple spaces between tokens)
test_cases.append([
    "+  1  2",
    "-   10   3",
    "*    4    5",
    "+   +   1   2   3",
])

# TC 12: Single operator only (illegal)
test_cases.append([
    "*",
    "/",
    "%",
    "-",
    "+",
])

# TC 13: Empty-ish / edge expressions
test_cases.append([
    "  ",
    "  42  ",
    "  + 1 2  ",
])

# TC 14: Complex mixed expression with all operators
test_cases.append([
    "+ - * / % 100 7 3 4 5",
    "% / * - + 10 20 3 6 7",
    "* + 1 2 % - 100 3 7",
])

# TC 15: Division producing zero
test_cases.append([
    "/ 1 2",
    "/ 3 10",
    "/ 0 100",
    "/ 99 100",
])

# TC 16: Stress - longer valid expression
def gen_random_prefix_expr(depth, max_depth):
    """Generate a random valid prefix expression."""
    ops = ['+', '-', '*', '/', '%']
    if depth >= max_depth or (depth > 0 and random.random() < 0.4):
        return str(random.randint(1, 100))
    op = random.choice(ops)
    left = gen_random_prefix_expr(depth + 1, max_depth)
    right = gen_random_prefix_expr(depth + 1, max_depth)
    return f"{op} {left} {right}"

random.seed(42)
stress_lines = []
for _ in range(5):
    expr = gen_random_prefix_expr(0, 6)
    stress_lines.append(expr)
test_cases.append(stress_lines)

# TC 17: Expressions with zero
test_cases.append([
    "* 0 999999",
    "+ 0 0",
    "- 0 0",
    "% 7 1",
    "/ 7 1",
])

# TC 18: Invalid tokens / partially invalid
test_cases.append([
    "++ 1 2",
    "a 1 2",
    "+ 1a 2",
    "1+2",
])

# TC 19: Very long chain of additions
chain = "1"
for i in range(50):
    chain = f"+ {chain} 1"
test_cases.append([
    chain,
])

# TC 20: Mixed valid and illegal in one test
test_cases.append([
    "+ 3 * 2 5",
    "- 100",
    "7",
    "/ 10 0",
    "+ 1 2 3",
    "* * * * 2 2 2 2 2",
])


def write_test_case(idx, lines):
    """Write a test case .in and compute .out using the solution."""
    in_path = os.path.join(TESTCASE_DIR, f"{idx:02d}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{idx:02d}.out")

    # Build input: lines + terminating '.'
    input_text = "\n".join(lines) + "\n.\n"

    with open(in_path, 'w') as f:
        f.write(input_text)

    # Run solution to get output
    result = subprocess.run(
        ["python3", SOLUTION],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=10,
    )

    if result.returncode != 0:
        print(f"ERROR on test case {idx:02d}: {result.stderr}")
        return False

    with open(out_path, 'w') as f:
        f.write(result.stdout)

    return True


def main():
    os.makedirs(TESTCASE_DIR, exist_ok=True)

    for i, lines in enumerate(test_cases, start=1):
        ok = write_test_case(i, lines)
        if ok:
            # Read back and display
            in_path = os.path.join(TESTCASE_DIR, f"{i:02d}.in")
            out_path = os.path.join(TESTCASE_DIR, f"{i:02d}.out")
            with open(in_path) as f:
                in_text = f.read()
            with open(out_path) as f:
                out_text = f.read()
            print(f"=== Test case {i:02d} ===")
            print(f"IN:\n{in_text}OUT:\n{out_text}")
        else:
            print(f"=== Test case {i:02d} FAILED ===")

    print(f"\nGenerated {len(test_cases)} test cases.")


if __name__ == '__main__':
    main()
