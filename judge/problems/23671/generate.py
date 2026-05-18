import random
import os
import subprocess

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/23671/testcases"
SOLVE_PATH = "/Users/lambert/Documents/GPE-Helper/judge/problems/23671/solve.py"
BRUTE_PATH = "/Users/lambert/Documents/GPE-Helper/judge/problems/23671/brute.py"

def gen_expr(num_count, min_val=1, max_val=20, ops=None):
    """Generate a random expression with num_count numbers."""
    if ops is None:
        ops = ['+', '*']
    nums = [random.randint(min_val, max_val) for _ in range(num_count)]
    operators = [random.choice(ops) for _ in range(num_count - 1)]
    expr = str(nums[0])
    for i in range(len(operators)):
        expr += operators[i] + str(nums[i+1])
    return expr

def write_test(case_num, expressions):
    """Write a test case file and compute output."""
    in_path = os.path.join(TESTCASE_DIR, f"{case_num:02d}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{case_num:02d}.out")

    input_text = f"{len(expressions)}\n"
    for expr in expressions:
        input_text += expr + "\n"

    with open(in_path, 'w') as f:
        f.write(input_text)

    # Compute output using solve.py
    result = subprocess.run(
        ['python3', SOLVE_PATH],
        input=input_text, capture_output=True, text=True
    )
    with open(out_path, 'w') as f:
        f.write(result.stdout)

    return input_text, result.stdout

def verify_with_brute(input_text, expected_output, case_num):
    """Verify using brute force (only for small expressions)."""
    result = subprocess.run(
        ['python3', BRUTE_PATH],
        input=input_text, capture_output=True, text=True
    )
    if result.stdout != expected_output:
        print(f"MISMATCH on case {case_num}!")
        print(f"Input:\n{input_text}")
        print(f"Expected:\n{expected_output}")
        print(f"Brute:\n{result.stdout}")
        return False
    return True

def main():
    random.seed(42)
    case_num = 1

    # ------ Test Case 01: Sample input ------
    exprs = ["1+2*3*4+5", "4*18+14+7*10", "3+11+4*1*13*12*8+3*3+8"]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: sample input ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 02: Single number ------
    exprs = ["1", "20", "10", "5"]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: single numbers ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 03: Two numbers ------
    exprs = ["1+1", "1*1", "20+20", "20*20", "1+20", "1*20", "20+1", "20*1"]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: two numbers ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 04: All additions ------
    exprs = [
        "1+1+1+1+1+1+1+1+1+1+1+1",
        "20+20+20+20+20+20+20+20+20+20+20+20",
        "1+2+3+4+5+6+7+8+9+10+11+12",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: all additions ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 05: All multiplications ------
    exprs = [
        "1*1*1*1*1*1*1*1*1*1*1*1",
        "2*2*2*2*2*2*2*2*2*2*2*2",
        "20*20*20*20*20*20*20*20*20*20*20*20",
        "1*2*3*4*5*6*7*8*9*10*11*12",
    ]
    inp, out = write_test(case_num, exprs)
    # brute force on 12 multiplications is fine (only one way to evaluate)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: all multiplications ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 06: Alternating +* ------
    exprs = [
        "1+2*3+4*5+6*7+8*9+10*11+12",
        "20+20*20+20*20+20*20+20*20+20*20+20",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: alternating operators ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 07: Alternating *+ ------
    exprs = [
        "1*2+3*4+5*6+7*8+9*10+11*12",
        "20*20+20*20+20*20+20*20+20*20+20*20",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: alternating *+ ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 08: All 1s with mixed operators ------
    exprs = [
        "1+1*1+1*1+1*1+1*1+1*1+1",
        "1*1+1*1+1*1+1*1+1*1+1*1",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: all 1s mixed ops ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 09: Maximum possible value (all 20s, 12 numbers) ------
    exprs = [
        "20*20*20*20*20*20*20*20*20*20*20*20",
        "20+20*20+20*20+20*20+20*20+20*20+20",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: large values ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 10: Single operator expressions ------
    exprs = [
        "5+10",
        "5*10",
        "1+1",
        "1*1",
        "20+20",
        "20*20",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: single operator ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 11: Random small (3-5 numbers), verified with brute ------
    exprs = [gen_expr(random.randint(3, 5)) for _ in range(10)]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: random small ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 12: Random medium (6-8 numbers), verified with brute ------
    exprs = [gen_expr(random.randint(6, 8)) for _ in range(10)]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: random medium ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 13: Random large (9-12 numbers), verified with brute ------
    exprs = [gen_expr(random.randint(9, 12)) for _ in range(8)]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: random large ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 14: Max 12 numbers, all expressions ------
    exprs = [gen_expr(12) for _ in range(5)]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: max-size expressions ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 15: Mostly additions with one multiplication ------
    exprs = [
        "5+5+5+5+5*5+5+5+5+5+5+5",
        "1+1+1+1+1+1+1+1+1+1+1*20",
        "20*1+1+1+1+1+1+1+1+1+1+1",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: mostly additions ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 16: Mostly multiplications with one addition ------
    exprs = [
        "2*2*2*2*2+2*2*2*2*2*2*2",
        "20*20*20*20*20*20*20*20*20*20*20+1",
        "1+20*20*20*20*20*20*20*20*20*20*20",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: mostly multiplications ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 17: Expressions with value 1 and 20 extremes ------
    exprs = [
        "1*1*1*1*1+20*20*20*20*20*20*20",
        "20+1*1*1*1*1*1*1*1*1*1+20",
        "1+20*1+20*1+20*1+20*1+20*1+20",
    ]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: extreme 1 and 20 ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 18: Stress test - many expressions ------
    exprs = [gen_expr(random.randint(2, 12)) for _ in range(20)]
    inp, out = write_test(case_num, exprs)
    # Verify with brute force
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: stress test ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 19: Three numbers, all operator combos ------
    exprs = []
    for a in [1, 10, 20]:
        for b in [1, 10, 20]:
            for op1 in ['+', '*']:
                for op2 in ['+', '*']:
                    exprs.append(f"{a}{op1}{b}{op2}{a}")
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: 3-number combos ({len(exprs)} expressions)")
    case_num += 1

    # ------ Test Case 20: Single expression, N=1 edge ------
    exprs = ["7"]
    inp, out = write_test(case_num, exprs)
    verify_with_brute(inp, out, case_num)
    print(f"Case {case_num:02d}: single expression N=1 ({len(exprs)} expressions)")
    case_num += 1

    print(f"\nGenerated {case_num - 1} test cases, all verified.")

if __name__ == '__main__':
    main()
