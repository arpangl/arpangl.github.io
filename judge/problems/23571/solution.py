import sys

def digit_sum(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s

def prime_factor_digit_sum(n):
    """Return sum of digits of all prime factors (with multiplicity)."""
    s = 0
    original = n
    d = 2
    while d * d <= n:
        while n % d == 0:
            s += digit_sum(d)
            n //= d
        d += 1
    if n > 1:
        s += digit_sum(n)
    # Check if original is prime (only one prime factor equal to itself)
    # A prime number: n was reduced to 1 only if original == prime factor
    return s, (n == 1 and s == digit_sum(original) and original > 1 and is_prime_check(original))

def is_prime_check(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_smith(n):
    """Check if n is a Smith number."""
    if n < 4:
        return False
    if is_prime_check(n):
        return False
    # Compute digit sum of n
    ds = digit_sum(n)
    # Compute sum of digit sums of prime factors with multiplicity
    pf_ds = 0
    temp = n
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            pf_ds += digit_sum(d)
            temp //= d
        d += 1
    if temp > 1:
        pf_ds += digit_sum(temp)
    return ds == pf_ds

def next_smith(n):
    """Find the smallest Smith number > n."""
    candidate = n + 1
    while True:
        if is_smith(candidate):
            return candidate
        candidate += 1

def solve():
    input_data = sys.stdin.read().split()
    t = int(input_data[0])
    results = []
    for i in range(1, t + 1):
        n = int(input_data[i])
        results.append(str(next_smith(n)))
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
