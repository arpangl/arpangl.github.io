#!/usr/bin/env python3
"""
Sum of Consecutive Prime Numbers
Given a positive integer N, count how many ways it can be represented
as a sum of one or more consecutive prime numbers.
"""

import sys

def sieve(limit):
    """Return list of primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [x for x in range(2, limit + 1) if is_prime[x]]

# Precompute primes up to 10000
PRIMES = sieve(10000)

def count_representations(n):
    """Count number of ways n can be expressed as sum of consecutive primes."""
    count = 0
    for i in range(len(PRIMES)):
        if PRIMES[i] > n:
            break
        s = 0
        for j in range(i, len(PRIMES)):
            s += PRIMES[j]
            if s == n:
                count += 1
                break
            elif s > n:
                break
    return count

def solve(input_text):
    """Process input and return output."""
    lines = input_text.strip().split('\n')
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        if n == 0:
            break
        results.append(str(count_representations(n)))
    return '\n'.join(results)

if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text))
