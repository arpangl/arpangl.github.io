#!/usr/bin/env python3
"""
Generate test cases for Problem 10582: Power Strings

The problem: Given a string s, find the largest n such that s = a^n.
Input is lines of strings, terminated by a line with just ".".
Each line produces one output line with the integer n.

We use the KMP failure function approach:
  If len(s) % (len(s) - fail[len(s)-1] - 1) == 0, then n = len(s) // (len(s) - fail[len(s)-1] - 1)
  Otherwise n = 1.
But for correctness we just use a straightforward divisor-checking approach.
"""

import os
import random
import string

OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10582/testcases"


def solve_one(s):
    """Find the largest n such that s = a^n for some string a."""
    n = len(s)
    # Try all divisors of n from smallest period length upward
    # We want the LARGEST n, so we want the SMALLEST period.
    for period in range(1, n + 1):
        if n % period != 0:
            continue
        base = s[:period]
        reps = n // period
        if base * reps == s:
            return reps
    return 1


def solve(input_text):
    """Process full input (multiple lines terminated by '.') and return output."""
    lines = input_text.split('\n')
    results = []
    for line in lines:
        line = line.rstrip('\r\n')
        if line == '.':
            break
        if line == '':
            continue
        results.append(str(solve_one(line)))
    return '\n'.join(results) + '\n'


def write_case(case_num, strings):
    """Write a test case: list of strings -> XX.in / XX.out"""
    in_lines = strings + ['.']
    in_text = '\n'.join(in_lines) + '\n'
    out_text = solve(in_text)

    prefix = f"{case_num:02d}"
    in_path = os.path.join(OUTDIR, f"{prefix}.in")
    out_path = os.path.join(OUTDIR, f"{prefix}.out")

    with open(in_path, 'w') as f:
        f.write(in_text)
    with open(out_path, 'w') as f:
        f.write(out_text)

    # Print summary
    out_lines = out_text.strip().split('\n')
    print(f"Case {prefix}: {len(strings)} string(s)")
    for i, s in enumerate(strings):
        display = s if len(s) <= 60 else s[:57] + "..."
        print(f"  \"{display}\" (len={len(s)}) -> {out_lines[i]}")


def rand_lower(n):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))


def rand_printable(n):
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(chars) for _ in range(n))


if __name__ == '__main__':
    random.seed(42)
    case = 1

    # -------------------------------------------------------------------
    # Case 01: Sample from problem statement
    # -------------------------------------------------------------------
    write_case(case, ["abcd", "aaaa", "ababab"])
    case += 1

    # -------------------------------------------------------------------
    # Case 02: Single character strings
    # -------------------------------------------------------------------
    write_case(case, ["a", "z", "A", "1"])
    case += 1

    # -------------------------------------------------------------------
    # Case 03: All same characters (various lengths)
    # -------------------------------------------------------------------
    write_case(case, [
        "aa",          # 2
        "aaa",         # 3
        "aaaa",        # 4
        "a" * 7,       # prime length 7
        "a" * 12,      # composite 12
        "a" * 100,     # 100
        "b" * 997,     # prime length
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 04: No repetition (answer = 1) -- distinct strings
    # -------------------------------------------------------------------
    write_case(case, [
        "abcde",
        "abcdefghij",
        "xyz",
        "abcdefghijklmnopqrstuvwxyz",  # 26 chars, no repeat pattern
        "abacaba",  # len=7 prime, not periodic
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 05: Simple repeat patterns
    # -------------------------------------------------------------------
    write_case(case, [
        "abab",       # ab * 2
        "abcabc",     # abc * 2
        "xyzxyzxyz",  # xyz * 3
        "abababab",   # ab * 4
        "abaaba",     # This is NOT aba*2 (abaaba = "aba"+"aba" -> yes! 2)
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 06: Prime length strings (answer is 1 or the length itself if single char)
    # -------------------------------------------------------------------
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    strs6 = []
    for p in primes:
        # All same char -> answer = p
        strs6.append("a" * p)
    for p in [5, 7, 11, 13]:
        # Random string of prime length -> likely answer = 1
        strs6.append(rand_lower(p))
    write_case(case, strs6)
    case += 1

    # -------------------------------------------------------------------
    # Case 07: Composite length with patterns that DO repeat
    # -------------------------------------------------------------------
    write_case(case, [
        "ab" * 6,       # len=12, answer=6
        "abc" * 4,      # len=12, answer=4
        "abcd" * 3,     # len=12, answer=3
        "abcdef" * 2,   # len=12, answer=2
        "ab" * 50,      # len=100, answer=50
        "abcde" * 20,   # len=100, answer=20
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 08: Composite length but NO repetition (answer=1)
    # -------------------------------------------------------------------
    write_case(case, [
        "abcdefghijkl",            # len=12, answer=1
        "abcdefghijklmnopqrst",    # len=20, answer=1
        "abcdefghijklmnopqrstuvwxyzabcde",  # len=31 prime, answer=1
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 09: Tricky near-repeats (should be 1)
    # -------------------------------------------------------------------
    write_case(case, [
        "aab",         # NOT a repetition
        "aba",         # NOT a repetition
        "abcab",       # len=5, NOT a repetition
        "ababc",       # NOT a repetition
        "aabaabaac",   # NOT "aab"*3 because last is "aac"
        "abcabcabd",   # NOT "abc"*3
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 10: Two-character alphabet stress
    # -------------------------------------------------------------------
    write_case(case, [
        "ab" * 500,          # len=1000, answer=500
        "aabb" * 250,        # len=1000, answer=250
        "aaabbb" * 100,      # len=600, answer=100  (period=6, but 600/6=100... wait "aaabbb" repeated)
        "ab" * 1,            # len=2, answer=1? No, "ab" answer=1. Wait: a^1 = "ab", so n=1
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 11: Longer strings with known repetition
    # -------------------------------------------------------------------
    base11a = "abcdefghij"  # len=10
    base11b = "HelloWorld"  # len=10
    write_case(case, [
        base11a * 100,   # len=1000, answer=100
        base11b * 50,    # len=500, answer=50
        base11a * 1,     # len=10, answer=1
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 12: Large strings - all same char
    # -------------------------------------------------------------------
    write_case(case, [
        "a" * 999983,    # prime length, answer = 999983
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 13: Large string - repeated pattern
    # -------------------------------------------------------------------
    base13 = "abcde"  # len=5
    write_case(case, [
        base13 * 200000,  # len=1000000, answer=200000
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 14: Large string - no repetition
    # -------------------------------------------------------------------
    # Create a string of length ~500000 that is NOT periodic
    s14 = rand_lower(500000)
    # Make sure it's not periodic by appending a unique suffix
    s14 = s14[:-1] + ('z' if s14[-2] != 'z' else 'y')
    write_case(case, [s14])
    case += 1

    # -------------------------------------------------------------------
    # Case 15: Large string with long period (period = 500, repeated 2000 times = 1000000)
    # -------------------------------------------------------------------
    base15 = rand_lower(500)
    write_case(case, [
        base15 * 2000,  # len=1000000, answer=2000
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 16: Mixed - printable characters including spaces and punctuation
    # -------------------------------------------------------------------
    write_case(case, [
        "!@#" * 10,             # len=30, answer=10
        "Hi!" * 5,              # len=15, answer=5
        "a-b-c" * 20,           # len=100, answer=20
        "..." * 3,              # len=9, answer=9 (each '.' repeated)
        "..",                    # len=2, answer=2
        "!@#$%^" * 3,           # len=18, answer=3
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 17: Power-of-two lengths
    # -------------------------------------------------------------------
    write_case(case, [
        "ab" * 1,       # len=2, answer=1
        "ab" * 2,       # len=4, answer=2
        "ab" * 4,       # len=8, answer=4
        "ab" * 8,       # len=16, answer=8
        "ab" * 16,      # len=32, answer=16
        "ab" * 512,     # len=1024, answer=512
        "a" * 1024,     # len=1024, answer=1024
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 18: Strings where answer equals a non-trivial divisor
    # -------------------------------------------------------------------
    # e.g., len=12: divisors are 1,2,3,4,6,12. Build strings for each.
    write_case(case, [
        "abcdefghijkl",         # len=12, answer=1
        "abcdefabcdef",         # len=12, answer=2 (period=6)
        "abcdabcdabcd",         # len=12, answer=3 (period=4)
        "abcabcabcabc",         # len=12, answer=4 (period=3)
        "ababababababab"[:12],   # "abababababab" len=12, answer=6 (period=2)
        "aaaaaaaaaaaa",         # len=12, answer=12 (period=1)
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 19: Large with period = 1 char but huge repetition
    # -------------------------------------------------------------------
    write_case(case, [
        "x" * 1000000,   # answer = 1000000
    ])
    case += 1

    # -------------------------------------------------------------------
    # Case 20: Multiple medium-length strings in one case
    # -------------------------------------------------------------------
    strs20 = []
    for _ in range(20):
        plen = random.choice([2, 3, 5, 7, 10, 13])
        reps = random.randint(1, 50)
        base = rand_lower(plen)
        strs20.append(base * reps)
    write_case(case, strs20)
    case += 1

    print(f"\nGenerated {case - 1} test cases in {OUTDIR}")
