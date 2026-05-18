import os
import subprocess
import random

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-28/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/2008-28/solution.py"

test_cases = []

# ============================================================
# Test 1: Sample test case from the problem
# ============================================================
test_cases.append({
    "name": "sample",
    "cases": [
        (6, [2, 5, 3, 1, 6, 4]),
        (9, [2, 6, 1, 9, 7, 3, 5, 4, 8]),
        (7, [1, 2, 3, 4, 5, 6, 7]),
        (7, [7, 6, 5, 4, 3, 2, 1]),
    ]
})

# ============================================================
# Test 2: Single element
# ============================================================
test_cases.append({
    "name": "single_element",
    "cases": [
        (1, [1]),
        (1, [100]),
        (1, [4294967295]),  # 2^32 - 1
    ]
})

# ============================================================
# Test 3: Two elements - increasing, decreasing, equal
# ============================================================
test_cases.append({
    "name": "two_elements",
    "cases": [
        (2, [1, 2]),
        (2, [2, 1]),
        (2, [5, 5]),  # equal -> LIS length 1
    ]
})

# ============================================================
# Test 4: All same elements
# ============================================================
test_cases.append({
    "name": "all_same",
    "cases": [
        (3, [5, 5, 5]),
        (5, [1, 1, 1, 1, 1]),
        (9, [42, 42, 42, 42, 42, 42, 42, 42, 42]),
    ]
})

# ============================================================
# Test 5: Strictly increasing sequences
# ============================================================
test_cases.append({
    "name": "strictly_increasing",
    "cases": [
        (5, [1, 2, 3, 4, 5]),
        (9, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (3, [10, 100, 1000]),
    ]
})

# ============================================================
# Test 6: Strictly decreasing sequences
# ============================================================
test_cases.append({
    "name": "strictly_decreasing",
    "cases": [
        (5, [5, 4, 3, 2, 1]),
        (9, [9, 8, 7, 6, 5, 4, 3, 2, 1]),
    ]
})

# ============================================================
# Test 7: Alternating up-down
# ============================================================
test_cases.append({
    "name": "alternating",
    "cases": [
        (5, [1, 3, 2, 4, 3]),
        (7, [1, 5, 2, 6, 3, 7, 4]),
        (9, [1, 9, 2, 8, 3, 7, 4, 6, 5]),
    ]
})

# ============================================================
# Test 8: Large values near 2^32 - 1
# ============================================================
test_cases.append({
    "name": "large_values",
    "cases": [
        (5, [4294967295, 4294967294, 4294967293, 4294967292, 4294967291]),
        (5, [4294967291, 4294967292, 4294967293, 4294967294, 4294967295]),
        (3, [1, 2147483648, 4294967295]),
    ]
})

# ============================================================
# Test 9: Multiple LIS of same length (many ties)
# ============================================================
test_cases.append({
    "name": "many_lis",
    "cases": [
        (6, [1, 3, 5, 2, 4, 6]),
        (8, [1, 4, 2, 5, 3, 6, 7, 8]),
    ]
})

# ============================================================
# Test 10: V-shape and inverted V-shape
# ============================================================
test_cases.append({
    "name": "v_shapes",
    "cases": [
        (5, [5, 4, 3, 2, 1]),  # strictly decreasing (degenerate V)
        (5, [1, 2, 3, 4, 5]),  # strictly increasing (degenerate inv-V)
        (5, [5, 3, 1, 3, 5]),  # V shape
        (5, [1, 3, 5, 3, 1]),  # inverted V
    ]
})

# ============================================================
# Test 11: Plateau then increase
# ============================================================
test_cases.append({
    "name": "plateau_increase",
    "cases": [
        (6, [1, 1, 1, 2, 3, 4]),
        (7, [5, 5, 5, 5, 6, 7, 8]),
        (9, [1, 1, 2, 2, 3, 3, 4, 4, 5]),
    ]
})

# ============================================================
# Test 12: Max n=9 with random permutation
# ============================================================
random.seed(42)
perm = list(range(1, 10))
random.shuffle(perm)
test_cases.append({
    "name": "random_perm_9",
    "cases": [
        (9, perm),
    ]
})

# ============================================================
# Test 13: n=9 zigzag pattern
# ============================================================
test_cases.append({
    "name": "zigzag_9",
    "cases": [
        (9, [1, 9, 2, 8, 3, 7, 4, 6, 5]),
    ]
})

# ============================================================
# Test 14: Sequences with duplicates interleaved
# ============================================================
test_cases.append({
    "name": "duplicates_interleaved",
    "cases": [
        (6, [1, 2, 1, 2, 1, 2]),
        (8, [3, 1, 4, 1, 5, 9, 2, 6]),
        (9, [1, 3, 2, 3, 1, 2, 3, 2, 1]),
    ]
})

# ============================================================
# Test 15: Single large test with n=9 (worst-case-like)
# ============================================================
test_cases.append({
    "name": "single_large_9",
    "cases": [
        (9, [5, 1, 4, 2, 3, 9, 7, 8, 6]),
    ]
})

# ============================================================
# Test 16: Edge - mixed large and small values
# ============================================================
test_cases.append({
    "name": "mixed_large_small",
    "cases": [
        (5, [4294967295, 1, 4294967294, 2, 4294967293]),
        (4, [1, 4294967295, 2, 4294967294]),
    ]
})

# ============================================================
# Test 17: Nearly sorted with one swap
# ============================================================
test_cases.append({
    "name": "nearly_sorted",
    "cases": [
        (9, [1, 2, 3, 4, 5, 6, 7, 9, 8]),
        (9, [2, 1, 3, 4, 5, 6, 7, 8, 9]),
        (9, [1, 2, 3, 4, 9, 6, 7, 8, 5]),
    ]
})

# ============================================================
# Test 18: Multiple test patterns with various n
# ============================================================
random.seed(123)
cases_18 = []
for _ in range(5):
    n = random.randint(3, 9)
    seq = [random.randint(1, 20) for _ in range(n)]
    cases_18.append((n, seq))
test_cases.append({
    "name": "random_multi",
    "cases": cases_18,
})


def generate_input(cases):
    lines = [str(len(cases))]
    for n, seq in cases:
        lines.append(str(n))
        lines.append(" ".join(map(str, seq)))
    return "\n".join(lines) + "\n"


def compute_output(input_text):
    result = subprocess.run(
        ["python3", SOLUTION],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        raise RuntimeError("Solution failed")
    return result.stdout


for i, tc in enumerate(test_cases, start=1):
    fname = f"{i:02d}"
    input_text = generate_input(tc["cases"])
    output_text = compute_output(input_text)

    in_path = os.path.join(TESTCASE_DIR, f"{fname}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{fname}.out")

    with open(in_path, "w") as f:
        f.write(input_text)
    with open(out_path, "w") as f:
        f.write(output_text)

    print(f"Generated {fname}: {tc['name']} ({len(tc['cases'])} patterns)")

print(f"\nTotal: {len(test_cases)} test files generated.")
