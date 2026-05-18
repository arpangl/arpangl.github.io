import random
import os

random.seed(42)

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10409/testcases"

test_cases = []

# TC 01: Sample input
test_cases.append(("01", "2\n10\n10\n4\n1\n2\n2\n4\n"))

# TC 02: Single element (n=1)
test_cases.append(("02", "1\n42\n"))

# TC 03: Two identical elements (even n, same values)
test_cases.append(("03", "2\n5\n5\n"))

# TC 04: Two different elements (even n, gap > 1)
test_cases.append(("04", "2\n3\n7\n"))

# TC 05: Odd n=3, distinct values
test_cases.append(("05", "3\n1\n5\n9\n"))

# TC 06: Even n=4, all same
test_cases.append(("06", "4\n100\n100\n100\n100\n"))

# TC 07: Odd n=5, all same
test_cases.append(("07", "5\n0\n0\n0\n0\n0\n"))

# TC 08: n=1 with 0 (minimum value)
test_cases.append(("08", "1\n0\n"))

# TC 09: n=1 with 65535 (maximum value)
test_cases.append(("09", "1\n65535\n"))

# TC 10: Even n=2, extreme gap (0 and 65535)
test_cases.append(("10", "2\n0\n65535\n"))

# TC 11: Odd n=3, with duplicates at median
test_cases.append(("11", "3\n1\n1\n1000\n"))

# TC 12: Even n=6, median range has width > 1
test_cases.append(("12", "6\n1\n3\n5\n10\n15\n20\n"))

# TC 13: Multiple blocks in one test case
test_cases.append(("13", "1\n0\n1\n65535\n2\n0\n65535\n3\n100\n200\n300\n"))

# TC 14: Even n, consecutive medians (gap=1 => 2 possible A values but answer is 1 distinct? No, gap=1 means 2 values)
# Actually gap=0 means 1, gap=1 means 2
test_cases.append(("14", "4\n1\n2\n3\n4\n"))

# TC 15: Large n=100, random values, odd
vals_15 = [random.randint(0, 65535) for _ in range(99)]
test_cases.append(("15", "99\n" + "\n".join(map(str, vals_15)) + "\n"))

# TC 16: Large n=100, random values, even
vals_16 = [random.randint(0, 65535) for _ in range(100)]
test_cases.append(("16", "100\n" + "\n".join(map(str, vals_16)) + "\n"))

# TC 17: n=1000, all zeros
test_cases.append(("17", "1000\n" + "\n".join(["0"] * 1000) + "\n"))

# TC 18: Even n=6 with duplicates at both medians
test_cases.append(("18", "6\n3\n3\n5\n5\n5\n10\n"))

# TC 19: Large-ish test with multiple blocks, including edge cases
block1_n = 500
block1_vals = [random.randint(0, 100) for _ in range(block1_n)]
block2_n = 501
block2_vals = [random.randint(60000, 65535) for _ in range(block2_n)]
inp_19 = f"{block1_n}\n" + "\n".join(map(str, block1_vals)) + "\n"
inp_19 += f"{block2_n}\n" + "\n".join(map(str, block2_vals)) + "\n"
test_cases.append(("19", inp_19))

# TC 20: Stress test - larger n with many blocks
inp_20 = ""
for _ in range(5):
    sz = random.randint(1, 200)
    vals = [random.randint(0, 65535) for _ in range(sz)]
    inp_20 += f"{sz}\n" + "\n".join(map(str, vals)) + "\n"
test_cases.append(("20", inp_20))

# Write .in files
for tc_id, inp in test_cases:
    in_path = os.path.join(TESTCASE_DIR, f"{tc_id}.in")
    with open(in_path, 'w') as f:
        f.write(inp)

print(f"Generated {len(test_cases)} test cases (.in files)")
