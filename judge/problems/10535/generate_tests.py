#!/usr/bin/env python3
"""
Generate test cases for Prime Distance (10535).

Constraints:
- L, U positive integers, L < U
- 1 <= L < U <= 2^31 - 1 (2147483647)
- U - L <= 1,000,000

Edge cases to cover:
1. Sample case
2. L=1, small range (1 is not prime)
3. L=2, U=3 (smallest primes)
4. Range with no primes at all (e.g., between two distant primes)
5. Range with exactly one prime
6. Range with exactly two primes
7. Large L and U near 2^31-1
8. Range around known prime gaps
9. L=1, U=1000000 (max range starting at 1)
10. Range with twin primes (gap=2)
11. Range with large gaps between primes
12. Single number range won't work (L < U), so L, L+1
13. Range containing only even numbers (no primes except possibly 2)
14. Large primes near 10^9
15. Range [1, 2] edge
16. Range around powers of 2
17. Dense prime region (small numbers)
18. Sparse prime region (large numbers)
"""

import subprocess
import os

BASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/10535/testcases"

test_cases = []

# TC 01: Sample case
test_cases.append({
    "id": "01",
    "lines": ["2 17", "14 17"]
})

# TC 02: L=1, U=2 (edge: 1 is not prime, only prime is 2 -> less than 2 primes)
test_cases.append({
    "id": "02",
    "lines": ["1 2"]
})

# TC 03: L=2, U=3 (two adjacent primes that are adjacent numbers)
test_cases.append({
    "id": "03",
    "lines": ["2 3"]
})

# TC 04: L=1, U=10 (small range from 1)
test_cases.append({
    "id": "04",
    "lines": ["1 10"]
})

# TC 05: Range with no primes - [20, 22] -> no primes (20,21,22 all composite)
test_cases.append({
    "id": "05",
    "lines": ["20 22", "24 28"]
})

# TC 06: Large range from 1 to 1000000 (max gap size)
test_cases.append({
    "id": "06",
    "lines": ["1 1000000"]
})

# TC 07: Range near 2^31-1 = 2147483647 (which is a Mersenne prime!)
# 2147483647 is prime itself
test_cases.append({
    "id": "07",
    "lines": ["2147483600 2147483647"]
})

# TC 08: Range with twin primes. (1000000000-ish range)
# Known twin primes exist near small numbers: 11,13 and 17,19 and 29,31
test_cases.append({
    "id": "08",
    "lines": ["10 50"]
})

# TC 09: Range [2, 2] won't work since L < U. Try [2, 4] -> primes 2,3
test_cases.append({
    "id": "09",
    "lines": ["2 4", "3 5"]
})

# TC 10: Large numbers, range around 10^9
test_cases.append({
    "id": "10",
    "lines": ["1000000000 1001000000"]
})

# TC 11: Range with exactly one prime -> no adjacent primes
# [7, 10] -> only prime is 7
test_cases.append({
    "id": "11",
    "lines": ["7 10", "4 6"]
})

# TC 12: Range around a known large prime gap
# After prime 31397, next prime is 31469 (gap of 72)
# Actually let's use a well-known gap. After 113 the next prime is 127 (gap 14)
test_cases.append({
    "id": "12",
    "lines": ["110 130", "23 30"]
})

# TC 13: Range of only even numbers with no 2 included
test_cases.append({
    "id": "13",
    "lines": ["100 200"]
})

# TC 14: Very large L near 2^31, max range
test_cases.append({
    "id": "14",
    "lines": ["2146483647 2147483647"]
})

# TC 15: Multiple queries - stress with various ranges
test_cases.append({
    "id": "15",
    "lines": [
        "1 3",
        "2 100",
        "999999000 1000000000",
        "1999999000 2000000000",
    ]
})

# TC 16: Edge - L=1, U=1000 (lots of primes)
test_cases.append({
    "id": "16",
    "lines": ["1 1000"]
})

# TC 17: Range containing a single even number and surrounding
# [4, 8] primes: 5, 7 -> closest 5,7 gap=2, also most distant
test_cases.append({
    "id": "17",
    "lines": ["4 8", "8 12", "14 16"]
})

# TC 18: Near powers of 2
test_cases.append({
    "id": "18",
    "lines": [
        "1073741800 1073741900",
        "536870900 536871000",
        "268435400 268435500",
    ]
})

# TC 19: Range with 3+ primes to ensure correct closest/most distant
# [90, 110] -> primes: 97, 101, 103, 107, 109
test_cases.append({
    "id": "19",
    "lines": ["90 110", "190 210"]
})

# TC 20: Large range in the billions
test_cases.append({
    "id": "20",
    "lines": ["2000000000 2000100000"]
})

print(f"Generating {len(test_cases)} test cases...")

for tc in test_cases:
    tc_id = tc["id"]
    in_path = os.path.join(BASE_DIR, f"{tc_id}.in")
    out_path = os.path.join(BASE_DIR, f"{tc_id}.out")

    # Write input
    with open(in_path, "w") as f:
        for line in tc["lines"]:
            f.write(line + "\n")

    # Generate output using solution
    result = subprocess.run(
        ["python3", "/Users/lambert/Documents/GPE-Helper/judge/problems/10535/solution.py"],
        input="\n".join(tc["lines"]) + "\n",
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        print(f"ERROR on TC {tc_id}: {result.stderr}")
        continue

    with open(out_path, "w") as f:
        f.write(result.stdout)

    print(f"TC {tc_id}: OK")
    # Print first few lines of output for verification
    lines_out = result.stdout.strip().split("\n")
    for lo in lines_out[:3]:
        print(f"  -> {lo}")
    if len(lines_out) > 3:
        print(f"  ... ({len(lines_out)} lines total)")

print("Done!")
