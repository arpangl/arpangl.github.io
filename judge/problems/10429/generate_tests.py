#!/usr/bin/env python3
"""
Generate test cases for problem 10429: Contest Scoreboard
"""
import random
import os
import subprocess
import sys

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10429/testcases"
SOLUTION_PATH = "/Users/lambert/Documents/GPE-Helper/judge/problems/10429/solution.py"

def generate_case_lines(teams, problems_range, max_time, num_submissions, include_all_verdicts=True):
    """Generate submission lines for one test case."""
    lines = []
    verdicts = ['C', 'I', 'R', 'U', 'E'] if include_all_verdicts else ['C', 'I']
    current_time = 1
    for _ in range(num_submissions):
        team = random.choice(teams)
        prob = random.randint(problems_range[0], problems_range[1])
        current_time += random.randint(0, max(1, max_time // num_submissions))
        time = min(current_time, max_time)
        verdict = random.choice(verdicts)
        lines.append(f"{team} {prob} {time} {verdict}")
    return lines


def make_input(cases):
    """Build full input from list of case line-lists."""
    parts = [str(len(cases)), ""]
    for i, case in enumerate(cases):
        for line in case:
            parts.append(line)
        if i < len(cases) - 1:
            parts.append("")
    return "\n".join(parts) + "\n"


def get_output(input_text):
    """Run solution and get output."""
    result = subprocess.run(
        ["python3", SOLUTION_PATH],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode != 0:
        print(f"Solution error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def write_test(idx, input_text, output_text):
    """Write a test case pair."""
    in_path = os.path.join(TESTCASE_DIR, f"{idx:02d}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{idx:02d}.out")
    with open(in_path, 'w') as f:
        f.write(input_text)
    with open(out_path, 'w') as f:
        f.write(output_text)
    print(f"  Written {idx:02d}.in / {idx:02d}.out")


def main():
    os.makedirs(TESTCASE_DIR, exist_ok=True)
    test_cases = []

    # ---- Test 01: Sample test case ----
    test_cases.append({
        'name': 'Sample from problem',
        'input': "1\n\n1 2 10 I\n3 1 11 C\n1 2 19 R\n1 2 21 C\n1 1 25 C\n"
    })

    # ---- Test 02: Single contestant, single correct submission ----
    test_cases.append({
        'name': 'Single contestant single correct',
        'input': "1\n\n1 1 10 C\n"
    })

    # ---- Test 03: Single contestant, only incorrect submissions (no solve) ----
    test_cases.append({
        'name': 'Single contestant only incorrect',
        'input': "1\n\n5 3 10 I\n5 3 20 I\n5 3 30 I\n"
    })

    # ---- Test 04: Multiple contestants tied in solved and penalty, sort by team number ----
    test_cases.append({
        'name': 'Tie-breaking by team number',
        'input': "1\n\n3 1 50 C\n1 1 50 C\n2 1 50 C\n"
    })

    # ---- Test 05: Contestant with R, U, E submissions only (still appears, 0 solved) ----
    test_cases.append({
        'name': 'Only R/U/E submissions',
        'input': "1\n\n7 2 15 R\n7 3 20 U\n7 4 30 E\n"
    })

    # ---- Test 06: Correct after many incorrect (penalty accumulation) ----
    test_cases.append({
        'name': 'Many incorrects before correct',
        'input': "1\n\n1 1 5 I\n1 1 10 I\n1 1 15 I\n1 1 20 I\n1 1 25 C\n"
    })

    # ---- Test 07: Submissions after correct should be ignored ----
    test_cases.append({
        'name': 'Submissions after correct ignored',
        'input': "1\n\n1 1 10 C\n1 1 20 I\n1 1 30 C\n"
    })

    # ---- Test 08: Multiple problems, some solved some not ----
    test_cases.append({
        'name': 'Multiple problems mixed',
        'input': "1\n\n1 1 10 I\n1 1 20 C\n1 2 30 I\n1 2 40 I\n1 3 50 C\n1 2 60 I\n"
    })

    # ---- Test 09: Two test cases (multiple cases in one input) ----
    test_cases.append({
        'name': 'Two cases in one input',
        'input': "2\n\n1 1 10 C\n2 1 20 C\n\n3 2 5 C\n4 2 10 I\n4 2 15 C\n"
    })

    # ---- Test 10: Large team numbers (up to 100) ----
    test_cases.append({
        'name': 'Large team numbers',
        'input': "1\n\n100 9 299 C\n99 9 300 C\n50 1 100 C\n50 2 200 C\n"
    })

    # ---- Test 11: All 9 problems solved by one contestant ----
    lines = []
    for p in range(1, 10):
        lines.append(f"1 {p} {p * 10} C")
    test_cases.append({
        'name': 'One contestant solves all 9 problems',
        'input': "1\n\n" + "\n".join(lines) + "\n"
    })

    # ---- Test 12: Ranking by solved count takes priority over penalty ----
    test_cases.append({
        'name': 'Solved count > penalty priority',
        'input': "1\n\n1 1 200 C\n1 2 250 C\n2 1 5 C\n"
    })

    # ---- Test 13: Multiple cases with blank line separation, some contestants only have non-scoring submissions ----
    test_cases.append({
        'name': 'Mixed scoring and non-scoring with multiple cases',
        'input': "3\n\n1 1 10 C\n2 1 20 R\n\n5 5 50 U\n5 5 60 E\n5 5 70 C\n\n10 1 5 I\n10 1 10 I\n20 2 15 C\n10 1 20 C\n"
    })

    # ---- Test 14: Contestant solves same problem with first submission correct (no penalty from wrong) ----
    test_cases.append({
        'name': 'Immediate correct, no penalty',
        'input': "1\n\n1 1 42 C\n2 1 42 I\n2 1 50 C\n"
    })

    # ---- Test 15: Stress test - many contestants many submissions ----
    random.seed(42)
    stress_lines = []
    teams = list(range(1, 51))
    current_t = 0
    for _ in range(500):
        team = random.choice(teams)
        prob = random.randint(1, 9)
        current_t += random.randint(1, 3)
        verdict = random.choice(['C', 'I', 'R', 'U', 'E'])
        stress_lines.append(f"{team} {prob} {current_t} {verdict}")
    test_cases.append({
        'name': 'Stress: 50 teams, 500 submissions',
        'input': "1\n\n" + "\n".join(stress_lines) + "\n"
    })

    # ---- Test 16: Stress test - 100 teams, 1000 submissions, 3 cases ----
    random.seed(123)
    all_case_lines = []
    for _ in range(3):
        case_lines = []
        current_t = 0
        for _ in range(300):
            team = random.randint(1, 100)
            prob = random.randint(1, 9)
            current_t += random.randint(1, 5)
            verdict = random.choice(['C', 'I', 'I', 'R', 'U', 'E'])  # more I's
            case_lines.append(f"{team} {prob} {current_t} {verdict}")
        all_case_lines.append(case_lines)
    parts = ["3", ""]
    for i, cl in enumerate(all_case_lines):
        parts.extend(cl)
        if i < 2:
            parts.append("")
    test_cases.append({
        'name': 'Stress: 3 cases, 100 teams, 300 submissions each',
        'input': "\n".join(parts) + "\n"
    })

    # ---- Test 17: Edge - single submission that is Unjudged ----
    test_cases.append({
        'name': 'Single unjudged submission',
        'input': "1\n\n42 5 100 U\n"
    })

    # ---- Test 18: Edge - contestant 1 and 100 with various problems ----
    test_cases.append({
        'name': 'Min and max team IDs',
        'input': "1\n\n1 1 1 C\n100 9 299 I\n100 9 300 C\n1 9 200 I\n1 9 250 I\n1 9 290 C\n"
    })

    # ---- Test 19: Multiple cases where one case is empty (no submissions) ----
    # Actually per problem spec, cases have submissions. Let's do: one case with only non-scoring.
    test_cases.append({
        'name': 'Case with only clarification requests',
        'input': "2\n\n1 1 10 C\n2 1 20 C\n\n5 3 50 R\n5 4 60 R\n"
    })

    # ---- Test 20: All incorrect for multiple problems, then solve one ----
    test_cases.append({
        'name': 'Many wrongs across problems, only one solved',
        'input': "1\n\n1 1 10 I\n1 1 20 I\n1 2 30 I\n1 2 40 I\n1 3 50 I\n1 3 60 I\n1 1 70 C\n"
    })

    # Generate all test cases
    print(f"Generating {len(test_cases)} test cases...")
    for idx, tc in enumerate(test_cases, 1):
        input_text = tc['input']
        output_text = get_output(input_text)
        write_test(idx, input_text, output_text)
        print(f"    [{tc['name']}]")

    print(f"\nDone! {len(test_cases)} test cases generated.")


if __name__ == '__main__':
    main()
