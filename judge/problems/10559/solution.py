#!/usr/bin/env python3
"""
Problem 10559: I Love Big Numbers !
Given n, compute n!, then output the sum of digits of n!.
n <= 1000, multiple test cases until EOF.
"""

import math
import sys

def digit_sum_of_factorial(n):
    f = math.factorial(n)
    return sum(int(d) for d in str(f))

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    n = int(line)
    print(digit_sum_of_factorial(n))
