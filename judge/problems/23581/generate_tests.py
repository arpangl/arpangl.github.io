#!/usr/bin/env python3
"""
Generate test cases for Glass Beads (problem 23581).
Creates 20 test cases covering edge cases and corner cases.
"""

import random
import string
import os

# Booth's algorithm for computing correct answers
def booth(s):
    s2 = s + s
    n = len(s)
    f = [-1] * (2 * n)
    k = 0
    for j in range(1, 2 * n):
        sj = s2[j]
        i = f[j - 1 - k]
        while i != -1 and sj != s2[k + i + 1]:
            if sj < s2[k + i + 1]:
                k = j - i - 1
            i = f[i]
        if sj != s2[k + i + 1]:
            if sj < s2[k]:
                k = j
            f[j - k] = -1
        else:
            f[j - k] = i + 1
    return k

# Brute-force verification for small cases
def brute_force(s):
    n = len(s)
    best = 0
    for i in range(1, n):
        rot_i = s[i:] + s[:i]
        rot_best = s[best:] + s[:best]
        if rot_i < rot_best:
            best = i
    return best

def generate_and_verify(test_cases):
    """Verify all test cases using both Booth and brute force (for small ones)."""
    results = []
    for s in test_cases:
        ans = booth(s)
        # Brute-force verify for strings up to length 5000
        if len(s) <= 5000:
            bf = brute_force(s)
            assert ans == bf, f"Mismatch for '{s[:50]}...': booth={ans}, brute={bf}"
        results.append(ans + 1)  # 1-indexed
    return results


def main():
    random.seed(42)

    test_cases = []

    # --- Edge Cases ---

    # 1. Single character
    test_cases.append("a")

    # 2. Two identical characters
    test_cases.append("aa")

    # 3. Two different characters
    test_cases.append("ba")

    # 4. All same characters
    test_cases.append("aaaaaaaaaa")

    # 5. Already smallest rotation at position 1
    test_cases.append("abcdefghij")

    # 6. Smallest rotation at the last position
    test_cases.append("bcdefghija")

    # 7. Sample: helloworld
    test_cases.append("helloworld")

    # 8. Sample: amandamanda
    test_cases.append("amandamanda")

    # 9. Repeated pattern - "abcabc"
    test_cases.append("abcabc")

    # 10. Descending order (smallest is last char)
    test_cases.append("zyxwvutsrqponmlkjihgfedcba")

    # 11. All 'z' except one 'a' at the end
    test_cases.append("z" * 99 + "a")

    # 12. Alternating characters with tie-breaking
    test_cases.append("ababababab")

    # 13. String where multiple rotations start with 'a' but differ later
    test_cases.append("aabaabaac")

    # 14. Large string of all same character (10000)
    test_cases.append("a" * 10000)

    # 15. Large random string (10000 chars, full alphabet)
    test_cases.append(''.join(random.choice(string.ascii_lowercase) for _ in range(10000)))

    # 16. Large string with only 2 characters making many near-ties
    s = ''.join(random.choice("ab") for _ in range(10000))
    test_cases.append(s)

    # 17. Nearly sorted large string with a twist at the end
    s = "abcdefghijklmnopqrstuvwxyz" * 384 + "abcdefghijklmnop"  # 26*384+16 = 10000
    test_cases.append(s)

    # 18. Worst case for naive: long runs of 'a' with one 'b'
    test_cases.append("a" * 9999 + "b")

    # 19. String with periodic pattern that's tricky: "abab...abc"
    s = "ab" * 4999 + "ac"
    test_cases.append(s)

    # 20. Random medium string (500 chars, small alphabet a-d)
    test_cases.append(''.join(random.choice("abcd") for _ in range(500)))

    # Verify all test cases
    results = generate_and_verify(test_cases)

    # Write test cases
    base_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/23581/testcases"

    for i, (tc, ans) in enumerate(zip(test_cases, results), start=1):
        in_file = os.path.join(base_dir, f"{i:02d}.in")
        out_file = os.path.join(base_dir, f"{i:02d}.out")

        # Each .in file has: first line = 1 (number of cases), second line = the string
        with open(in_file, 'w') as f:
            f.write(f"1\n{tc}\n")

        with open(out_file, 'w') as f:
            f.write(f"{ans}\n")

        print(f"Test {i:02d}: len={len(tc):>5}, answer={ans}")

    print(f"\nGenerated {len(test_cases)} test cases successfully.")
    print("All test cases verified against brute force (where applicable).")


if __name__ == '__main__':
    main()
