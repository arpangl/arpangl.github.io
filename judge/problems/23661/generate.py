import sys
import random

def solve(N, L, U):
    M = 0
    for bit in range(31, -1, -1):
        mask = 1 << bit
        n_bit = (N >> bit) & 1
        if n_bit == 1:
            candidate = M
            lo = candidate
            hi = candidate | (mask - 1)
            if lo <= U and hi >= L:
                M = candidate
            else:
                M = M | mask
        else:
            candidate = M | mask
            lo = candidate
            hi = candidate | (mask - 1)
            if lo <= U and hi >= L:
                M = candidate
            else:
                M = M
    return M

def brute_force(N, L, U):
    best_or = -1
    best_m = -1
    for m in range(L, U + 1):
        val = N | m
        if val > best_or or (val == best_or and m < best_m):
            best_or = val
            best_m = m
    return best_m

# Verify greedy matches brute force on small cases
print("Verifying greedy vs brute force on small cases...")
count = 0
for N in range(0, 256):
    for L in range(0, 128):
        for U in range(L, 128):
            g = solve(N, L, U)
            b = brute_force(N, L, U)
            if g != b:
                print(f"MISMATCH: N={N}, L={L}, U={U}, greedy={g}, brute={b}")
                sys.exit(1)
            count += 1
print(f"Verified {count} small cases. All match!")

# Additional random verification with larger values
print("Verifying random larger cases...")
random.seed(42)
for _ in range(10000):
    N = random.randint(0, 2**32 - 1)
    L = random.randint(0, 2**32 - 1)
    U = random.randint(L, min(L + 100000, 2**32 - 1))
    g = solve(N, L, U)
    b = brute_force(N, L, U)
    if g != b:
        print(f"MISMATCH: N={N}, L={L}, U={U}, greedy={g}, brute={b}")
        sys.exit(1)
print("All random cases match!")

# Now generate test cases
MAX32 = 2**32 - 1

test_cases = []

# TC 01: Sample input
tc1 = [
    (100, 50, 60),
    (100, 50, 50),
    (100, 0, 100),
    (1, 0, 100),
    (15, 1, 15),
]
test_cases.append(tc1)

# TC 02: Edge - all zeros
tc2 = [
    (0, 0, 0),
]
test_cases.append(tc2)

# TC 03: Edge - max values
tc3 = [
    (MAX32, 0, MAX32),
    (0, 0, MAX32),
    (MAX32, MAX32, MAX32),
    (0, MAX32, MAX32),
]
test_cases.append(tc3)

# TC 04: N = 0, various ranges
tc4 = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 1),
    (0, 0, 255),
    (0, 100, 200),
    (0, 0, MAX32),
]
test_cases.append(tc4)

# TC 05: N = MAX32, M doesn't matter for OR
tc5 = [
    (MAX32, 0, 0),
    (MAX32, 0, MAX32),
    (MAX32, 100, 200),
    (MAX32, MAX32, MAX32),
    (MAX32, 1000000, 2000000),
]
test_cases.append(tc5)

# TC 06: L = U (single choice)
tc6 = [
    (0, 0, 0),
    (0, 1, 1),
    (0, MAX32, MAX32),
    (12345, 67890, 67890),
    (MAX32, 0, 0),
    (123456789, 987654321, 987654321),
]
test_cases.append(tc6)

# TC 07: Powers of 2
tc7 = []
for i in range(32):
    N = 1 << i
    L = 0
    U = (1 << (i+1)) - 1 if i < 31 else MAX32
    tc7.append((N, L, U))
test_cases.append(tc7)

# TC 08: N has alternating bits
tc8 = [
    (0xAAAAAAAA, 0, MAX32),
    (0x55555555, 0, MAX32),
    (0xAAAAAAAA, 0x55555555, 0x55555555),
    (0x55555555, 0xAAAAAAAA, 0xAAAAAAAA),
    (0xAAAAAAAA, 0x50000000, 0x5FFFFFFF),
    (0x55555555, 0xA0000000, 0xAFFFFFFF),
]
test_cases.append(tc8)

# TC 09: Tight ranges near powers of 2
tc9 = [
    (0, 1023, 1025),
    (1023, 1023, 1025),
    (1024, 1023, 1025),
    (1025, 1023, 1025),
    (0, 2**31 - 1, 2**31 + 1),
    (2**31, 2**31 - 1, 2**31 + 1),
    (MAX32, 2**31 - 1, 2**31 + 1),
]
test_cases.append(tc9)

# TC 10: Large N, small range
tc10 = [
    (0xFFFF0000, 0, 0xFFFF),
    (0x0000FFFF, 0xFFFF0000, MAX32),
    (0xF0F0F0F0, 0x0F0F0F0F, 0x0F0F0F0F),
    (0x0F0F0F0F, 0xF0F0F0F0, 0xF0F0F0F0),
]
test_cases.append(tc10)

# TC 11: Random medium values
random.seed(123)
tc11 = []
for _ in range(20):
    N = random.randint(0, 2**32 - 1)
    L = random.randint(0, 2**32 - 1)
    U = random.randint(L, min(L + random.randint(1, 2**20), MAX32))
    tc11.append((N, L, U))
test_cases.append(tc11)

# TC 12: Random large ranges
random.seed(456)
tc12 = []
for _ in range(20):
    N = random.randint(0, MAX32)
    L = random.randint(0, MAX32 // 2)
    U = random.randint(L, MAX32)
    tc12.append((N, L, U))
test_cases.append(tc12)

# TC 13: N complement scenarios - want M to fill in missing bits
tc13 = [
    (0b11110000, 0b00001111, 0b00001111),  # perfect complement
    (0b11110000, 0b00000000, 0b11111111),   # range includes complement
    (0b10101010, 0b01010101, 0b01010101),   # perfect complement
    (0b11001100, 0b00000000, 0b00111111),
    (0b11001100, 0b00110000, 0b00110011),
]
test_cases.append(tc13)

# TC 14: Stress - many lines with wide ranges
random.seed(789)
tc14 = []
for _ in range(30):
    N = random.randint(0, MAX32)
    L = random.randint(0, MAX32)
    U = random.randint(L, MAX32)
    tc14.append((N, L, U))
test_cases.append(tc14)

# TC 15: Boundary values
tc15 = [
    (0, 0, 1),
    (1, 0, 1),
    (2, 0, 1),
    (3, 0, 1),
    (0, 0, MAX32),
    (1, 0, MAX32),
    (MAX32 - 1, 0, MAX32),
    (MAX32, 0, MAX32),
    (2**31, 0, MAX32),
    (2**31 - 1, 0, MAX32),
]
test_cases.append(tc15)

# TC 16: Cases where minimum M is important
tc16 = [
    (7, 0, 7),       # N|M = 7 for all M in [0,7], so min M = 0
    (255, 0, 255),    # same idea
    (0xFFFF, 0, 0xFFFF),
    (3, 4, 7),        # N=011, range [100,111], OR: 111 for all, min M=4
    (5, 2, 3),        # N=101, M=2(010)->111, M=3(011)->111, min=2
    (6, 1, 1),        # N=110, M=1(001)->111
]
test_cases.append(tc16)

# TC 17: Very large values near MAX32
tc17 = [
    (MAX32 - 1, MAX32 - 10, MAX32),
    (MAX32 - 1, MAX32, MAX32),
    (1, MAX32 - 1, MAX32),
    (0, MAX32 - 1, MAX32),
    (2**31, MAX32 - 100, MAX32),
    (MAX32 - 255, 0, 255),
    (0, MAX32 - 255, MAX32),
]
test_cases.append(tc17)

# Write test cases
basedir = "/Users/lambert/Documents/GPE-Helper/judge/problems/23661/testcases"
for i, tc in enumerate(test_cases, 1):
    fname_in = f"{basedir}/{i:02d}.in"
    fname_out = f"{basedir}/{i:02d}.out"

    input_lines = []
    output_lines = []
    for (N, L, U) in tc:
        input_lines.append(f"{N} {L} {U}")
        result = solve(N, L, U)
        output_lines.append(str(result))

    with open(fname_in, 'w') as f:
        f.write('\n'.join(input_lines) + '\n')
    with open(fname_out, 'w') as f:
        f.write('\n'.join(output_lines) + '\n')

    print(f"Written {fname_in} ({len(tc)} cases)")

print(f"\nGenerated {len(test_cases)} test case files.")
