#!/usr/bin/env python3
"""
Solver for 2015-09: Longest Increasing Subsequence
Uses O(n log n) patience sorting approach with bisect.
"""
import sys
import bisect

def lis_length(arr):
    """Return the length of the longest strictly increasing subsequence."""
    if not arr:
        return 0
    tails = []
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(input_data):
        n = int(input_data[idx]); idx += 1
        arr = []
        for i in range(n):
            arr.append(int(input_data[idx])); idx += 1
        results.append(str(lis_length(arr)))
    print('\n'.join(results))

if __name__ == '__main__':
    main()
