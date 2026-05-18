#!/usr/bin/env python3
"""
Generate and verify test cases for problem 10421: All You Need Is Love.

Problem summary:
- Given two valid binary strings S1 and S2 (no leading zeros, length >= 2),
  determine if there exists a valid L (binary string, no leading zeros, length >= 2,
  so L >= 2 in decimal) such that L divides both S1 and S2.
- Equivalently: GCD(decimal(S1), decimal(S2)) >= 2.

Output format:
  "Pair #p: All you need is love!"      if GCD >= 2
  "Pair #p: Love is not all you need!"  if GCD == 1
"""

import math
import os
import random

random.seed(42)

def to_bin_str(n):
    """Convert a positive integer to a binary string (no leading zeros)."""
    return bin(n)[2:]

def solve(s1, s2):
    """Given two binary strings, return True if GCD of their decimal values >= 2."""
    v1 = int(s1, 2)
    v2 = int(s2, 2)
    return math.gcd(v1, v2) >= 2

def make_output(pairs):
    """Generate full output text for a list of (s1, s2) pairs."""
    lines = []
    for i, (s1, s2) in enumerate(pairs, 1):
        if solve(s1, s2):
            lines.append(f"Pair #{i}: All you need is love!")
        else:
            lines.append(f"Pair #{i}: Love is not all you need!")
    return "\n".join(lines) + "\n"

def make_input(pairs):
    """Generate full input text."""
    lines = [str(len(pairs))]
    for s1, s2 in pairs:
        lines.append(s1)
        lines.append(s2)
    return "\n".join(lines) + "\n"

def valid_bin_str(s):
    """Check if a binary string is valid: length >= 2, no leading zeros."""
    if len(s) < 2:
        return False
    if s[0] == '0':
        return False
    return all(c in '01' for c in s)

def random_bin_str(min_len=2, max_len=30):
    """Generate a random valid binary string of length between min_len and max_len."""
    length = random.randint(min_len, max_len)
    # First bit is always 1
    bits = ['1'] + [random.choice('01') for _ in range(length - 1)]
    return ''.join(bits)

def random_value_with_len(bit_len):
    """Generate a random integer whose binary representation has exactly bit_len bits."""
    if bit_len < 2:
        bit_len = 2
    low = 1 << (bit_len - 1)
    high = (1 << bit_len) - 1
    return random.randint(low, high)

# ============================================================
# Define test cases
# ============================================================

all_test_cases = []

# --- Test Case 01: Sample from problem statement ---
tc01 = [
    ("11011", "11000"),
    ("11011", "11001"),
    ("111111", "100"),
    ("1000000000", "110"),
    ("1010", "100"),
]

# --- Test Case 02: Edge cases - minimum length strings (length 2) ---
tc02 = [
    ("10", "10"),   # 2, 2 -> GCD=2 >= 2 -> love
    ("10", "11"),   # 2, 3 -> GCD=1 -> not love
    ("11", "11"),   # 3, 3 -> GCD=3 >= 2 -> love
    ("10", "110"),  # 2, 6 -> GCD=2 >= 2 -> love
    ("11", "110"),  # 3, 6 -> GCD=3 >= 2 -> love
    ("11", "101"),  # 3, 5 -> GCD=1 -> not love
    ("11", "111"),  # 3, 7 -> GCD=1 -> not love
    ("10", "100"),  # 2, 4 -> GCD=2 -> love
]

# --- Test Case 03: Equal numbers ---
tc03 = [
    ("11011", "11011"),             # same -> GCD=self >= 2 -> love
    ("10", "10"),                   # 2, 2 -> love
    ("111111111111111111111111111111", "111111111111111111111111111111"),  # 30 bits, same
    ("100000000000000000000000000000", "100000000000000000000000000000"),  # 2^29, same
    ("101010101010101010101010101010", "101010101010101010101010101010"),  # same
]

# --- Test Case 04: Powers of 2 ---
tc04 = [
    ("10", "100"),                  # 2, 4 -> GCD=2 -> love
    ("100", "1000"),                # 4, 8 -> GCD=4 -> love
    ("10", "1000000000000000000000000000000"),  # 2, 2^30... wait, max 30 chars
]
# 2^29 = 30 bits
p2_29 = to_bin_str(2**29)  # 30 chars
p2_1 = to_bin_str(2)
p2_5 = to_bin_str(32)
p2_10 = to_bin_str(1024)
p2_15 = to_bin_str(2**15)
p2_20 = to_bin_str(2**20)
tc04 = [
    (p2_1, p2_29),    # 2, 2^29 -> GCD=2 -> love
    (p2_5, p2_10),    # 32, 1024 -> GCD=32 -> love
    (p2_15, p2_20),   # 2^15, 2^20 -> GCD=2^15 -> love
    (p2_1, "11"),     # 2, 3 -> GCD=1 -> not love
    (p2_5, "101"),    # 32, 5 -> GCD=1 -> not love
]

# --- Test Case 05: Coprime (GCD=1) cases ---
tc05 = [
    (to_bin_str(7), to_bin_str(11)),    # primes
    (to_bin_str(13), to_bin_str(17)),   # primes
    (to_bin_str(23), to_bin_str(29)),   # primes
    (to_bin_str(97), to_bin_str(101)),  # primes
    (to_bin_str(127), to_bin_str(131)), # primes
    (to_bin_str(3), to_bin_str(5)),     # 3, 5 coprime
    (to_bin_str(9), to_bin_str(25)),    # 9, 25 coprime (3^2, 5^2)
    (to_bin_str(49), to_bin_str(27)),   # 49, 27 coprime (7^2, 3^3)
]

# --- Test Case 06: Non-coprime (GCD >= 2) cases ---
tc06 = [
    (to_bin_str(6), to_bin_str(10)),    # GCD=2
    (to_bin_str(12), to_bin_str(18)),   # GCD=6
    (to_bin_str(100), to_bin_str(250)), # GCD=50
    (to_bin_str(36), to_bin_str(48)),   # GCD=12
    (to_bin_str(1000), to_bin_str(750)),# GCD=250
    (to_bin_str(21), to_bin_str(35)),   # GCD=7
    (to_bin_str(77), to_bin_str(91)),   # GCD=7
    (to_bin_str(121), to_bin_str(143)), # GCD=11
]

# --- Test Case 07: Large values near 30-bit limit ---
max30 = (1 << 30) - 1  # 1073741823, 30 bits
tc07 = []
# Both max
tc07.append((to_bin_str(max30), to_bin_str(max30 - 1)))
# GCD(2^30-1, 2^30-2) = GCD(1073741823, 1073741822) = 1 (one is odd, other even) -> not love
# Actually: 1073741823 is odd, 1073741822 is even -> GCD = GCD(odd, even) = GCD(odd, even)
# Since 1073741823 = 3 * 357913941, 1073741822 = 2 * 536870911. GCD = ?
g = math.gcd(max30, max30 - 1)  # consecutive integers -> GCD = 1
tc07.append((to_bin_str(max30), to_bin_str(max30 - 2)))
# max30 = 2^30-1 (odd), max30-2 = 2^30-3 (odd). Diff = 2, so GCD | 2, but both odd -> GCD = 1
tc07.append((to_bin_str(max30 - 1), to_bin_str(max30 - 3)))
# both even, GCD >= 2 -> love
tc07.append((to_bin_str(2**29), to_bin_str(2**29 + 2**15)))
# 2^29, 2^29 + 2^15 = 2^15 * (2^14 + 1) ... GCD = 2^15? No. 2^29 = 2^15 * 2^14. GCD(2^15*2^14, 2^15*(2^14+1)) = 2^15
tc07.append((to_bin_str(999999999), to_bin_str(888888888)))
# Large interesting numbers

# --- Test Case 08: Primes as binary ---
primes_large = [524287, 131071, 8191, 65537, 7919, 104729]
tc08 = []
for i in range(0, len(primes_large) - 1, 2):
    tc08.append((to_bin_str(primes_large[i]), to_bin_str(primes_large[i+1])))
# Add some where one is prime * 2
tc08.append((to_bin_str(524287 * 2), to_bin_str(131071 * 2)))  # GCD=2 -> love
tc08.append((to_bin_str(8191), to_bin_str(8191 * 3)))          # GCD=8191 -> love
tc08.append((to_bin_str(7919), to_bin_str(7919 * 5)))          # GCD=7919 -> love... check length

# --- Test Case 09: Mix of various sizes ---
tc09 = []
for _ in range(10):
    l1 = random.randint(2, 30)
    l2 = random.randint(2, 30)
    v1 = random_value_with_len(l1)
    v2 = random_value_with_len(l2)
    tc09.append((to_bin_str(v1), to_bin_str(v2)))

# --- Test Case 10: Multiples of small numbers ---
tc10 = [
    (to_bin_str(2 * 3), to_bin_str(2 * 5)),       # GCD=2 -> love
    (to_bin_str(3 * 5), to_bin_str(3 * 7)),       # GCD=3 -> love
    (to_bin_str(5 * 7), to_bin_str(5 * 11)),      # GCD=5 -> love
    (to_bin_str(7 * 11), to_bin_str(7 * 13)),     # GCD=7 -> love
    (to_bin_str(11 * 13), to_bin_str(11 * 17)),   # GCD=11 -> love
    (to_bin_str(13 * 17), to_bin_str(13 * 19)),   # GCD=13 -> love
    (to_bin_str(2 * 3 * 5), to_bin_str(2 * 3 * 7)),  # GCD=6 -> love
    (to_bin_str(2*3*5*7), to_bin_str(2*3*5*11)),  # GCD=30 -> love
]

# --- Test Case 11: Stress - N close to max (many pairs) with random data ---
tc11 = []
for _ in range(50):
    l1 = random.randint(2, 30)
    l2 = random.randint(2, 30)
    v1 = random_value_with_len(l1)
    v2 = random_value_with_len(l2)
    tc11.append((to_bin_str(v1), to_bin_str(v2)))

# --- Test Case 12: All same GCD scenario ---
tc12 = []
base = 7
for i in range(1, 11):
    for j in range(i+1, i+2):
        if len(to_bin_str(base * i)) >= 2 and len(to_bin_str(base * j)) >= 2:
            tc12.append((to_bin_str(base * i), to_bin_str(base * j)))

# --- Test Case 13: Consecutive even numbers (GCD >= 2) ---
tc13 = []
for v in [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]:
    if len(to_bin_str(v)) <= 30 and len(to_bin_str(v + 2)) <= 30:
        tc13.append((to_bin_str(v), to_bin_str(v + 2)))

# --- Test Case 14: Consecutive odd numbers (GCD could be 1 or 2) ---
# GCD of consecutive odds: always 1 or 2. Actually GCD(odd, odd+2) divides 2, but both odd -> GCD = 1
tc14 = []
for v in [11, 101, 1001, 10001, 100001, 1000001, 10000001, 100000001]:
    if len(to_bin_str(v)) <= 30 and len(to_bin_str(v + 2)) <= 30:
        tc14.append((to_bin_str(v), to_bin_str(v + 2)))

# --- Test Case 15: Binary palindromes ---
def is_bin_palindrome(n):
    s = bin(n)[2:]
    return s == s[::-1]

palindromes = [n for n in range(2, 2**20) if is_bin_palindrome(n) and len(bin(n)[2:]) >= 2]
random.shuffle(palindromes)
tc15 = []
for i in range(0, min(16, len(palindromes) - 1), 2):
    s1 = to_bin_str(palindromes[i])
    s2 = to_bin_str(palindromes[i + 1])
    if len(s1) <= 30 and len(s2) <= 30:
        tc15.append((s1, s2))

# --- Test Case 16: Large stress test ---
tc16 = []
for _ in range(200):
    l1 = random.randint(2, 30)
    l2 = random.randint(2, 30)
    v1 = random_value_with_len(l1)
    v2 = random_value_with_len(l2)
    tc16.append((to_bin_str(v1), to_bin_str(v2)))

# --- Test Case 17: Fibonacci numbers as binary ---
fibs = [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
tc17 = []
for i in range(len(fibs) - 1):
    s1 = to_bin_str(fibs[i])
    s2 = to_bin_str(fibs[i + 1])
    # GCD of consecutive Fibonacci numbers is 1
    tc17.append((s1, s2))
# Add some non-consecutive (GCD = fib of GCD of indices)
tc17.append((to_bin_str(fibs[3]), to_bin_str(fibs[5])))   # fib(6), fib(8) -> GCD=fib(gcd(6,8))=fib(2)=1...
# Actually fib indices start differently. Let's just add them.
tc17.append((to_bin_str(fibs[2] * 2), to_bin_str(fibs[4] * 2)))  # both even -> GCD >= 2

# --- Test Case 18: One value is 2 or 3 ---
tc18 = [
    ("10", to_bin_str(1000000000)),  # 2, 10^9... check bits
    ("10", to_bin_str(999999999)),
    ("11", to_bin_str(999999999)),   # 3, 999999999=3*333333333 -> GCD=3 -> love
    ("11", to_bin_str(1000000000)),  # 3, 10^9 -> 10^9 = 2^9 * ... GCD(3, 10^9)? 10^9 = 2^9*5^9*... no. 10^9 not div by 3 -> not love
    ("10", to_bin_str(2**29)),       # 2, 2^29 -> GCD=2 -> love
    ("11", to_bin_str(3 * 111111)),  # 3, 333333 -> GCD=3 -> love
    ("10", to_bin_str(2**29 + 1)),   # 2, odd -> GCD=1 -> not love
    ("11", to_bin_str(2**29)),       # 3, 2^29 -> GCD=1 -> not love
]

# Validate all binary strings and trim test cases with strings > 30 chars
all_raw = [
    tc01, tc02, tc03, tc04, tc05, tc06, tc07, tc08,
    tc09, tc10, tc11, tc12, tc13, tc14, tc15, tc16,
    tc17, tc18,
]

all_test_cases = []
for tc in all_raw:
    filtered = []
    for s1, s2 in tc:
        assert valid_bin_str(s1), f"Invalid: {s1}"
        assert valid_bin_str(s2), f"Invalid: {s2}"
        assert len(s1) <= 30, f"Too long: {s1} ({len(s1)})"
        assert len(s2) <= 30, f"Too long: {s2} ({len(s2)})"
        filtered.append((s1, s2))
    all_test_cases.append(filtered)

# ============================================================
# Verify against sample
# ============================================================
sample_input_pairs = [
    ("11011", "11000"),
    ("11011", "11001"),
    ("111111", "100"),
    ("1000000000", "110"),
    ("1010", "100"),
]
expected_output = [
    "Pair #1: All you need is love!",
    "Pair #2: Love is not all you need!",
    "Pair #3: Love is not all you need!",
    "Pair #4: All you need is love!",
    "Pair #5: All you need is love!",
]

for i, (s1, s2) in enumerate(sample_input_pairs):
    v1 = int(s1, 2)
    v2 = int(s2, 2)
    g = math.gcd(v1, v2)
    result = g >= 2
    exp_love = "All you need is love!" in expected_output[i]
    assert result == exp_love, f"Sample {i+1} failed: GCD({v1},{v2})={g}, expected love={exp_love}"

print("Sample verification passed!")

# ============================================================
# Verify all test cases and write files
# ============================================================
outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10421/testcases"

for idx, tc in enumerate(all_test_cases, 1):
    fname = f"{idx:02d}"
    inp = make_input(tc)
    out = make_output(tc)

    # Double-check each pair
    for j, (s1, s2) in enumerate(tc, 1):
        v1 = int(s1, 2)
        v2 = int(s2, 2)
        g = math.gcd(v1, v2)
        line = f"Pair #{j}: " + ("All you need is love!" if g >= 2 else "Love is not all you need!")
        out_lines = out.strip().split("\n")
        assert out_lines[j-1] == line, f"TC{idx} pair {j}: expected '{line}', got '{out_lines[j-1]}'"

    in_path = os.path.join(outdir, f"{fname}.in")
    out_path = os.path.join(outdir, f"{fname}.out")

    with open(in_path, 'w') as f:
        f.write(inp)
    with open(out_path, 'w') as f:
        f.write(out)

    print(f"Test case {fname}: {len(tc)} pairs written. ({in_path})")

print(f"\nTotal: {len(all_test_cases)} test cases generated and verified.")
print("All verifications passed!")
