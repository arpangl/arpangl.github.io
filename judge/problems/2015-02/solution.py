import sys

# f(n) = 3*f(n-1) + 4, f(1) = 1
# MOD = 10^9 + 9
#
# Closed form: f(n) = 3*f(n-1) + 4
# The homogeneous solution: f(n) = A * 3^n
# Particular solution: f(n) = c => c = 3c + 4 => c = -2
# General: f(n) = A * 3^n - 2
# f(1) = 3A - 2 = 1 => A = 1
# So f(n) = 3^n - 2
#
# Therefore f(n) mod (10^9+9) = (pow(3, n, MOD) - 2) % MOD
#
# Alternatively, use matrix exponentiation:
# [f(n)]   = [3 4] ^ (n-1) * [f(1)]   = [3 4]^(n-1) * [1]
# [  1 ]     [0 1]           [  1 ]     [0 1]          [1]
#
# But the closed form is simpler and correct.

MOD = 10**9 + 9

def solve(n):
    # f(n) = 3^n - 2 (mod MOD)
    return (pow(3, n, MOD) - 2) % MOD

# Verify with sample
assert solve(1) == 1
assert solve(2) == 7
assert solve(3) == 25
assert solve(4) == 79

# Also verify by brute force for small values
def brute(n):
    f = 1
    for i in range(2, n+1):
        f = 3*f + 4
    return f % MOD

for i in range(1, 30):
    assert solve(i) == brute(i), f"Mismatch at n={i}: solve={solve(i)}, brute={brute(i)}"

print("All assertions passed!")

# Now generate test cases
import os

testcases_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/2015-02/testcases"

# Design test cases:
# 01: Sample input
# 02: n=1 (minimum)
# 03: Small values
# 04: Medium values
# 05: Powers of 2
# 06: Large n near 2^63
# 07: n = 2^63 - 1 (maximum)
# 08: Various large values
# 09: n where result is 0 (if possible: 3^n ≡ 2 mod MOD)
# 10-15: Random mix, edge cases, stress with 1000 test cases

import random
random.seed(42)

MAX_N = 2**63 - 1

test_cases = []

# TC 01: Sample
tc01 = [1, 2, 3, 4]
test_cases.append(("01", tc01))

# TC 02: Single minimum n=1
tc02 = [1]
test_cases.append(("02", tc02))

# TC 03: Small consecutive values
tc03 = list(range(1, 21))
test_cases.append(("03", tc03))

# TC 04: Medium values
tc04 = [50, 100, 500, 1000, 5000, 10000, 100000, 1000000]
test_cases.append(("04", tc04))

# TC 05: Powers of 2
tc05 = [2**i for i in range(0, 63)]
test_cases.append(("05", tc05))

# TC 06: Near 2^63-1 (maximum)
tc06 = [MAX_N, MAX_N - 1, MAX_N - 2, MAX_N - 100, MAX_N - 999]
test_cases.append(("06", tc06))

# TC 07: Single maximum n = 2^63 - 1
tc07 = [MAX_N]
test_cases.append(("07", tc07))

# TC 08: Powers of 3 and 10
tc08 = [3**i for i in range(1, 20) if 3**i < MAX_N] + [10**i for i in range(1, 19) if 10**i < MAX_N]
test_cases.append(("08", tc08))

# TC 09: Values around MOD
tc09 = [MOD - 1, MOD, MOD + 1, MOD * 2, MOD * 2 + 1, 2 * MOD - 1]
# filter valid ones (0 < n < 2^63)
tc09 = [n for n in tc09 if 0 < n < 2**63]
test_cases.append(("09", tc09))

# TC 10: Random small (1-1000)
tc10 = sorted(random.sample(range(1, 1001), 50))
test_cases.append(("10", tc10))

# TC 11: Random medium (1000-10^9)
tc11 = sorted([random.randint(1000, 10**9) for _ in range(50)])
test_cases.append(("11", tc11))

# TC 12: Random large (10^9 - 2^63-1)
tc12 = sorted([random.randint(10**9, MAX_N) for _ in range(50)])
test_cases.append(("12", tc12))

# TC 13: n=1 repeated (edge case: many same values)
tc13 = [1] * 100
test_cases.append(("13", tc13))

# TC 14: Stress test - 1000 random values (max test cases)
tc14 = [random.randint(1, MAX_N) for _ in range(1000)]
test_cases.append(("14", tc14))

# TC 15: Special values - Fibonacci-like indices, primes, etc.
primes_small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
large_primes = [999999937, 999999929, 999999893, 999999883, 999999877]
tc15 = primes_small + large_primes + [2**62, 2**62 + 1, 2**61 - 1, 2**60]
test_cases.append(("15", tc15))

# TC 16: Mix of edge and random
tc16 = [1, 2, MAX_N, MAX_N - 1, 10**18, 10**17, 10**16, 123456789012345678]
test_cases.append(("16", tc16))

# TC 17: Consecutive around interesting boundaries
tc17 = list(range(1, 11)) + [10**9 + 7, 10**9 + 8, 10**9 + 9, 10**9 + 10] + [MAX_N - i for i in range(5)]
test_cases.append(("17", tc17))

# TC 18: Single large value
tc18 = [5846293710583746291]  # random large
test_cases.append(("18", tc18))

# Write all test cases
for name, inputs in test_cases:
    in_path = os.path.join(testcases_dir, f"{name}.in")
    out_path = os.path.join(testcases_dir, f"{name}.out")

    with open(in_path, 'w') as fin:
        for n in inputs:
            fin.write(f"{n}\n")

    with open(out_path, 'w') as fout:
        for n in inputs:
            fout.write(f"{solve(n)}\n")

print(f"Generated {len(test_cases)} test cases.")

# Verify by reading back
for name, inputs in test_cases:
    in_path = os.path.join(testcases_dir, f"{name}.in")
    out_path = os.path.join(testcases_dir, f"{name}.out")

    with open(in_path) as f:
        in_lines = f.read().strip().split('\n')
    with open(out_path) as f:
        out_lines = f.read().strip().split('\n')

    assert len(in_lines) == len(out_lines), f"TC {name}: line count mismatch"

    for i, (il, ol) in enumerate(zip(in_lines, out_lines)):
        n = int(il)
        expected = solve(n)
        actual = int(ol)
        assert expected == actual, f"TC {name} line {i}: expected {expected}, got {actual}"

print("All test cases verified!")
