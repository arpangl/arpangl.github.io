#!/usr/bin/env python3
"""Generate test cases for problem 10552 - Automated Judge Script."""

import os
import subprocess
import sys

TESTCASES_DIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10552/testcases'
SOLUTION_PATH = '/Users/lambert/Documents/GPE-Helper/judge/problems/10552/solution.py'

test_cases = []

# ============================================================
# Test 1: Sample input (from problem statement)
# ============================================================
test_cases.append("""\
2
The answer is: 10
The answer is: 5
2
The answer is: 10
The answer is: 5
2
The answer is: 10
The answer is: 5
2
The answer is: 10
The answer is: 15
2
The answer is: 10
The answer is:  5
2
The answer is: 10
The answer is: 5
3
Input Set #1: YES
Input Set #2: NO
Input Set #3: NO
3
Input Set #0: YES
Input Set #1: NO
Input Set #2: NO
1
1 0 1 0
1
1010
1
The judges are mean!
1
The judges are good!
0
""")

# ============================================================
# Test 2: Single line, exact match (Accepted)
# ============================================================
test_cases.append("""\
1
Hello World
1
Hello World
0
""")

# ============================================================
# Test 3: Single line, completely different no digits (Wrong Answer - no digits means empty == empty => PE)
# Actually: no numeric chars in either => both numeric sequences are empty "" == "" => Presentation Error
# Wait - but if both have NO digits, numeric strings are both empty, so they match => PE
# But the text differs, so not Accepted. So it should be Presentation Error.
# Let me reconsider: if no digits, standard_nums="" and team_nums="" => they match => PE
# ============================================================
test_cases.append("""\
1
abc
1
xyz
0
""")

# ============================================================
# Test 4: No digits in standard, digits in team (Wrong Answer)
# standard_nums="" vs team_nums="123" => WA
# ============================================================
test_cases.append("""\
1
hello
1
hello123
0
""")

# ============================================================
# Test 5: Digits in standard, no digits in team (Wrong Answer)
# ============================================================
test_cases.append("""\
1
answer is 42
1
answer is
0
""")

# ============================================================
# Test 6: Same digits different non-digit chars (Presentation Error)
# ============================================================
test_cases.append("""\
1
a1b2c3
1
x1y2z3
0
""")

# ============================================================
# Test 7: Multiple lines standard vs single line team - exact digits (PE)
# Standard: "12\n34" => digits "1234", Team: "1234" => digits "1234" => PE (not accepted since text differs)
# ============================================================
test_cases.append("""\
2
12
34
1
1234
0
""")

# ============================================================
# Test 8: Empty lines / whitespace differences (Presentation Error if no digits)
# Standard: " " (one space), Team: "" (empty) => no digits => PE
# Actually let me make both have same content with slight whitespace diff and digits
# ============================================================
test_cases.append("""\
1
 1 2 3
1
123
0
""")

# ============================================================
# Test 9: Large multi-line accepted
# ============================================================
test_cases.append("""\
3
Line one: 100
Line two: 200
Line three: 300
3
Line one: 100
Line two: 200
Line three: 300
0
""")

# ============================================================
# Test 10: Different number of lines, same content spread differently (PE)
# Standard (1 line): "12 34 56" => digits "123456"
# Team (3 lines): "12\n34\n56" => digits "123456"
# Text differs => PE
# ============================================================
test_cases.append("""\
1
12 34 56
3
12
34
56
0
""")

# ============================================================
# Test 11: Digits reordered (Wrong Answer)
# Standard digits: "123", Team digits: "321"
# ============================================================
test_cases.append("""\
1
1 2 3
1
3 2 1
0
""")

# ============================================================
# Test 12: Mixed - multiple test sets in one input
# Set 1: Accepted (exact match)
# Set 2: PE (same digits, different text)
# Set 3: WA (different digits)
# ============================================================
test_cases.append("""\
1
YES
1
YES
1
result: 99
1
Result: 99
1
score 10
1
score 20
0
""")

# ============================================================
# Test 13: Edge case - single character lines
# ============================================================
test_cases.append("""\
1
5
1
5
1
5
1
6
1
a
1
b
0
""")

# ============================================================
# Test 14: Lines with only digits and spaces
# Standard: "1 2 3", Team: "1  2  3" => digits both "123" => PE (text differs due to extra spaces)
# ============================================================
test_cases.append("""\
1
1 2 3
1
1  2  3
0
""")

# ============================================================
# Test 15: Empty digit sequences on both sides but different text (PE)
# No digits at all in either
# ============================================================
test_cases.append("""\
2
Hello World
Goodbye World
2
Hi World
Bye World
0
""")

# ============================================================
# Test 16: Team output has extra digits (WA)
# Standard: "abc" => "", Team: "abc1" => "1"
# ============================================================
test_cases.append("""\
1
abc
1
abc1
0
""")

# ============================================================
# Test 17: Long lines with many digits, presentation error
# Same digits but different formatting
# ============================================================
test_cases.append("""\
1
Result: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
1
Result:1 2 3 4 5 6 7 8 9 10
0
""")

# ============================================================
# Test 18: Multiple runs covering all three verdicts in one input
# Run 1: Accepted
# Run 2: Presentation Error
# Run 3: Wrong Answer
# Run 4: Accepted (multi-line)
# Run 5: PE (trailing space difference with digits)
# ============================================================
test_cases.append("""\
1
42
1
42
1
The answer is 42.
1
answer 42
1
100
1
200
3
alpha
beta
gamma
3
alpha
beta
gamma
2
x = 10
y = 20
2
x=10
y=20
0
""")

# ============================================================
# Test 19: Stress - many test sets
# ============================================================
lines_19 = []
for i in range(20):
    lines_19.append("1")
    lines_19.append(f"value {i}")
    lines_19.append("1")
    lines_19.append(f"value {i}")
lines_19.append("0")
test_cases.append('\n'.join(lines_19) + '\n')

# ============================================================
# Test 20: Edge - standard and team both have zero-length numeric after filtering
# but text is identical => Accepted
# ============================================================
test_cases.append("""\
1
no digits here
1
no digits here
0
""")

# ============================================================
# Generate .in and .out files
# ============================================================

def compute_output(input_text):
    proc = subprocess.run(
        [sys.executable, SOLUTION_PATH],
        input=input_text,
        capture_output=True,
        text=True
    )
    return proc.stdout


os.makedirs(TESTCASES_DIR, exist_ok=True)

for i, tc in enumerate(test_cases, start=1):
    in_file = os.path.join(TESTCASES_DIR, f'{i:02d}.in')
    out_file = os.path.join(TESTCASES_DIR, f'{i:02d}.out')

    with open(in_file, 'w') as f:
        f.write(tc)

    output = compute_output(tc)

    with open(out_file, 'w') as f:
        f.write(output)

    # Print for verification
    print(f'=== Test {i:02d} ===')
    print(f'Input:\n{tc}')
    print(f'Output:\n{output}')
    print()

print(f'Generated {len(test_cases)} test cases.')
