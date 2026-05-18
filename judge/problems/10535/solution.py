import sys
import math

def sieve_small(limit):
    """Standard sieve of Eratosthenes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

def segmented_sieve(L, U):
    """Find all primes in [L, U] using segmented sieve."""
    if U < 2:
        return []
    L = max(L, 2)

    # We need primes up to sqrt(U) to sieve the segment
    sqrt_u = int(math.isqrt(U)) + 1
    small_primes = sieve_small(sqrt_u)

    size = U - L + 1
    is_prime = [True] * size

    # If L == 1, mark it as not prime
    if L <= 1:
        is_prime[1 - L] = False
    if L == 0:
        is_prime[0] = False

    for p in small_primes:
        # Find the first multiple of p >= L
        start = ((L + p - 1) // p) * p
        if start == p:
            start += p  # p itself is prime, skip it
        for j in range(start, U + 1, p):
            is_prime[j - L] = False

    primes = []
    for i in range(size):
        if is_prime[i]:
            primes.append(L + i)
    return primes

def solve(L, U):
    primes = segmented_sieve(L, U)

    if len(primes) < 2:
        return "There are no adjacent primes."

    min_gap = float('inf')
    max_gap = 0
    closest = None
    distant = None

    for i in range(1, len(primes)):
        gap = primes[i] - primes[i - 1]
        if gap < min_gap:
            min_gap = gap
            closest = (primes[i - 1], primes[i])
        if gap > max_gap:
            max_gap = gap
            distant = (primes[i - 1], primes[i])

    return f"{closest[0]},{closest[1]} are closest, {distant[0]},{distant[1]} are most distant."

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        L, U = int(parts[0]), int(parts[1])
        print(solve(L, U))

if __name__ == "__main__":
    main()
