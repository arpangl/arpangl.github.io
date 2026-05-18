#!/usr/bin/env python3
"""
Generate test cases for problem 10471: COUNTING CHAOS

Test case strategy:
01: Sample input
02: All single-digit palindromes in hour 0 (edge: HH=00)
03: Current time is a palindrome (must find NEXT one)
04: Wrapping around midnight (23:59 and similar late times)
05: All two-digit hour palindromic times as input (10:01, 11:11, etc.)
06: Times just before each palindrome
07: Times just after a palindrome (long gap to next)
08: Hour 00 with various minutes
09: Hour boundaries (XX:59 transitions)
10: Minute 00 for various hours
11: Maximum gap scenarios
12: All times at XX:00
13: Random spread across the day
14: Edge: every palindromic time as input
15: Edge: 23:32 (last palindrome before midnight wrap)
16: Large input (stress test with many queries)
17: Times one minute before midnight wrap palindromes
18: Boundary: all HH:59 times
"""

import os
import sys

def is_palindromic_time(h, m):
    if h == 0:
        s = str(m)
    else:
        s = str(h) + '%02d' % m
    return s == s[::-1]

def next_time(h, m):
    m += 1
    if m >= 60:
        m = 0
        h += 1
        if h >= 24:
            h = 0
    return h, m

def find_next_palindrome(h, m):
    h, m = next_time(h, m)
    while not is_palindromic_time(h, m):
        h, m = next_time(h, m)
    return h, m

def solve_case(time_str):
    parts = time_str.split(':')
    h, m = int(parts[0]), int(parts[1])
    nh, nm = find_next_palindrome(h, m)
    return "%02d:%02d" % (nh, nm)

def write_test(test_dir, test_num, times):
    in_path = os.path.join(test_dir, "%02d.in" % test_num)
    out_path = os.path.join(test_dir, "%02d.out" % test_num)

    in_lines = [str(len(times))]
    out_lines = []
    for t in times:
        in_lines.append(t)
        out_lines.append(solve_case(t))

    with open(in_path, 'w') as f:
        f.write('\n'.join(in_lines) + '\n')
    with open(out_path, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f"Test {test_num:02d}: {len(times)} cases written")

def main():
    test_dir = "/Users/lambert/Documents/GPE-Helper/judge/problems/10471/testcases"
    os.makedirs(test_dir, exist_ok=True)

    test_num = 1

    # Test 01: Sample input
    write_test(test_dir, test_num, ["00:00", "23:30", "14:59"])
    test_num += 1

    # Test 02: All single-digit minute palindromes in hour 0
    # When HH=00, palindromic minutes are 0-9 (single digit always palindrome), 11, 22, 33, 44, 55
    write_test(test_dir, test_num, [
        "00:00", "00:01", "00:02", "00:03", "00:04",
        "00:05", "00:06", "00:07", "00:08", "00:09"
    ])
    test_num += 1

    # Test 03: Current time IS a palindrome - must find NEXT
    write_test(test_dir, test_num, [
        "01:01",  # palindrome, next is 01:11
        "11:11",  # palindrome, next is 12:21
        "22:22",  # palindrome, next is 23:32
        "23:32",  # last 4-digit palindrome, next wraps to 00:00
        "00:09",  # palindrome, next is 00:11
        "09:59",  # palindrome, next is 10:01
    ])
    test_num += 1

    # Test 04: Wrapping around midnight
    write_test(test_dir, test_num, [
        "23:32",  # palindrome, next is 00:00
        "23:33",  # next palindrome is 00:00
        "23:50",  # next is 00:00
        "23:59",  # next is 00:00
    ])
    test_num += 1

    # Test 05: Two-digit hour palindromic times as input
    write_test(test_dir, test_num, [
        "10:01", "11:11", "12:21", "13:31",
        "14:41", "15:51", "20:02", "21:12",
        "22:22", "23:32"
    ])
    test_num += 1

    # Test 06: Times just BEFORE a palindrome (1 minute before)
    write_test(test_dir, test_num, [
        "00:10",  # next is 00:11
        "01:00",  # next is 01:01
        "10:00",  # next is 10:01
        "11:10",  # next is 11:11
        "12:20",  # next is 12:21
        "20:01",  # next is 20:02
        "22:21",  # next is 22:22
        "23:31",  # next is 23:32
    ])
    test_num += 1

    # Test 07: Times just AFTER a palindrome (long gap to next)
    write_test(test_dir, test_num, [
        "09:59",  # this IS a palindrome actually (959), next: 10:01
        "10:02",  # next palindrome: 11:11 (long gap)
        "15:52",  # next: 20:02 (very long gap!)
        "23:33",  # next: 00:00 (wraps)
        "00:56",  # next: 01:01
    ])
    test_num += 1

    # Test 08: Hour 00 with various minutes
    write_test(test_dir, test_num, [
        "00:10",  # between 9 and 11
        "00:12",  # between 11 and 22
        "00:23",  # between 22 and 33
        "00:34",  # between 33 and 44
        "00:45",  # between 44 and 55
        "00:56",  # between 55 and 01:01
        "00:59",  # last minute of hour 0
    ])
    test_num += 1

    # Test 09: Hour boundaries (XX:59)
    write_test(test_dir, test_num, [
        "00:59", "01:59", "02:59", "03:59", "04:59", "05:59",
        "06:59", "07:59", "08:59", "09:59", "10:59", "11:59",
    ])
    test_num += 1

    # Test 10: More hour boundaries
    write_test(test_dir, test_num, [
        "12:59", "13:59", "14:59", "15:59", "16:59", "17:59",
        "18:59", "19:59", "20:59", "21:59", "22:59", "23:59",
    ])
    test_num += 1

    # Test 11: XX:00 for all hours
    write_test(test_dir, test_num, [
        "%02d:00" % h for h in range(24)
    ])
    test_num += 1

    # Test 12: "Dead zones" - hours with no palindromes (16, 17, 18, 19)
    write_test(test_dir, test_num, [
        "16:00", "16:30", "17:00", "17:30",
        "18:00", "18:30", "19:00", "19:30",
    ])
    test_num += 1

    # Test 13: Random spread across the day
    write_test(test_dir, test_num, [
        "02:17", "05:30", "07:42", "09:15",
        "11:45", "13:00", "16:22", "19:55",
        "21:08", "23:01",
    ])
    test_num += 1

    # Test 14: Every palindromic time as input (all 79)
    palindromes = []
    for h in range(24):
        for m in range(60):
            if is_palindromic_time(h, m):
                palindromes.append("%02d:%02d" % (h, m))
    write_test(test_dir, test_num, palindromes)
    test_num += 1

    # Test 15: Times that are "almost" palindromic (off by 1 in last digit)
    write_test(test_dir, test_num, [
        "01:02",  # 102, palindrome is 101 (01:01) -> next 01:11
        "02:03",  # 203 -> next 02:12
        "11:12",  # 1112 -> next 12:21
        "22:23",  # 2223 -> next 23:32
        "20:03",  # 2003 -> next 21:12
        "13:30",  # 1330 -> next 13:31
        "14:40",  # 1440 -> next 14:41
    ])
    test_num += 1

    # Test 16: Stress test - many queries
    import random
    random.seed(42)
    stress_times = []
    for _ in range(200):
        h = random.randint(0, 23)
        m = random.randint(0, 59)
        stress_times.append("%02d:%02d" % (h, m))
    write_test(test_dir, test_num, stress_times)
    test_num += 1

    # Test 17: Single query edge cases
    write_test(test_dir, test_num, [
        "00:00",  # midnight
    ])
    test_num += 1

    # Test 18: The gap between 15:51 and 20:02 (longest gap)
    write_test(test_dir, test_num, [
        "15:51",  # palindrome -> next 20:02
        "15:52",  # next 20:02
        "16:00",  # next 20:02
        "18:00",  # next 20:02
        "19:59",  # next 20:02
        "20:01",  # next 20:02
        "20:02",  # palindrome -> next 21:12
    ])
    test_num += 1

    print(f"\nTotal test cases generated: {test_num - 1}")

if __name__ == '__main__':
    main()
