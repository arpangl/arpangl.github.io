import random
import subprocess
import os

BASE = "/Users/lambert/Documents/GPE-Helper/judge/problems/10615"
TC_DIR = os.path.join(BASE, "testcases")
SOLUTION = os.path.join(BASE, "solution.py")

test_cases = []

# ============================================================
# Test 1: Sample test case from the problem
# ============================================================
test_cases.append({
    "desc": "Sample from problem",
    "cases": [
        (4, 7, [17, 5, -21, 15]),
        (4, 5, [17, 5, -21, 15]),
    ]
})

# ============================================================
# Test 2: N=1, single element divisible by K
# ============================================================
test_cases.append({
    "desc": "N=1 single element divisible",
    "cases": [
        (1, 3, [9]),
        (1, 7, [0]),
        (1, 2, [-4]),
    ]
})

# ============================================================
# Test 3: N=1, single element NOT divisible by K
# ============================================================
test_cases.append({
    "desc": "N=1 single element not divisible",
    "cases": [
        (1, 3, [10]),
        (1, 7, [1]),
        (1, 100, [99]),
    ]
})

# ============================================================
# Test 4: All zeros
# ============================================================
test_cases.append({
    "desc": "All zeros",
    "cases": [
        (5, 2, [0, 0, 0, 0, 0]),
        (3, 100, [0, 0, 0]),
    ]
})

# ============================================================
# Test 5: All same number
# ============================================================
test_cases.append({
    "desc": "All same number",
    "cases": [
        (4, 3, [3, 3, 3, 3]),   # 3+3+3+3=12 div by 3, or 3-3+3-3=0
        (3, 5, [7, 7, 7]),      # 7+7-7=7, 7-7+7=7, 7+7+7=21, 7-7-7=-7 -> none div by 5
        (5, 4, [2, 2, 2, 2, 2]),# 2+2+2+2-2=6, 2+2+2-2+2=6, ... 2-2+2-2+2=2, 2+2-2+2-2=2, 2+2+2-2-2=2, 2-2-2+2+2=2, 2-2+2+2-2=2, etc. all even but check mod 4
    ]
})

# ============================================================
# Test 6: N=2 edge cases
# ============================================================
test_cases.append({
    "desc": "N=2 edge",
    "cases": [
        (2, 2, [1, 1]),         # 1+1=2 divisible, 1-1=0 divisible
        (2, 3, [1, 1]),         # 1+1=2, 1-1=0 -> Divisible (0 is div by 3)
        (2, 5, [3, 7]),         # 3+7=10, 3-7=-4 -> 10 div by 5 -> Divisible
        (2, 5, [3, 6]),         # 3+6=9, 3-6=-3 -> Not divisible
    ]
})

# ============================================================
# Test 7: Large K=100, small numbers
# ============================================================
test_cases.append({
    "desc": "Large K=100 small nums",
    "cases": [
        (10, 100, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
        (5, 100, [1, 2, 3, 4, 5]),
    ]
})

# ============================================================
# Test 8: Negative numbers
# ============================================================
test_cases.append({
    "desc": "Negative numbers",
    "cases": [
        (4, 3, [-1, -2, -3, -4]),
        (3, 7, [-7, -14, -21]),
        (5, 10, [-5, -15, -25, -35, -45]),
    ]
})

# ============================================================
# Test 9: Mix of positive and negative, all large abs values
# ============================================================
test_cases.append({
    "desc": "Large absolute values",
    "cases": [
        (5, 7, [10000, -10000, 9999, -9999, 7]),
        (3, 100, [10000, 10000, 10000]),
    ]
})

# ============================================================
# Test 10: N=10000 (max), K=2, all odd -> always odd sum -> check parity
# ============================================================
random.seed(42)
nums_10 = [random.choice([1, 3, 5, 7, 9]) for _ in range(10000)]
test_cases.append({
    "desc": "N=10000 K=2 all odd numbers",
    "cases": [
        (10000, 2, nums_10),
    ]
})

# ============================================================
# Test 11: N=10000 (max), K=100 (max), random values
# ============================================================
random.seed(123)
nums_11 = [random.randint(-10000, 10000) for _ in range(10000)]
test_cases.append({
    "desc": "N=10000 K=100 random",
    "cases": [
        (10000, 100, nums_11),
    ]
})

# ============================================================
# Test 12: N=10000, K=97 (large prime), random
# ============================================================
random.seed(456)
nums_12 = [random.randint(-10000, 10000) for _ in range(10000)]
test_cases.append({
    "desc": "N=10000 K=97 large prime random",
    "cases": [
        (10000, 97, nums_12),
    ]
})

# ============================================================
# Test 13: All elements are multiples of K
# ============================================================
test_cases.append({
    "desc": "All multiples of K",
    "cases": [
        (5, 7, [7, 14, 21, 28, 35]),
        (4, 10, [10, 20, 30, 40]),
    ]
})

# ============================================================
# Test 14: K=2 with mix of odd/even
# ============================================================
test_cases.append({
    "desc": "K=2 parity cases",
    "cases": [
        (5, 2, [1, 2, 3, 4, 5]),   # sum of odds: 1,3,5 = 3 odds, 2 evens. +/- on odds can flip parity
        (4, 2, [1, 3, 5, 7]),      # all odd, 4 of them, sum is always even
        (3, 2, [1, 3, 5]),         # all odd, 3 of them, sum is always odd -> Not divisible
    ]
})

# ============================================================
# Test 15: Stress test - multiple large cases in one input
# ============================================================
random.seed(789)
stress_cases = []
for _ in range(5):
    n = random.randint(5000, 10000)
    k = random.randint(2, 100)
    nums = [random.randint(-10000, 10000) for _ in range(n)]
    stress_cases.append((n, k, nums))
test_cases.append({
    "desc": "Multiple large random cases",
    "cases": stress_cases,
})

# ============================================================
# Test 16: Edge - N=1, K=100, value=0
# ============================================================
test_cases.append({
    "desc": "Single zero element",
    "cases": [
        (1, 100, [0]),
        (1, 2, [0]),
    ]
})

# ============================================================
# Test 17: Tricky - values that are exactly +/- K
# ============================================================
test_cases.append({
    "desc": "Values equal to K or -K",
    "cases": [
        (3, 5, [5, -5, 5]),
        (4, 3, [3, -3, 3, -3]),
        (2, 7, [7, -7]),
    ]
})

# ============================================================
# Test 18: Large N, K=2, alternating 1 and -1
# ============================================================
nums_18 = []
for i in range(10000):
    nums_18.append(1 if i % 2 == 0 else -1)
test_cases.append({
    "desc": "N=10000 K=2 alternating 1 and -1",
    "cases": [
        (10000, 2, nums_18),
    ]
})

# ============================================================
# Now generate .in/.out files
# ============================================================
def format_input(cases_list):
    lines = []
    lines.append(str(len(cases_list)))
    for (n, k, nums) in cases_list:
        lines.append(f"{n} {k}")
        lines.append(' '.join(map(str, nums)))
    return '\n'.join(lines) + '\n'

for i, tc in enumerate(test_cases):
    idx = i + 1
    fname = f"{idx:02d}"
    in_path = os.path.join(TC_DIR, f"{fname}.in")
    out_path = os.path.join(TC_DIR, f"{fname}.out")

    in_content = format_input(tc["cases"])

    with open(in_path, 'w') as f:
        f.write(in_content)

    # Run solution to get output
    result = subprocess.run(
        ['python3', SOLUTION],
        input=in_content,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        print(f"ERROR on test {idx}: {result.stderr}")
        continue

    with open(out_path, 'w') as f:
        f.write(result.stdout)

    print(f"Test {idx:02d} ({tc['desc']}): generated OK  [{len(tc['cases'])} case(s)]")

print("\nAll test cases generated!")
