#!/usr/bin/env python3
"""
Generate test cases for "Extend to Palindromes" (24931).
Each test file contains multiple lines (multiple test strings).
We generate 18 test files covering various edge cases and stress scenarios.
"""

import os
import random
import string

BASE = "/Users/lambert/Documents/GPE-Helper/judge/problems/24931/testcases"

def solve(s):
    if not s:
        return s
    rev = s[::-1]
    combined = rev + '#' + s
    n = len(combined)
    fail = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and combined[k] != combined[i]:
            k = fail[k - 1]
        if combined[k] == combined[i]:
            k += 1
        fail[i] = k
    longest_palindrome_suffix = fail[-1]
    append = s[:len(s) - longest_palindrome_suffix][::-1]
    return s + append

def write_test(test_id, lines):
    """Write a test case: lines is a list of input strings."""
    inp_path = os.path.join(BASE, f"{test_id:02d}.in")
    out_path = os.path.join(BASE, f"{test_id:02d}.out")
    with open(inp_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    with open(out_path, 'w') as f:
        for line in lines:
            f.write(solve(line) + '\n')

def random_string(length, charset=None):
    if charset is None:
        charset = string.ascii_letters
    return ''.join(random.choice(charset) for _ in range(length))

def random_palindrome(half_len, charset=None):
    if charset is None:
        charset = string.ascii_lowercase
    half = ''.join(random.choice(charset) for _ in range(half_len))
    # randomly odd or even
    if random.random() < 0.5:
        return half + random.choice(charset) + half[::-1]
    else:
        return half + half[::-1]

random.seed(42)

# ---- Test 01: Sample input ----
write_test(1, ["aaaa", "abba", "amanaplanacanal", "xyz"])

# ---- Test 02: Single characters ----
write_test(2, ["a", "Z", "m", "B", "x"])

# ---- Test 03: All same characters ----
write_test(3, ["aaa", "bbbbb", "ZZZZZZZZZ", "cc", "DDDDDDDDDDDDD"])

# ---- Test 04: Already palindromes (odd length) ----
write_test(4, ["aba", "abcba", "racecar", "level", "madam"])

# ---- Test 05: Already palindromes (even length) ----
write_test(5, ["abba", "abccba", "aaaa", "bccb", "deed"])

# ---- Test 06: Two characters ----
write_test(6, ["ab", "ba", "aa", "zA", "Az"])

# ---- Test 07: Strings needing one char appended ----
write_test(7, ["abc", "xyza", "abcd", "race"])

# ---- Test 08: Odd length strings, not palindrome ----
write_test(8, ["abcde", "hello", "world", "xyzab", "aloha"])

# ---- Test 09: Even length strings, not palindrome ----
write_test(9, ["abcd", "test", "code", "palm", "frog"])

# ---- Test 10: Mixed case ----
write_test(10, ["AbBa", "AaA", "aBcDe", "XyZyX", "HeLLo"])

# ---- Test 11: Near-palindromes (palindrome with one extra char at end removed) ----
write_test(11, [
    "abcb",       # abcba minus last 'a'
    "racecar"[:-1],  # raceca
    "abacab",     # needs just a
    "deified"[:-2],  # deifi -> deified? let solver handle
    "reviver"[:-1],
])

# ---- Test 12: Medium random strings (100-500 chars) ----
lines12 = []
for _ in range(10):
    n = random.randint(100, 500)
    lines12.append(random_string(n, string.ascii_lowercase))
write_test(12, lines12)

# ---- Test 13: Medium strings that are palindromes ----
lines13 = []
for _ in range(10):
    half = random.randint(50, 250)
    lines13.append(random_palindrome(half, string.ascii_lowercase))
write_test(13, lines13)

# ---- Test 14: Medium strings with palindromic suffix ----
lines14 = []
for _ in range(10):
    prefix_len = random.randint(20, 100)
    pal_half = random.randint(30, 150)
    prefix = random_string(prefix_len, string.ascii_lowercase)
    pal = random_palindrome(pal_half, string.ascii_lowercase)
    lines14.append(prefix + pal)
write_test(14, lines14)

# ---- Test 15: Large strings ~50000 chars, lowercase ----
lines15 = []
for _ in range(2):
    n = random.randint(40000, 50000)
    lines15.append(random_string(n, string.ascii_lowercase))
write_test(15, lines15)

# ---- Test 16: Large palindrome ~100000 chars ----
lines16 = []
half = random.randint(49000, 50000)
lines16.append(random_palindrome(half, string.ascii_lowercase))
write_test(16, lines16)

# ---- Test 17: Large string that is almost a palindrome (palindrome with a few chars chopped from end) ----
lines17 = []
half = random.randint(40000, 49000)
pal = random_palindrome(half, string.ascii_lowercase)
# chop last 5-20 chars
chop = random.randint(5, 20)
lines17.append(pal[:-chop])
# Also one large string of all same char
lines17.append('a' * 100000)
write_test(17, lines17)

# ---- Test 18: Stress test - max length 100000, mixed case ----
lines18 = []
lines18.append(random_string(100000, string.ascii_letters))
write_test(18, lines18)

print("All 18 test cases generated successfully.")
