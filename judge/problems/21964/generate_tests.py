import random
import subprocess
import os

TESTCASES_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/21964/testcases"
SOLUTION_PATH = "/Users/lambert/Documents/GPE-Helper/judge/problems/21964/solution.py"

def solve_input(input_text):
    """Run solution.py on the given input and return output."""
    result = subprocess.run(
        ["python3", SOLUTION_PATH],
        input=input_text, capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"Solution failed: {result.stderr}"
    return result.stdout.strip()

def write_test(idx, input_text):
    """Write a test case pair and verify it."""
    input_text = input_text.strip() + "\n"
    output_text = solve_input(input_text)

    in_path = os.path.join(TESTCASES_DIR, f"{idx:02d}.in")
    out_path = os.path.join(TESTCASES_DIR, f"{idx:02d}.out")

    with open(in_path, "w") as f:
        f.write(input_text)
    with open(out_path, "w") as f:
        f.write(output_text + "\n")

    print(f"Test {idx:02d}: input lines={input_text.count(chr(10))}, output={output_text}")

test_cases = []

# ---- Test 01: Sample input ----
test_cases.append(
    "5 3\n1 2 3 4 5\n3 2\n4 78 9"
)

# ---- Test 02: Single vessel, single container ----
test_cases.append("1 1\n42")

# ---- Test 03: Single vessel, many containers (m >> n) ----
test_cases.append("1 1000000\n999999")

# ---- Test 04: n vessels, m = n (each vessel in its own container) ----
test_cases.append("5 5\n10 20 30 40 50")

# ---- Test 05: n vessels, m > n ----
test_cases.append("3 10\n100 200 300")

# ---- Test 06: n vessels, m = 1 (everything in one container) ----
test_cases.append("5 1\n1 2 3 4 5")

# ---- Test 07: All equal vessels ----
test_cases.append("6 3\n10 10 10 10 10 10")

# ---- Test 08: All equal vessels, not perfectly divisible ----
test_cases.append("7 3\n10 10 10 10 10 10 10")

# ---- Test 09: One very large vessel among small ones ----
test_cases.append("5 3\n1 1 1000000 1 1")

# ---- Test 10: Descending order ----
test_cases.append("5 2\n100 80 60 40 20")

# ---- Test 11: Two vessels ----
test_cases.append("2 1\n500000 500000")

# ---- Test 12: Two vessels, two containers ----
test_cases.append("2 2\n500000 500000")

# ---- Test 13: Large n, small values, few containers ----
vessels = [1] * 1000
test_cases.append(f"1000 3\n{' '.join(map(str, vessels))}")

# ---- Test 14: Large n, random values, many containers ----
random.seed(42)
n = 1000
m = 500
vessels = [random.randint(1, 1000000) for _ in range(n)]
test_cases.append(f"{n} {m}\n{' '.join(map(str, vessels))}")

# ---- Test 15: Large n, m = 1 (sum of all) ----
random.seed(123)
n = 100
vessels = [random.randint(1, 1000000) for _ in range(n)]
test_cases.append(f"{n} 1\n{' '.join(map(str, vessels))}")

# ---- Test 16: Large n, m = n ----
random.seed(456)
n = 100
vessels = [random.randint(1, 1000000) for _ in range(n)]
test_cases.append(f"{n} {n}\n{' '.join(map(str, vessels))}")

# ---- Test 17: Multiple test cases in one input (mimics EOF multi-case) ----
test_cases.append(
    "4 2\n10 20 30 40\n"
    "6 3\n5 5 5 5 5 5\n"
    "3 1\n100 200 300"
)

# ---- Test 18: Vessels of capacity 1, large m ----
n = 500
vessels = [1] * n
test_cases.append(f"{n} 250\n{' '.join(map(str, vessels))}")

# ---- Test 19: Max single vessel value ----
test_cases.append("5 2\n1000000 1000000 1000000 1000000 1000000")

# ---- Test 20: Alternating large and small ----
n = 20
vessels = []
for i in range(n):
    if i % 2 == 0:
        vessels.append(1000000)
    else:
        vessels.append(1)
test_cases.append(f"{n} 5\n{' '.join(map(str, vessels))}")

# Write all test cases
for idx, tc in enumerate(test_cases, start=1):
    write_test(idx, tc)

print(f"\nGenerated {len(test_cases)} test cases successfully.")
