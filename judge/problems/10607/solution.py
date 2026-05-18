#!/usr/bin/env python3
"""
Joseph's Cousin (10607)

n people in a circle numbered 1..n.
Elimination proceeds: the i-th elimination counts the i-th prime number of people.
  Round 1: count 2 (1st prime)
  Round 2: count 3 (2nd prime)
  Round 3: count 5 (3rd prime)
  ...
Output the last survivor's original position (1-indexed).
"""

import sys

def sieve_primes(limit):
    """Generate primes up to limit using Sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

# We need at most 3500 primes (for n=3501, we eliminate 3500 people)
# The 3500th prime is around 32600, so sieve up to 35000 to be safe
PRIMES = sieve_primes(35000)

def solve(n):
    if n == 1:
        return 1
    # Circle of people numbered 1..n
    circle = list(range(1, n + 1))
    idx = 0  # current index in circle
    for i in range(n - 1):
        p = PRIMES[i]  # i-th prime (0-indexed: PRIMES[0]=2, PRIMES[1]=3, ...)
        # Count p people from current position (1-indexed counting)
        # The person eliminated is at index (idx + p - 1) % len(circle)
        idx = (idx + p - 1) % len(circle)
        circle.pop(idx)
        # After removal, idx now points to the next person (or wraps)
        if idx == len(circle):
            idx = 0
    return circle[0]

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        if n == 0:
            break
        print(solve(n))

if __name__ == "__main__":
    main()
