#!/usr/bin/env python3
"""
Generate test cases for problem 10567 - Common Permutation.

For each pair (a, b), the answer is: for each letter c in 'a'..'z',
take min(count(c in a), count(c in b)) copies of c, concatenated in order.
"""

import os
import random
import string
from collections import Counter

TESTCASES_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10567/testcases"

def solve_case(a, b):
    ca = Counter(a)
    cb = Counter(b)
    result = []
    for ch in 'abcdefghijklmnopqrstuvwxyz':
        count = min(ca.get(ch, 0), cb.get(ch, 0))
        result.append(ch * count)
    return ''.join(result)

def solve_all(pairs):
    """Given list of (a, b) pairs, return list of answer strings."""
    return [solve_case(a, b) for a, b in pairs]

def rand_string(length, charset=string.ascii_lowercase):
    return ''.join(random.choice(charset) for _ in range(length))

# Each test case is a list of (a, b) pairs (multiple pairs per file, as per problem format)
test_cases = []

# --- TC 01: Sample input ---
test_cases.append([
    ("pretty", "women"),
    ("walking", "down"),
    ("the", "street"),
])

# --- TC 02: Identical strings ---
test_cases.append([
    ("abcdef", "abcdef"),
    ("aaabbb", "aaabbb"),
    ("zzz", "zzz"),
])

# --- TC 03: No common characters ---
test_cases.append([
    ("abc", "xyz"),
    ("aaa", "bbb"),
    ("mnop", "qrst"),
])

# --- TC 04: Single character strings ---
test_cases.append([
    ("a", "a"),
    ("a", "b"),
    ("z", "z"),
])

# --- TC 05: One empty-like (single char vs multi) ---
test_cases.append([
    ("a", "abcdef"),
    ("abcdef", "f"),
    ("zzz", "z"),
])

# --- TC 06: All same character ---
test_cases.append([
    ("aaaaaaaaaa", "aaaaaaaaaa"),
    ("aaaaaa", "aaa"),
    ("bbbbbbb", "bb"),
])

# --- TC 07: One string is subsequence of another (anagram sense) ---
test_cases.append([
    ("abc", "aabbcc"),
    ("xxyyzz", "xyz"),
    ("abcabc", "aabbcc"),
])

# --- TC 08: Reversed strings ---
test_cases.append([
    ("abcdefg", "gfedcba"),
    ("stress", "sserts"),
    ("racecar", "racecar"),
])

# --- TC 09: Long identical strings (max 1000) ---
test_cases.append([
    ("a" * 1000, "a" * 1000),
    ("ab" * 500, "ba" * 500),
])

# --- TC 10: Long strings, no overlap ---
test_cases.append([
    ("a" * 1000, "b" * 1000),
    ("abcdefghijklm" * 76 + "abcdefghijkl", "nopqrstuvwxyz" * 76 + "nopqrstuvwxy"),  # 76*13+12 = 1000
])

# --- TC 11: Long random strings ---
random.seed(42)
test_cases.append([
    (rand_string(1000), rand_string(1000)),
    (rand_string(500), rand_string(800)),
])

# --- TC 12: Partial overlap with repeated chars ---
test_cases.append([
    ("aabbccdd", "bbccddee"),
    ("xxyyzzaa", "aabbccxx"),
    ("abcabcabc", "cbacbacba"),
])

# --- TC 13: Strings of different lengths ---
test_cases.append([
    ("a", "aaaaaaaaaaaaaaaaaaaaa"),
    ("abcdefghijklmnopqrstuvwxyz", "a"),
    ("ab" * 500, "a"),
])

# --- TC 14: Only vowels vs consonants ---
test_cases.append([
    ("aeiouaeiou", "bcdfghjklm"),
    ("aeiou", "aeiou"),
    ("aaeeiioouu", "aeiou"),
])

# --- TC 15: Large with limited charset ---
random.seed(123)
test_cases.append([
    (rand_string(1000, "abc"), rand_string(1000, "bcd")),
    (rand_string(1000, "ab"), rand_string(1000, "ab")),
])

# --- TC 16: Palindromes ---
test_cases.append([
    ("abacaba", "abacaba"),
    ("abcba", "aabbc"),
    ("racecar", "abcdefg"),
])

# --- TC 17: Alternating characters ---
test_cases.append([
    ("ababababab", "bababababa"),
    ("cdcdcdcdcd", "dcdcdcdcdc"),
    ("efefef", "fefefe"),
])

# --- TC 18: Stress - many pairs of medium strings ---
random.seed(999)
tc18 = []
for _ in range(10):
    tc18.append((rand_string(random.randint(50, 200)), rand_string(random.randint(50, 200))))
test_cases.append(tc18)

# --- Write all test cases ---
for idx, pairs in enumerate(test_cases, start=1):
    filename_in = os.path.join(TESTCASES_DIR, f"{idx:02d}.in")
    filename_out = os.path.join(TESTCASES_DIR, f"{idx:02d}.out")

    input_lines = []
    for a, b in pairs:
        input_lines.append(a)
        input_lines.append(b)

    answers = solve_all(pairs)

    with open(filename_in, 'w') as f:
        f.write('\n'.join(input_lines) + '\n')

    with open(filename_out, 'w') as f:
        f.write('\n'.join(answers) + '\n')

print(f"Generated {len(test_cases)} test cases in {TESTCASES_DIR}")

# --- Verify all test cases against solution.py ---
import subprocess

print("\nVerifying all test cases...")
all_pass = True
for idx in range(1, len(test_cases) + 1):
    in_file = os.path.join(TESTCASES_DIR, f"{idx:02d}.in")
    out_file = os.path.join(TESTCASES_DIR, f"{idx:02d}.out")

    result = subprocess.run(
        ["python3", "/Users/lambert/Documents/GPE-Helper/judge/problems/10567/solution.py"],
        stdin=open(in_file),
        capture_output=True, text=True
    )

    expected = open(out_file).read()
    actual = result.stdout

    if actual == expected:
        print(f"  TC {idx:02d}: PASS")
    else:
        print(f"  TC {idx:02d}: FAIL")
        print(f"    Expected: {repr(expected[:200])}")
        print(f"    Actual:   {repr(actual[:200])}")
        all_pass = False

if all_pass:
    print("\nAll test cases verified successfully!")
else:
    print("\nSome test cases FAILED!")
