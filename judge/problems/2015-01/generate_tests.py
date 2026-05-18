#!/usr/bin/env python3
"""
Generate test cases for 2015-01: Missing Numbers

Constraints:
- M lists, N numbers in 1st list
- M < N
- M * N <= 5,000,000
- All integers < 65536
- i-th list has (N - i + 1) numbers
- One and only one number in i-th list is missing in (i+1)-th list
"""

import random
import os

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/2015-01/testcases"


def solve(input_data):
    """Solve the Missing Numbers problem."""
    lines = input_data.strip().split('\n')
    first = lines[0].split()
    M = int(first[0])
    N = int(first[1])

    results = []
    prev_list = list(map(int, lines[1].split()))

    for i in range(2, M + 1):
        curr_list = list(map(int, lines[i].split()))
        prev_sum = sum(prev_list)
        curr_sum = sum(curr_list)
        missing = prev_sum - curr_sum
        results.append(str(missing))
        prev_list = curr_list

    return '\n'.join(results) + '\n' if results else ''


def generate_case(M, N, nums=None, missing_indices=None, max_val=65535):
    """
    Generate a test case.
    M: number of lists
    N: number of elements in the first list
    nums: optional first list of numbers
    missing_indices: optional list of indices to remove (length M-1)
    max_val: max value for random numbers
    """
    if nums is None:
        nums = random.sample(range(0, min(max_val + 1, max(N * 2, 100))), N)

    lines = [f"{M} {N}"]
    current = list(nums)
    random.shuffle(current)
    lines.append(' '.join(map(str, current)))

    missing_numbers = []
    for i in range(M - 1):
        if missing_indices is not None:
            idx = missing_indices[i]
        else:
            idx = random.randint(0, len(current) - 1)
        missing_numbers.append(current[idx])
        current = current[:idx] + current[idx+1:]
        random.shuffle(current)
        lines.append(' '.join(map(str, current)))

    input_data = '\n'.join(lines) + '\n'
    output_data = '\n'.join(map(str, missing_numbers)) + '\n'
    return input_data, output_data


def write_case(case_num, input_data, output_data):
    """Write a test case to files."""
    prefix = f"{case_num:02d}"
    in_path = os.path.join(TESTCASE_DIR, f"{prefix}.in")
    out_path = os.path.join(TESTCASE_DIR, f"{prefix}.out")
    with open(in_path, 'w') as f:
        f.write(input_data)
    with open(out_path, 'w') as f:
        f.write(output_data)
    # Verify
    computed = solve(input_data)
    assert computed == output_data, (
        f"Case {case_num} MISMATCH!\n"
        f"Expected:\n{output_data}\n"
        f"Got:\n{computed}"
    )
    print(f"Case {prefix}: M={input_data.split()[0]}, N={input_data.split()[1]} -- OK")


def main():
    random.seed(42)
    case_num = 0

    # =========================================================================
    # Case 01: Sample case from problem statement
    # =========================================================================
    case_num += 1
    inp = "3 5\n13766 1891 5370 24317 30676\n13766 5370 30676 24317\n24317 5370 13766\n"
    out = "1891\n30676\n"
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 02: Minimum M=2, N=2 (smallest valid case)
    # =========================================================================
    case_num += 1
    inp_data, out_data = generate_case(2, 2, nums=[1, 2])
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 03: M=2, N=3 - simple small case
    # =========================================================================
    case_num += 1
    inp_data, out_data = generate_case(2, 3, nums=[10, 20, 30])
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 04: All zeros except the missing one
    # =========================================================================
    case_num += 1
    nums = [0, 0, 0, 0, 42]
    # Build manually to handle duplicates properly
    lines = ["2 5"]
    current = [0, 42, 0, 0, 0]
    lines.append(' '.join(map(str, current)))
    # Remove 42
    current2 = [0, 0, 0, 0]
    lines.append(' '.join(map(str, current2)))
    inp = '\n'.join(lines) + '\n'
    out = '42\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 05: Numbers include 0
    # =========================================================================
    case_num += 1
    inp_data, out_data = generate_case(3, 5, nums=[0, 1, 2, 3, 4])
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 06: All numbers are the same value (duplicates allowed by sum trick)
    # Actually, the problem says "one number is missing", with duplicates the
    # sum approach still works. But let's use distinct numbers to be safe.
    # Sequential numbers 1..N, remove first element each time
    # =========================================================================
    case_num += 1
    M, N = 5, 10
    nums = list(range(1, N + 1))
    # Remove specific indices: always remove index 0
    missing_indices = [0] * (M - 1)
    inp_data, out_data = generate_case(M, N, nums=nums, missing_indices=missing_indices)
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 07: Remove last element each time
    # =========================================================================
    case_num += 1
    M, N = 5, 10
    nums = list(range(100, 100 + N))
    # We need to generate manually since indices shift
    lines = [f"{M} {N}"]
    current = list(nums)
    random.shuffle(current)
    lines.append(' '.join(map(str, current)))
    missing_numbers = []
    for i in range(M - 1):
        idx = len(current) - 1  # always remove last
        missing_numbers.append(current[idx])
        current = current[:idx]
        random.shuffle(current)
        lines.append(' '.join(map(str, current)))
    inp = '\n'.join(lines) + '\n'
    out = '\n'.join(map(str, missing_numbers)) + '\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 08: Numbers near max value (65535)
    # =========================================================================
    case_num += 1
    M, N = 4, 8
    nums = [65530, 65531, 65532, 65533, 65534, 65535, 0, 1]
    inp_data, out_data = generate_case(M, N, nums=nums)
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 09: N = M+1 (minimum valid: each list shrinks to size 2 at the end)
    # =========================================================================
    case_num += 1
    M, N = 9, 10
    nums = list(range(10, 20))
    inp_data, out_data = generate_case(M, N, nums=nums)
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 10: M=2, large N (stress: sum-based)
    # M*N = 2 * 2_500_000 = 5_000_000 (max allowed)
    # =========================================================================
    case_num += 1
    M, N = 2, 2500000
    nums = random.sample(range(0, 65536), min(N, 65536))
    # If N > 65536 we can't have all unique under 65536, but N=2500000 > 65536
    # So we need to allow duplicates. Let's pick N random values < 65536.
    nums = [random.randint(0, 65535) for _ in range(N)]
    current = list(nums)
    random.shuffle(current)
    remove_idx = random.randint(0, N - 1)
    missing_val = current[remove_idx]
    current2 = current[:remove_idx] + current[remove_idx+1:]
    random.shuffle(current2)
    lines = [f"{M} {N}"]
    lines.append(' '.join(map(str, current)))
    lines.append(' '.join(map(str, current2)))
    inp = '\n'.join(lines) + '\n'
    out = f'{missing_val}\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 11: Medium case M=100, N=1000
    # =========================================================================
    case_num += 1
    M, N = 100, 1000
    nums = [random.randint(0, 65535) for _ in range(N)]
    lines = [f"{M} {N}"]
    current = list(nums)
    random.shuffle(current)
    lines.append(' '.join(map(str, current)))
    missing_numbers = []
    for i in range(M - 1):
        idx = random.randint(0, len(current) - 1)
        missing_numbers.append(current[idx])
        current = current[:idx] + current[idx+1:]
        random.shuffle(current)
        lines.append(' '.join(map(str, current)))
    inp = '\n'.join(lines) + '\n'
    out = '\n'.join(map(str, missing_numbers)) + '\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 12: Large M, moderate N. M=1000, N=1001
    # M*N = 1_001_000 < 5_000_000
    # =========================================================================
    case_num += 1
    M, N = 1000, 1001
    nums = [random.randint(0, 65535) for _ in range(N)]
    lines = [f"{M} {N}"]
    current = list(nums)
    random.shuffle(current)
    lines.append(' '.join(map(str, current)))
    missing_numbers = []
    for i in range(M - 1):
        idx = random.randint(0, len(current) - 1)
        missing_numbers.append(current[idx])
        current = current[:idx] + current[idx+1:]
        random.shuffle(current)
        lines.append(' '.join(map(str, current)))
    inp = '\n'.join(lines) + '\n'
    out = '\n'.join(map(str, missing_numbers)) + '\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 13: All numbers are 0 except one per list
    # =========================================================================
    case_num += 1
    M, N = 3, 6
    nums = [0, 0, 0, 5000, 10000, 65535]
    inp_data, out_data = generate_case(M, N, nums=nums)
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 14: Consecutive integers starting from 0
    # =========================================================================
    case_num += 1
    M, N = 6, 20
    nums = list(range(0, 20))
    inp_data, out_data = generate_case(M, N, nums=nums)
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 15: Large N with M=2 (another big case, different structure)
    # N = 1_000_000, M = 5 -> M*N = 5_000_000
    # =========================================================================
    case_num += 1
    M, N = 5, 1000000
    nums = [random.randint(0, 65535) for _ in range(N)]
    lines = [f"{M} {N}"]
    current = list(nums)
    random.shuffle(current)
    lines.append(' '.join(map(str, current)))
    missing_numbers = []
    for i in range(M - 1):
        idx = random.randint(0, len(current) - 1)
        missing_numbers.append(current[idx])
        current = current[:idx] + current[idx+1:]
        random.shuffle(current)
        lines.append(' '.join(map(str, current)))
    inp = '\n'.join(lines) + '\n'
    out = '\n'.join(map(str, missing_numbers)) + '\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 16: Single missing number (M=2, N=2) - minimum with value 0 missing
    # =========================================================================
    case_num += 1
    lines = ["2 2", "0 65535", "65535"]
    inp = '\n'.join(lines) + '\n'
    out = '0\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 17: M=2, N=2, max value missing
    # =========================================================================
    case_num += 1
    lines = ["2 2", "65535 0", "0"]
    inp = '\n'.join(lines) + '\n'
    out = '65535\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 18: Medium case with many lists (M=50, N=100)
    # =========================================================================
    case_num += 1
    M, N = 50, 100
    nums = random.sample(range(0, 65536), N)
    inp_data, out_data = generate_case(M, N, nums=nums)
    write_case(case_num, inp_data, out_data)

    # =========================================================================
    # Case 19: Stress - large M*N near limit: M=2236, N=2237 (M*N ~ 5,000,132)
    # Adjust so M*N <= 5,000,000: M=2235, N=2236 -> 4,996,260
    # =========================================================================
    case_num += 1
    M, N = 2235, 2236
    nums = [random.randint(0, 65535) for _ in range(N)]
    lines = [f"{M} {N}"]
    current = list(nums)
    random.shuffle(current)
    lines.append(' '.join(map(str, current)))
    missing_numbers = []
    for i in range(M - 1):
        idx = random.randint(0, len(current) - 1)
        missing_numbers.append(current[idx])
        current = current[:idx] + current[idx+1:]
        random.shuffle(current)
        lines.append(' '.join(map(str, current)))
    inp = '\n'.join(lines) + '\n'
    out = '\n'.join(map(str, missing_numbers)) + '\n'
    write_case(case_num, inp, out)

    # =========================================================================
    # Case 20: Duplicate values in lists
    # =========================================================================
    case_num += 1
    M, N = 4, 8
    nums = [100, 100, 200, 200, 300, 300, 400, 500]
    inp_data, out_data = generate_case(M, N, nums=nums)
    write_case(case_num, inp_data, out_data)

    print(f"\nTotal test cases generated: {case_num}")


if __name__ == '__main__':
    main()
