#!/usr/bin/env python3
"""Generate test cases for problem 2008-06: Parser and evaluator."""

import os

TESTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-06/testcases"

# Each test case is a list of expression strings (one per line in the .in file)
test_cases = []

# TC 01: Sample test case
test_cases.append([
    "789-(400+300)",
    "789-400+300",
    "-9*80+72/61%7",
    "72+((38-66)",
    "-101**29",
    "123/78%23 45",
])

# TC 02: Simple single numbers and zero
test_cases.append([
    "0",
    "1",
    "999999999",
    "00123",
])

# TC 03: Unary plus and minus
test_cases.append([
    "-0",
    "+0",
    "-1",
    "+1",
    "--5",
    "---5",
    "+-+-5",
    "-+-+5",
])

# TC 04: Simple binary operations
test_cases.append([
    "3+4",
    "10-7",
    "6*8",
    "17/5",
    "17%5",
    "-17/5",
    "-17%5",
    "17/-5",
    "17%-5",
])

# TC 05: Priority: % higher than * and /
test_cases.append([
    "100/10%3",
    "100*10%3",
    "10%3*100",
    "10%3/2",
    "72/61%7",
    "100%7*3",
    "100%7/2",
])

# TC 06: Parentheses and nesting
test_cases.append([
    "(1)",
    "((1))",
    "(((1)))",
    "(1+2)*3",
    "3*(1+2)",
    "((2+3)*(4-1))",
    "(((5)))",
])

# TC 07: Syntactically incorrect - various errors
test_cases.append([
    "",
    "()",
    "1+",
    "+",
    "*5",
    "1 2",
    "(1+2",
    "1+2)",
    "1+2+",
    "abc",
    "1&2",
    "1^2",
])

# TC 08: Complex expressions with all operators
test_cases.append([
    "1+2-3+4-5+6",
    "2*3*4*5",
    "100/3/3/3",
    "100%13%5",
    "1+2*3+4",
    "2*3+4*5",
    "10-2*3+4/2",
])

# TC 09: Unary minus with operators
test_cases.append([
    "-1+2",
    "-1*-2",
    "-1*(-2)",
    "-(1+2)",
    "-(-(-1))",
    "1--2",
    "1*-2*-3",
])

# TC 10: Large numbers
test_cases.append([
    "999999999+1",
    "1000000000-999999999",
    "99999*99999",
    "1000000000/3",
    "1000000000%3",
])

# TC 11: Division and modulo edge cases (C-style truncation toward zero)
test_cases.append([
    "7/2",
    "-7/2",
    "7/-2",
    "-7/-2",
    "7%2",
    "-7%2",
    "7%-2",
    "-7%-2",
    "1/1",
    "0/1",
    "0%1",
])

# TC 12: Tricky syntactic cases
test_cases.append([
    "1*-2",
    "1/-2",
    "1%-2",
    "1+(-2)",
    "1+(+2)",
    "(+5)",
    "(-5)",
    "1*(-(2+3))",
])

# TC 13: Empty/whitespace and special characters (all should be incorrect)
test_cases.append([
    " ",
    "  ",
    "1 +2",
    "1+ 2",
    " 1+2",
    "1+2 ",
    "1.5+2",
    "1,2",
])

# TC 14: Long chained operations
test_cases.append([
    "1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1",
    "100-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1",
    "2*2*2*2*2*2*2*2*2*2",
    "1024/2/2/2/2/2/2/2/2/2/2",
    "1000000%97%13",
])

# TC 15: Deeply nested parentheses
test_cases.append([
    "((((((((1+2))))))))",
    "((((((((-1))))))))",
    "((1+2)*(3+4))%((5-2)*(1+1))",
    "-(-(-(-(1))))",
])

# TC 16: Priority interaction stress
test_cases.append([
    "2+3%2*4",
    "10%3+2*5%3",
    "100/10%3+5*2%3-1",
    "5%3%2",
    "100/7%3*2+1",
    "-5%3",
    "-5%-3",
    "(-5)%3",
    "(-5)%(-3)",
])

# TC 17: More syntax errors
test_cases.append([
    "**1",
    "//1",
    "%%1",
    "()",
    ")(",
    "1(2)",
    "(1)(2)",
    "1+*2",
    "1*/2",
    "1%*2",
])

# TC 18: Edge: only unary operations
test_cases.append([
    "-(-(-(-(-1))))",
    "+(+(+(+(+1))))",
    "-1",
    "+1",
    "-(1)",
    "+(1)",
    "--1",
    "++1",
])

os.makedirs(TESTDIR, exist_ok=True)

for i, expressions in enumerate(test_cases, 1):
    in_file = os.path.join(TESTDIR, f"{i:02d}.in")
    with open(in_file, "w") as f:
        for expr in expressions:
            f.write(expr + "\n")

print(f"Generated {len(test_cases)} test input files.")
