#!/usr/bin/env python3
"""
Glass Beads - Find the lexicographically smallest rotation of a circular string.
Uses Booth's algorithm (O(n) time, O(n) space).
Output: 1-indexed position of the starting bead for the smallest rotation.
"""

import sys

def booth(s):
    """Return the 0-indexed starting position of the lexicographically smallest rotation."""
    s = s + s  # concatenate string with itself
    n = len(s) // 2
    f = [-1] * len(s)
    k = 0  # current best starting index
    for j in range(1, len(s)):
        sj = s[j]
        i = f[j - 1 - k]
        while i != -1 and sj != s[k + i + 1]:
            if sj < s[k + i + 1]:
                k = j - i - 1
            i = f[i]
        if sj != s[k + i + 1]:
            if sj < s[k]:
                k = j
            f[j - k] = -1
        else:
            f[j - k] = i + 1
    return k


def solve():
    input_data = sys.stdin.read().split('\n')
    idx = 0
    n = int(input_data[idx].strip())
    idx += 1
    results = []
    for _ in range(n):
        s = input_data[idx].strip()
        idx += 1
        pos = booth(s)
        results.append(str(pos + 1))  # convert to 1-indexed
    print('\n'.join(results))


if __name__ == '__main__':
    solve()
