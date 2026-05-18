#!/usr/bin/env python3
"""
Safe Salutations - Problem 10501
The answer for n pairs is the n-th Catalan number: C(n) = C(2n, n) / (n+1)

Input: multiple datasets separated by blank lines. Each dataset is an integer n.
Output: Catalan number for n, with blank lines between datasets.
"""

import sys
from math import comb

def catalan(n):
    return comb(2 * n, n) // (n + 1)

def solve(input_text):
    # Split input into lines, strip whitespace
    lines = input_text.strip().split('\n')

    datasets = []
    current = []
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            if current:
                datasets.append(current)
                current = []
        else:
            current.append(stripped)
    if current:
        datasets.append(current)

    results = []
    for dataset in datasets:
        # Each dataset is a single integer n
        n = int(dataset[0])
        results.append(str(catalan(n)))

    # Print with blank lines between datasets
    return '\n\n'.join(results) + '\n'

if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text), end='')
