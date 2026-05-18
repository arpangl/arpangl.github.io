#!/usr/bin/env python3
"""
Test data generator for Problem 11017: Longest Common Subsequence

Problem format:
  - Input: pairs of lines (two strings per pair), multiple pairs per file
  - Output: one integer per pair = length of LCS
  - Each string up to 1000 characters
"""

import os
import random
import string

TESTCASES_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/11017/testcases"


def lcs_length(s1: str, s2: str) -> int:
    """Standard DP solution for LCS length."""
    m, n = len(s1), len(s2)
    # Use rolling array for memory efficiency
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * (n + 1)
    return prev[n]


def write_testcase(case_id: int, pairs: list[tuple[str, str]]):
    """Write a single test case file pair (XX.in / XX.out)."""
    tag = f"{case_id:02d}"
    in_path = os.path.join(TESTCASES_DIR, f"{tag}.in")
    out_path = os.path.join(TESTCASES_DIR, f"{tag}.out")

    in_lines = []
    out_lines = []
    for s1, s2 in pairs:
        in_lines.append(s1)
        in_lines.append(s2)
        out_lines.append(str(lcs_length(s1, s2)))

    with open(in_path, "w") as f:
        f.write("\n".join(in_lines) + "\n")
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")

    # Verification: re-read and check
    print(f"  Case {tag}: {len(pairs)} pair(s)")
    for i, (s1, s2) in enumerate(pairs):
        ans = lcs_length(s1, s2)
        print(f"    Pair {i+1}: |s1|={len(s1)}, |s2|={len(s2)}, LCS={ans}")


def rand_str(length: int, alphabet: str = string.ascii_lowercase) -> str:
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_all():
    random.seed(42)
    case_id = 0

    # =========================================================================
    # Case 01: Sample from problem statement
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("a1b2c3d4e", "zz1yy2xx3ww4vv"),
        ("abcdgh", "aedfhr"),
        ("abcdefghijklmnopqrstuvwxyz", "a0b0c0d0e0f0g0h0i0j0k0l0m0n0o0p0q0r0s0t0u0v0w0x0y0z0"),
        ("abcdefghijklmnzyxwvutsrqpo", "opqrstuvwxyzabcdefghijklmn"),
    ])

    # =========================================================================
    # Case 02: Empty strings
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("", ""),
        ("", "abc"),
        ("xyz", ""),
        ("", "a"),
    ])

    # =========================================================================
    # Case 03: Single characters
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("a", "a"),
        ("a", "b"),
        ("x", "xyz"),
        ("xyz", "z"),
        ("m", "m"),
    ])

    # =========================================================================
    # Case 04: Identical strings
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("abcdef", "abcdef"),
        ("aaaaaa", "aaaaaa"),
        ("hello world", "hello world"),
        ("xyxyxyxy", "xyxyxyxy"),
    ])

    # =========================================================================
    # Case 05: Completely different strings (no common characters)
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("aaaa", "bbbb"),
        ("abc", "xyz"),
        ("111", "222"),
        ("aeiou", "bcdfg"),
        ("pqr", "stu"),
    ])

    # =========================================================================
    # Case 06: One string is a subsequence of the other
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("ace", "abcde"),
        ("abc", "aXbYcZ"),
        ("xyz", "xxxyyyzzz"),
        ("ad", "abcd"),
    ])

    # =========================================================================
    # Case 07: Reversed strings
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("abcdef", "fedcba"),
        ("abcba", "abcba"[::-1]),
        ("abcdefghij", "jihgfedcba"),
        ("aabbcc", "ccbbaa"),
    ])

    # =========================================================================
    # Case 08: Palindromes
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("racecar", "racecar"),
        ("racecar", "racecar"[::-1]),
        ("abacaba", "abacaba"),
        ("madam", "madam"[::-1]),
        ("level", "levee"),
    ])

    # =========================================================================
    # Case 09: Repeated single character
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("aaaaaaaaaa", "aaaaa"),
        ("bbb", "bbbbbbb"),
        ("a" * 100, "a" * 50),
        ("x" * 200, "x" * 200),
    ])

    # =========================================================================
    # Case 10: Strings with digits and letters mixed
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("a1b2c3d4e5f6", "123456"),
        ("1a2b3c4d5e6f", "abcdef"),
        ("abc123def456", "123abc456def"),
        ("a1a1a1", "1a1a1a"),
    ])

    # =========================================================================
    # Case 11: Medium length random (lowercase, len ~50-100)
    # =========================================================================
    case_id += 1
    pairs = []
    for _ in range(4):
        s1 = rand_str(random.randint(50, 100))
        s2 = rand_str(random.randint(50, 100))
        pairs.append((s1, s2))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 12: Medium with small alphabet (more matches expected)
    # =========================================================================
    case_id += 1
    pairs = []
    for _ in range(4):
        s1 = rand_str(random.randint(80, 150), "abc")
        s2 = rand_str(random.randint(80, 150), "abc")
        pairs.append((s1, s2))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 13: Long strings, full alphabet (~500 chars)
    # =========================================================================
    case_id += 1
    pairs = []
    for _ in range(3):
        s1 = rand_str(random.randint(400, 500))
        s2 = rand_str(random.randint(400, 500))
        pairs.append((s1, s2))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 14: Long strings, small alphabet (~500 chars, alphabet "ab")
    # =========================================================================
    case_id += 1
    pairs = []
    for _ in range(3):
        s1 = rand_str(random.randint(400, 500), "ab")
        s2 = rand_str(random.randint(400, 500), "ab")
        pairs.append((s1, s2))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 15: Maximum length 1000 chars, full alphabet
    # =========================================================================
    case_id += 1
    pairs = []
    for _ in range(2):
        s1 = rand_str(1000)
        s2 = rand_str(1000)
        pairs.append((s1, s2))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 16: Maximum length 1000 chars, small alphabet ("abc")
    # =========================================================================
    case_id += 1
    pairs = []
    for _ in range(2):
        s1 = rand_str(1000, "abc")
        s2 = rand_str(1000, "abc")
        pairs.append((s1, s2))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 17: One string much longer than the other
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        ("ab", rand_str(500)),
        (rand_str(500), "z"),
        ("abc", rand_str(1000)),
        (rand_str(1000), "xy"),
    ])

    # =========================================================================
    # Case 18: Interleaved pattern - s2 is s1 with chars inserted
    # =========================================================================
    case_id += 1
    base1 = rand_str(100)
    # Insert random chars between each char of base1
    expanded1 = ""
    for ch in base1:
        expanded1 += rand_str(random.randint(0, 3)) + ch
    base2 = rand_str(50)
    expanded2 = ""
    for ch in base2:
        expanded2 += rand_str(random.randint(0, 2)) + ch
    write_testcase(case_id, [
        (base1, expanded1),
        (base2, expanded2),
        (rand_str(200), rand_str(200, "abcde")),
    ])

    # =========================================================================
    # Case 19: Stress test - multiple max-length pairs
    # =========================================================================
    case_id += 1
    pairs = []
    s1 = rand_str(1000, "abcdefgh")
    s2 = rand_str(1000, "abcdefgh")
    pairs.append((s1, s2))
    # Identical 1000-char strings
    s3 = rand_str(1000)
    pairs.append((s3, s3))
    write_testcase(case_id, pairs)

    # =========================================================================
    # Case 20: Edge cases mix - special patterns
    # =========================================================================
    case_id += 1
    write_testcase(case_id, [
        # Alternating characters
        ("ababababab", "bababababa"),
        # All same char vs mixed
        ("aaaaaaaaaa", "abcdefghij"),
        # Prefix match
        ("abcdefghij", "abcdeXXXXX"),
        # Suffix match
        ("XXXXXfghij", "abcdefghij"),
        # LCS in the middle
        ("XXXabcXXX", "YYYabcYYY"),
    ])

    print(f"\nGenerated {case_id} test cases in {TESTCASES_DIR}")


if __name__ == "__main__":
    generate_all()
