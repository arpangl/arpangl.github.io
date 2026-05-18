#!/usr/bin/env python3
"""Generate test cases for problem 10679: Irreducible Basic Fractions."""

import os
import random

def euler_totient(n):
    if n == 1:
        return 1
    result = n
    temp = n
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def make_test(test_id, values, outdir):
    """Write a single test case. values is a list of n (without the trailing 0)."""
    in_path = os.path.join(outdir, f"{test_id:02d}.in")
    out_path = os.path.join(outdir, f"{test_id:02d}.out")

    in_lines = [str(v) for v in values] + ["0"]
    out_lines = [str(euler_totient(v)) for v in values]

    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f"Test {test_id:02d}: {len(values)} value(s), range [{min(values)}, {max(values)}]")

outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10679/testcases"

test_id = 1

# --- Test 01: Sample from problem ---
make_test(test_id, [12, 123456, 7654321], outdir)
test_id += 1

# --- Test 02: n=1 (edge: phi(1)=1) ---
make_test(test_id, [1], outdir)
test_id += 1

# --- Test 03: n=2 (smallest prime, phi(2)=1) ---
make_test(test_id, [2], outdir)
test_id += 1

# --- Test 04: Small primes (phi(p) = p-1) ---
make_test(test_id, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], outdir)
test_id += 1

# --- Test 05: Powers of 2 (phi(2^k) = 2^(k-1)) ---
vals = [2**k for k in range(1, 30) if 2**k < 1000000000]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 06: Powers of small primes ---
vals = []
for p in [3, 5, 7, 11]:
    k = 1
    while p**k < 1000000000:
        vals.append(p**k)
        k += 1
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 07: Products of two primes (semiprimes) ---
vals = [6, 10, 14, 15, 21, 35, 77, 143, 221, 323]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 08: Highly composite numbers ---
vals = [1, 2, 4, 6, 12, 24, 36, 48, 60, 120, 180, 240, 360, 720, 1260, 2520, 5040, 10080, 25200, 55440]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 09: Large primes near 10^9 ---
# These are known primes < 10^9
large_primes = [999999937, 999999893, 999999877, 999999613, 999999541]
make_test(test_id, large_primes, outdir)
test_id += 1

# --- Test 10: Values near upper bound (999999999) ---
vals = [999999999, 999999998, 999999997, 999999996, 999999995]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 11: n with very many small prime factors ---
# 2*3*5*7*11*13*17*19*23 = 223092870
vals = [
    2*3*5*7*11*13*17*19*23,   # 223092870
    2*3*5*7*11*13*17*19,       # 9699690
    2*3*5*7*11*13*17,          # 510510
    2*3*5*7*11*13,             # 30030
    2*3*5*7*11,                # 2310
    2*3*5*7,                   # 210
    2*3*5,                     # 30
    2*3,                       # 6
]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 12: Perfect squares ---
vals = [4, 9, 25, 49, 121, 169, 289, 529, 961, 10000, 1000000, 100000000]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 13: Consecutive integers ---
vals = list(range(1, 21))
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 14: Random medium values ---
random.seed(42)
vals = sorted(random.sample(range(1, 1000000), 20))
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 15: Random large values ---
random.seed(123)
vals = [random.randint(1, 999999999) for _ in range(20)]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 16: Single large value (max-1) ---
make_test(test_id, [999999999], outdir)
test_id += 1

# --- Test 17: Powers of 10 ---
vals = [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
make_test(test_id, vals, outdir)
test_id += 1

# --- Test 18: Fibonacci-like numbers < 10^9 ---
fibs = [1, 2]
while True:
    nxt = fibs[-1] + fibs[-2]
    if nxt >= 1000000000:
        break
    fibs.append(nxt)
make_test(test_id, fibs, outdir)
test_id += 1

print(f"\nGenerated {test_id - 1} test cases.")
