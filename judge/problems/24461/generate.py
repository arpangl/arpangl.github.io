#!/usr/bin/env python3
"""
Generate test cases for Sum of Consecutive Prime Numbers.
Constraints: N is between 2 and 10000, inclusive. Input ends with 0.
"""

import os
import random
from solve import sieve, count_representations, PRIMES, solve

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/24461/testcases"

def generate_test_cases():
    """Generate 18 test cases covering edge cases and corner cases."""

    test_cases = []

    # --- Test 1: Sample input (exact from problem) ---
    test_cases.append(("Sample input from problem", [2, 3, 17, 41, 20, 666, 12, 53]))

    # --- Test 2: Minimum value - single value 2 ---
    test_cases.append(("Minimum value: 2", [2]))

    # --- Test 3: Small primes that are themselves consecutive prime sums ---
    test_cases.append(("Small primes (each is at least 1 representation)", [2, 3, 5, 7, 11, 13]))

    # --- Test 4: Numbers with 0 representations ---
    # Find numbers in range [2,100] with 0 representations
    zeros = []
    for n in range(2, 101):
        if count_representations(n) == 0:
            zeros.append(n)
    test_cases.append(("Numbers with 0 representations", zeros[:15]))

    # --- Test 5: Numbers with high representation counts ---
    # Scan all numbers 2..10000 for those with the most representations
    best = []
    for n in range(2, 10001):
        c = count_representations(n)
        best.append((c, n))
    best.sort(reverse=True)
    high_rep_numbers = [n for c, n in best[:15]]
    test_cases.append(("Numbers with highest representation counts", high_rep_numbers))

    # --- Test 6: Maximum value 10000 ---
    test_cases.append(("Maximum value: 10000", [10000]))

    # --- Test 7: Values near the maximum boundary ---
    test_cases.append(("Near max boundary", [9999, 9998, 9997, 9996, 10000]))

    # --- Test 8: All values that are single primes up to 50 ---
    small_primes = [p for p in PRIMES if p <= 50]
    test_cases.append(("All primes up to 50", small_primes))

    # --- Test 9: Consecutive even numbers (many will have 0 reps) ---
    test_cases.append(("Even numbers", [4, 6, 8, 10, 14, 16, 18, 20, 22, 24]))

    # --- Test 10: Sum of first k primes for various k ---
    prefix_sums = []
    s = 0
    for i in range(20):
        s += PRIMES[i]
        if s <= 10000:
            prefix_sums.append(s)
    test_cases.append(("Prefix sums of primes (sum of first k primes)", prefix_sums))

    # --- Test 11: Numbers that are exactly 2+3+...+p for some prime p ---
    # These should have at least 1 representation starting from 2
    test_cases.append(("Sums starting from 2", prefix_sums[:10]))

    # --- Test 12: Large primes (should have exactly 1 representation) ---
    large_primes = [p for p in PRIMES if p > 9000]
    test_cases.append(("Large primes near 10000", large_primes))

    # --- Test 13: Single input then zero ---
    test_cases.append(("Single input: 5", [5]))

    # --- Test 14: Random values across the full range ---
    random.seed(24461)
    rand_vals = sorted(random.sample(range(2, 10001), 20))
    test_cases.append(("Random values across range", rand_vals))

    # --- Test 15: Powers of 2 in range ---
    powers_of_2 = [2**k for k in range(1, 14) if 2**k <= 10000]
    test_cases.append(("Powers of 2", powers_of_2))

    # --- Test 16: Composite numbers that happen to be sums of consecutive primes ---
    composites_with_reps = []
    for n in range(4, 200):
        if not any(n == p for p in PRIMES):
            c = count_representations(n)
            if c > 0:
                composites_with_reps.append(n)
    test_cases.append(("Composite numbers with representations", composites_with_reps[:15]))

    # --- Test 17: Stress test - many queries ---
    random.seed(17)
    stress_vals = [random.randint(2, 10000) for _ in range(50)]
    test_cases.append(("Stress test: 50 random queries", stress_vals))

    # --- Test 18: Edge: value 2 (smallest prime, exactly 1 rep) and value 3 ---
    test_cases.append(("Smallest values: 2 and 3", [2, 3]))

    # Write test cases
    for idx, (desc, values) in enumerate(test_cases, 1):
        in_file = os.path.join(TESTCASE_DIR, f"{idx:02d}.in")
        out_file = os.path.join(TESTCASE_DIR, f"{idx:02d}.out")

        # Build input
        input_lines = [str(v) for v in values] + ["0"]
        input_text = "\n".join(input_lines) + "\n"

        # Compute output
        output_text = solve(input_text)

        with open(in_file, 'w') as f:
            f.write(input_text)
        with open(out_file, 'w') as f:
            f.write(output_text + "\n")

        # Print summary
        print(f"Test {idx:02d}: {desc}")
        print(f"  Input ({len(values)} queries): {values[:5]}{'...' if len(values) > 5 else ''}")
        in_lines = input_text.strip().split('\n')
        out_lines = output_text.strip().split('\n')
        print(f"  Output preview: {out_lines[:5]}{'...' if len(out_lines) > 5 else ''}")
        print()

if __name__ == '__main__':
    generate_test_cases()
