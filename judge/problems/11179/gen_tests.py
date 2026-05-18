import random
import bisect
import os

def solve_cases(input_text):
    """Run the solution logic and return list of answers."""
    tokens = input_text.split()
    idx = 0
    results = []
    while idx < len(tokens):
        n = int(tokens[idx]); idx += 1
        a = []
        for i in range(n):
            a.append(int(tokens[idx])); idx += 1

        # LIS ending at each position (from left)
        lis = [0] * n
        tails = []
        for i in range(n):
            pos = bisect.bisect_left(tails, a[i])
            if pos == len(tails):
                tails.append(a[i])
            else:
                tails[pos] = a[i]
            lis[i] = pos + 1

        # LDS ending at each position (from right) = LIS from right
        lds = [0] * n
        tails = []
        for i in range(n - 1, -1, -1):
            pos = bisect.bisect_left(tails, a[i])
            if pos == len(tails):
                tails.append(a[i])
            else:
                tails[pos] = a[i]
            lds[i] = pos + 1

        ans = 1
        for i in range(n):
            w = 2 * min(lis[i], lds[i]) - 1
            if w > ans:
                ans = w
        results.append(str(ans))
    return results


def make_case_lines(cases):
    """Given list of (n, list_of_ints), produce input lines."""
    lines = []
    for n, arr in cases:
        lines.append(str(n))
        lines.append(' '.join(map(str, arr)))
    return '\n'.join(lines) + '\n'


def write_test(test_id, cases, outdir):
    inp = make_case_lines(cases)
    answers = solve_cases(inp)
    out = '\n'.join(answers) + '\n'
    fname_in = os.path.join(outdir, f"{test_id:02d}.in")
    fname_out = os.path.join(outdir, f"{test_id:02d}.out")
    with open(fname_in, 'w') as f:
        f.write(inp)
    with open(fname_out, 'w') as f:
        f.write(out)
    print(f"Test {test_id:02d}: {len(cases)} case(s), answers={answers}")


outdir = '/Users/lambert/Documents/GPE-Helper/judge/problems/11179/testcases'
os.makedirs(outdir, exist_ok=True)

tid = 1

# ============================================================
# Test 01: Sample input
# ============================================================
cases = [
    (10, [1, 2, 3, 4, 5, 4, 3, 2, 1, 10]),
    (19, [1, 2, 3, 2, 1, 2, 3, 4, 3, 2, 1, 5, 4, 1, 2, 3, 2, 2, 1]),
    (5, [1, 2, 3, 4, 5]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 02: Single element (minimum N)
# ============================================================
cases = [
    (1, [42]),
    (1, [1]),
    (1, [10000]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 03: Two elements
# ============================================================
cases = [
    (2, [1, 2]),
    (2, [2, 1]),
    (2, [5, 5]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 04: Three elements - minimal wavio
# ============================================================
cases = [
    (3, [1, 3, 2]),    # wavio of length 3
    (3, [1, 2, 3]),    # strictly increasing, answer 1
    (3, [3, 2, 1]),    # strictly decreasing, answer 1
    (3, [5, 5, 5]),    # all same, answer 1
    (3, [1, 3, 1]),    # perfect wavio length 3
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 05: All same elements
# ============================================================
cases = [
    (5, [7, 7, 7, 7, 7]),
    (10, [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 06: Strictly increasing / strictly decreasing
# ============================================================
cases = [
    (10, list(range(1, 11))),
    (10, list(range(10, 0, -1))),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 07: Perfect wavio sequences
# ============================================================
# 1 2 3 4 5 4 3 2 1 => length 9
cases = [
    (9, [1, 2, 3, 4, 5, 4, 3, 2, 1]),
    (5, [1, 3, 5, 3, 1]),
    (7, [10, 20, 30, 40, 30, 20, 10]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 08: Wavio at different positions
# ============================================================
# Wavio at the beginning
cases = [
    (10, [1, 5, 3, 2, 2, 2, 2, 2, 2, 2]),  # wavio 1,5,3 = 3 at start
    (10, [2, 2, 2, 2, 2, 2, 2, 1, 5, 3]),  # wavio 1,5,3 = 3 at end
    (10, [2, 2, 2, 1, 5, 3, 2, 2, 2, 2]),  # wavio 1,5,3 = 3 in middle
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 09: V-shape (decreasing then increasing) - answer should be 1
# ============================================================
cases = [
    (7, [7, 5, 3, 1, 3, 5, 7]),   # V-shape, no wavio > 1
    (9, [9, 7, 5, 3, 1, 3, 5, 7, 9]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 10: Zigzag pattern
# ============================================================
cases = [
    (10, [1, 10, 1, 10, 1, 10, 1, 10, 1, 10]),
    (11, [1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 11: Large values
# ============================================================
cases = [
    (7, [1000000000, 999999999, 1000000000, 999999998, 999999999, 1000000000, 999999997]),
    (5, [2147483647, 2147483646, 2147483647, 2147483646, 2147483645]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 12: Multiple wavio subsequences of same length
# ============================================================
cases = [
    (15, [1, 2, 3, 2, 1, 1, 2, 3, 2, 1, 1, 2, 3, 2, 1]),
    (11, [1, 3, 5, 7, 9, 7, 5, 3, 1, 3, 5]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 13: Medium random cases
# ============================================================
random.seed(42)
cases = []
for _ in range(5):
    n = random.randint(50, 200)
    arr = [random.randint(1, 100) for _ in range(n)]
    cases.append((n, arr))
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 14: Larger random cases
# ============================================================
random.seed(123)
cases = []
for _ in range(3):
    n = random.randint(500, 2000)
    arr = [random.randint(1, 10000) for _ in range(n)]
    cases.append((n, arr))
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 15: Near-maximum N with multiple test cases
# ============================================================
random.seed(456)
cases = []
for _ in range(3):
    n = random.randint(3000, 5000)
    arr = [random.randint(1, 100000) for _ in range(n)]
    cases.append((n, arr))
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 16: Maximum N = 10000
# ============================================================
random.seed(789)
n = 10000
arr = [random.randint(1, 1000000) for _ in range(n)]
cases = [(n, arr)]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 17: N=10000 with small value range (many duplicates)
# ============================================================
random.seed(101)
n = 10000
arr = [random.randint(1, 50) for _ in range(n)]
cases = [(n, arr)]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 18: Constructed large wavio inside noise
# ============================================================
random.seed(202)
n = 5000
# Build a wavio of length ~201 (100 up, peak, 100 down) embedded in random data
arr = [random.randint(1, 50) for _ in range(n)]
# Place an increasing sequence then decreasing
base = 1000
for i in range(101):
    arr[2000 + i] = base + i * 10          # increasing from 1000 to 2000
for i in range(100):
    arr[2101 + i] = base + 1000 - (i+1)*10  # decreasing from 1990 to 1010
# The wavio around index 2100 should be quite long
cases = [(n, arr)]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 19: Negative numbers (problem says integers, could be negative)
# Actually the problem says "positive integer N" and "N integers" -
# let's use values that include negatives to be safe
# ============================================================
cases = [
    (9, [-5, -3, -1, 0, 5, 0, -1, -3, -5]),
    (7, [-10, -5, 0, 10, 0, -5, -10]),
    (5, [-1, -2, -3, -4, -5]),
]
write_test(tid, cases, outdir); tid += 1

# ============================================================
# Test 20: Many small test cases (stress)
# ============================================================
random.seed(303)
cases = []
for _ in range(70):  # up to 75 test cases allowed
    n = random.randint(1, 100)
    arr = [random.randint(1, 1000) for _ in range(n)]
    cases.append((n, arr))
write_test(tid, cases, outdir); tid += 1

print("\nAll test cases generated successfully!")
