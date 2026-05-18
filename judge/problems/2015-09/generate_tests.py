#!/usr/bin/env python3
"""
Test case generator for 2015-09: Longest Increasing Subsequence

Generates 18 test cases covering edge cases and corner cases:
 01: Sample from problem statement
 02: Single element
 03: Two elements, increasing
 04: Two elements, decreasing
 05: All same elements (LIS = 1)
 06: Strictly increasing (LIS = n)
 07: Strictly decreasing (LIS = 1)
 08: V-shape: decreasing then increasing
 09: Mountain shape: increasing then decreasing
 10: Alternating up-down pattern
 11: Already sorted with duplicates (strictly increasing => skip dups)
 12: Random small array (n=20)
 13: Medium random (n=500)
 14: Medium random with negative numbers (n=1000)
 15: Large random (n=10000)
 16: Large nearly sorted with some swaps (n=10000)
 17: Large random (n=65535, max n)
 18: Large decreasing with occasional spikes (n=50000)
"""
import random
import os

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2015-09/testcases"

def write_case(case_num, n, arr):
    """Write a single test case .in file."""
    fname = os.path.join(TESTCASE_DIR, f"{case_num:02d}.in")
    with open(fname, 'w') as f:
        f.write(f"{n}\n")
        f.write(' '.join(map(str, arr)) + '\n')

def main():
    random.seed(42)

    cases = []

    # 01: Sample from problem statement
    cases.append((8, [10, 9, 2, 5, 3, 7, 101, 18]))

    # 02: Single element
    cases.append((1, [42]))

    # 03: Two elements, increasing
    cases.append((2, [1, 2]))

    # 04: Two elements, decreasing
    cases.append((2, [5, 3]))

    # 05: All same elements => LIS = 1
    cases.append((10, [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]))

    # 06: Strictly increasing => LIS = n
    n = 15
    cases.append((n, list(range(1, n + 1))))

    # 07: Strictly decreasing => LIS = 1
    n = 15
    cases.append((n, list(range(n, 0, -1))))

    # 08: V-shape: decreasing then increasing
    arr = list(range(10, 0, -1)) + list(range(2, 12))
    cases.append((len(arr), arr))

    # 09: Mountain shape: increasing then decreasing
    arr = list(range(1, 11)) + list(range(9, 0, -1))
    cases.append((len(arr), arr))

    # 10: Alternating up-down pattern
    arr = []
    for i in range(20):
        if i % 2 == 0:
            arr.append(i * 2)
        else:
            arr.append(i * 2 - 3)
    cases.append((len(arr), arr))

    # 11: Sorted with duplicates => strictly increasing skips dups
    arr = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
    cases.append((len(arr), arr))

    # 12: Random small (n=20)
    n = 20
    arr = [random.randint(-100, 100) for _ in range(n)]
    cases.append((n, arr))

    # 13: Medium random (n=500)
    n = 500
    arr = [random.randint(-10000, 10000) for _ in range(n)]
    cases.append((n, arr))

    # 14: Medium random with negatives (n=1000)
    n = 1000
    arr = [random.randint(-1000000, 1000000) for _ in range(n)]
    cases.append((n, arr))

    # 15: Large random (n=10000)
    n = 10000
    arr = [random.randint(-1000000, 1000000) for _ in range(n)]
    cases.append((n, arr))

    # 16: Large nearly sorted with some swaps (n=10000)
    n = 10000
    arr = list(range(n))
    for _ in range(n // 10):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    cases.append((n, arr))

    # 17: Max n, random (n=65535)
    n = 65535
    arr = [random.randint(-2**31, 2**31 - 1) for _ in range(n)]
    cases.append((n, arr))

    # 18: Large decreasing with occasional spikes (n=50000)
    n = 50000
    arr = []
    val = 1000000
    for i in range(n):
        if random.random() < 0.05:  # 5% chance of spike
            arr.append(val + random.randint(1, 1000))
        else:
            val -= random.randint(0, 5)
            arr.append(val)
    cases.append((n, arr))

    # Write all .in files
    for i, (n, arr) in enumerate(cases, 1):
        write_case(i, n, arr)
        print(f"  Case {i:02d}: n={n}")

    print(f"\nGenerated {len(cases)} test cases (.in files).")

if __name__ == '__main__':
    main()
