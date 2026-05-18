#!/usr/bin/env python3
"""
Solve "Extend to Palindromes":
Given a string s, find the shortest palindrome formed by appending characters to the end of s.

Approach: Find the longest suffix of s that is already a palindrome.
Then prepend the reverse of the remaining prefix to the end.

We use KMP failure function on (reverse(s) + '#' + s) to find the longest
suffix of s that is a palindrome efficiently.
"""

import sys

def solve(s):
    if not s:
        return s
    rev = s[::-1]
    # Build: rev + '#' + s
    combined = rev + '#' + s
    n = len(combined)
    # KMP failure function
    fail = [0] * n
    k = 0
    for i in range(1, n):
        while k > 0 and combined[k] != combined[i]:
            k = fail[k - 1]
        if combined[k] == combined[i]:
            k += 1
        fail[i] = k
    # fail[-1] gives the length of the longest suffix of s that is a palindrome
    longest_palindrome_suffix = fail[-1]
    # We need to append reverse of s[0 : len(s) - longest_palindrome_suffix] to the end
    append = s[:len(s) - longest_palindrome_suffix][::-1]
    return s + append

def main():
    for line in sys.stdin:
        line = line.rstrip('\n').rstrip('\r')
        if line == '':
            continue
        print(solve(line))

if __name__ == '__main__':
    main()
