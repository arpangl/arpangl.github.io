#!/usr/bin/env python3
"""
Generate test cases for Problem 11028: Digit Primes

A digit prime is a prime number whose digit sum is also prime.
Given queries [t1, t2], count digit primes in range [t1, t2] inclusive.

Constraints: 0 < t1 <= t2 < 1000000
"""

import os

LIMIT = 1000000

# Step 1: Sieve of Eratosthenes up to LIMIT
def sieve(n):
    is_prime = [False, False] + [True] * (n - 1)
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return is_prime

def digit_sum(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s

print("Building sieve...")
is_prime = sieve(LIMIT)

# Step 2: Identify digit primes
# A digit prime: is_prime[n] and is_prime[digit_sum(n)]
# Max digit sum for 999999 = 9*6 = 54, so our sieve covers it.
is_digit_prime = [False] * LIMIT
for i in range(2, LIMIT):
    if is_prime[i] and is_prime[digit_sum(i)]:
        is_digit_prime[i] = True

# Step 3: Build prefix sum for O(1) range queries
# prefix[i] = number of digit primes in [1, i]
prefix = [0] * LIMIT
for i in range(1, LIMIT):
    prefix[i] = prefix[i - 1] + (1 if is_digit_prime[i] else 0)

def count_digit_primes(t1, t2):
    """Count digit primes in [t1, t2] inclusive."""
    return prefix[t2] - prefix[t1 - 1]

# Verify with sample input/output
assert count_digit_primes(10, 20) == 1, f"Expected 1, got {count_digit_primes(10, 20)}"
assert count_digit_primes(10, 100) == 10, f"Expected 10, got {count_digit_primes(10, 100)}"
assert count_digit_primes(100, 10000) == 576, f"Expected 576, got {count_digit_primes(100, 10000)}"
print("Sample cases verified!")

# Let's also print what digit primes are in [10,20] for sanity check
dps_10_20 = [i for i in range(10, 21) if is_digit_prime[i]]
print(f"Digit primes in [10,20]: {dps_10_20}")
# 11: prime, digit_sum=2 (prime) -> YES. That's the only one.

# Step 4: Define test cases
# Format: list of (description, [(t1, t2), ...])
test_cases = []

# TC 01: Sample input from problem
test_cases.append(("Sample from problem", [(10, 20), (10, 100), (100, 10000)]))

# TC 02: Single number that IS a digit prime (2: prime, digit_sum=2 prime)
test_cases.append(("Single digit prime", [(2, 2)]))

# TC 03: Single number that is NOT a digit prime (4: not prime)
test_cases.append(("Single non-digit-prime", [(4, 4)]))

# TC 04: Single number = 1 (not prime)
test_cases.append(("t1=t2=1", [(1, 1)]))

# TC 05: Very small range at start [1, 10]
test_cases.append(("Small range [1,10]", [(1, 10)]))

# TC 06: Small primes range [2, 50]
test_cases.append(("Small primes range [2,50]", [(2, 50)]))

# TC 07: Range with no digit primes - find one
# Primes in [24,28]: none (24,25,26,27,28 are all composite). So 0 digit primes.
test_cases.append(("Range with no digit primes [24,28]", [(24, 28)]))

# TC 08: Range [1, 999999] - full range
test_cases.append(("Full range", [(1, 999999)]))

# TC 09: Boundary at 999999
test_cases.append(("Boundary near max", [(999990, 999999)]))

# TC 10: Large range [1, 500000]
test_cases.append(("Large range [1,500000]", [(1, 500000)]))

# TC 11: Multiple queries including edge cases
test_cases.append(("Mixed queries", [
    (1, 1),
    (2, 2),
    (3, 3),
    (5, 5),
    (7, 7),
    (11, 11),
    (17, 17),  # 1+7=8, not prime
    (41, 41),  # 4+1=5, prime -> digit prime
    (1, 999999),
]))

# TC 12: Range of composites [8, 10] - 8,9,10 all composite
test_cases.append(("All composites [8,10]", [(8, 10)]))

# TC 13: Ranges around 100s
test_cases.append(("Around hundreds", [
    (100, 200),
    (200, 300),
    (300, 400),
    (900, 1000),
]))

# TC 14: Large number of queries (stress test, but keep reasonable for test data)
import random
random.seed(42)
stress_queries = []
for _ in range(50):
    a = random.randint(1, 999998)
    b = random.randint(a, min(a + random.randint(0, 500000), 999999))
    stress_queries.append((a, b))
test_cases.append(("Stress test 50 queries", stress_queries))

# TC 15: Ranges where t1=t2 for various primes and non-primes
single_checks = []
for v in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]:
    single_checks.append((v, v))
test_cases.append(("Single value checks for small primes", single_checks))

# TC 16: Near boundary values
test_cases.append(("Near boundaries", [
    (999997, 999999),  # 999997 is prime? check
    (999979, 999979),  # 999979 is prime
    (1, 2),
    (1, 3),
    (999998, 999999),
]))

# TC 17: Medium ranges
test_cases.append(("Medium ranges", [
    (10000, 20000),
    (50000, 60000),
    (100000, 200000),
    (500000, 600000),
    (800000, 900000),
]))

# TC 18: Range with no digit primes in composite zone
# [114, 120]: 114=2*57, 115=5*23, 116=4*29, 117=9*13, 118=2*59, 119=7*17, 120=2^3*3*5
# All composite -> 0 digit primes
test_cases.append(("Composite zone [114,120]", [(114, 120)]))

# TC 19: Interesting edge - range [2, 3]
test_cases.append(("Tiny range [2,3]", [(2, 3), (2, 5), (2, 7), (2, 11), (2, 13)]))

# TC 20: Multiple large ranges
test_cases.append(("Multiple large ranges", [
    (1, 100000),
    (100001, 200000),
    (200001, 300000),
    (300001, 400000),
    (400001, 500000),
    (500001, 600000),
    (600001, 700000),
    (700001, 800000),
    (800001, 900000),
    (900001, 999999),
]))

# Step 5: Write test case files
outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/11028/testcases"

for idx, (desc, queries) in enumerate(test_cases, 1):
    fname = f"{idx:02d}"

    # Build input
    lines_in = [str(len(queries))]
    for t1, t2 in queries:
        lines_in.append(f"{t1} {t2}")
    input_data = "\n".join(lines_in) + "\n"

    # Build output
    lines_out = []
    for t1, t2 in queries:
        lines_out.append(str(count_digit_primes(t1, t2)))
    output_data = "\n".join(lines_out) + "\n"

    with open(os.path.join(outdir, f"{fname}.in"), "w") as f:
        f.write(input_data)
    with open(os.path.join(outdir, f"{fname}.out"), "w") as f:
        f.write(output_data)

    print(f"TC {fname}: {desc} ({len(queries)} queries)")

print(f"\nGenerated {len(test_cases)} test cases.")

# Print some useful stats
total_dp = prefix[LIMIT - 1]
print(f"Total digit primes in [1, 999999]: {total_dp}")
