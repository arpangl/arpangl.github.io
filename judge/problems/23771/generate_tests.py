import math
import random
import os

random.seed(42)

BASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/23771/testcases"

def solve_case(s, k):
    """Given string s and k (1-based), find the alphabet ordering."""
    n = len(s)
    k0 = k - 1  # 0-based
    lehmer = []
    for i in range(n):
        fact = math.factorial(n - 1 - i)
        digit = k0 // fact
        k0 = k0 % fact
        lehmer.append(digit)

    alpha = []
    for i in range(n - 1, -1, -1):
        alpha.insert(lehmer[i], s[i])
    return ''.join(alpha)


def generate_kth_permutation(alpha_order, k):
    """Given an alphabet ordering, return the k-th (1-based) permutation."""
    n = len(alpha_order)
    k0 = k - 1
    remaining = list(alpha_order)
    result = []
    for i in range(n):
        fact = math.factorial(n - 1 - i)
        idx = k0 // fact
        k0 = k0 % fact
        result.append(remaining.pop(idx))
    return ''.join(result)


# Collect all test cases as (s, k) pairs grouped by test file
test_files = []

# --- Test 1: Sample cases ---
test_files.append([
    ("bdac", 11),
    ("abcd", 5),
    ("hjbrl", 120),
])

# --- Test 2: Single character (n=1), k must be 1 ---
cases = []
for ch in ['a', 'z', 'm']:
    cases.append((ch, 1))
test_files.append(cases)

# --- Test 3: n=2 all possibilities ---
cases = []
# n=2: k can be 1 or 2
cases.append(("ab", 1))  # alpha = ab, 1st perm = ab
cases.append(("ab", 2))  # alpha = ba, 2nd perm of ba order = ab
cases.append(("za", 1))
cases.append(("za", 2))
test_files.append(cases)

# --- Test 4: n=3, first and last permutations ---
cases = []
alpha = "xyz"
cases.append((generate_kth_permutation(alpha, 1), 1))  # k=1 => first perm = alpha itself
cases.append((generate_kth_permutation(alpha, 6), 6))  # k=6 => last perm = reverse of alpha
cases.append((generate_kth_permutation(alpha, 3), 3))  # middle
test_files.append(cases)

# --- Test 5: k=1 always means s IS the alphabet order ---
cases = []
cases.append(("abcde", 1))
cases.append(("zyxwv", 1))
cases.append(("qwert", 1))
test_files.append(cases)

# --- Test 6: k = n! (last permutation = reverse of alpha) ---
cases = []
alpha = "abcde"
n = 5
cases.append((generate_kth_permutation(alpha, math.factorial(n)), math.factorial(n)))
alpha = "pqrst"
cases.append((generate_kth_permutation(alpha, math.factorial(n)), math.factorial(n)))
test_files.append(cases)

# --- Test 7: n=20, k=1 (alphabet order itself) ---
cases = []
alpha = "abcdefghijklmnopqrst"
cases.append((alpha, 1))
test_files.append(cases)

# --- Test 8: n=20, k = n! (maximum k, last permutation = reverse) ---
cases = []
alpha = "abcdefghijklmnopqrst"
n = 20
k = math.factorial(n)
cases.append((generate_kth_permutation(alpha, k), k))
test_files.append(cases)

# --- Test 9: n=20, random k values ---
cases = []
n = 20
max_k = math.factorial(n)
letters = list("abcdefghijklmnopqrst")
for _ in range(3):
    random.shuffle(letters)
    alpha = ''.join(letters)
    k = random.randint(1, max_k)
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 10: n=15, various random ---
cases = []
n = 15
max_k = math.factorial(n)
all_letters = list("abcdefghijklmno")
for _ in range(4):
    random.shuffle(all_letters)
    alpha = ''.join(all_letters)
    k = random.randint(1, max_k)
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 11: n=10, stress with several cases ---
cases = []
n = 10
max_k = math.factorial(n)
all_letters = list("abcdefghij")
for _ in range(5):
    random.shuffle(all_letters)
    alpha = ''.join(all_letters)
    k = random.randint(1, max_k)
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 12: Various n values mixed ---
cases = []
for n in [3, 5, 7, 9, 12, 18]:
    letters = random.sample("abcdefghijklmnopqrstuvwxyz", n)
    random.shuffle(letters)
    alpha = ''.join(letters)
    k = random.randint(1, math.factorial(n))
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 13: k=2 for various n (second permutation - swap last two) ---
cases = []
for n in [2, 4, 6, 10, 15]:
    letters = sorted(random.sample("abcdefghijklmnopqrstuvwxyz", n))
    alpha = ''.join(letters)
    k = 2
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 14: k = n! - 1 (second to last permutation) ---
cases = []
for n in [3, 5, 8, 12]:
    letters = sorted(random.sample("abcdefghijklmnopqrstuvwxyz", n))
    alpha = ''.join(letters)
    k = math.factorial(n) - 1
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 15: Large T with small n (stress test T close to 5000) ---
cases = []
for _ in range(100):
    n = random.randint(1, 5)
    letters = random.sample("abcdefghijklmnopqrstuvwxyz", n)
    random.shuffle(letters)
    alpha = ''.join(letters)
    k = random.randint(1, math.factorial(n))
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 16: n=20 with middle k values ---
cases = []
n = 20
max_k = math.factorial(n)
letters = list("abcdefghijklmnopqrst")
for _ in range(2):
    random.shuffle(letters)
    alpha = ''.join(letters)
    k = max_k // 2
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
    k = max_k // 3
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 17: Alphabet uses non-contiguous letters ---
cases = []
for _ in range(5):
    n = random.randint(5, 12)
    # Pick letters spread across the alphabet
    letters = random.sample("abcdefghijklmnopqrstuvwxyz", n)
    random.shuffle(letters)
    alpha = ''.join(letters)
    k = random.randint(1, math.factorial(n))
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)

# --- Test 18: Maximum T=5000, mixed small to medium n ---
cases = []
for _ in range(5000):
    n = random.randint(1, 10)
    letters = random.sample("abcdefghijklmnopqrstuvwxyz", n)
    random.shuffle(letters)
    alpha = ''.join(letters)
    k = random.randint(1, math.factorial(n))
    s = generate_kth_permutation(alpha, k)
    cases.append((s, k))
test_files.append(cases)


# Write all test files
for file_idx, cases in enumerate(test_files):
    file_num = file_idx + 1
    prefix = f"{file_num:02d}"

    # Build input
    lines_in = [str(len(cases))]
    for s, k in cases:
        lines_in.append(f"{s} {k}")
    input_text = '\n'.join(lines_in) + '\n'

    # Build output
    lines_out = []
    for case_idx, (s, k) in enumerate(cases):
        alpha = solve_case(s, k)
        lines_out.append(f"Case {case_idx + 1}: {alpha}")
    output_text = '\n'.join(lines_out) + '\n'

    in_path = os.path.join(BASE_DIR, f"{prefix}.in")
    out_path = os.path.join(BASE_DIR, f"{prefix}.out")

    with open(in_path, 'w') as f:
        f.write(input_text)
    with open(out_path, 'w') as f:
        f.write(output_text)

    print(f"Test {prefix}: {len(cases)} cases written")

print(f"\nTotal: {len(test_files)} test files")
