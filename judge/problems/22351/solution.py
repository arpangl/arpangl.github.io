import sys

def find_quirksome(n):
    """Find all quirksome squares with n digits."""
    results = []
    half = n // 2
    upper = 10 ** n
    divisor = 10 ** half
    # We iterate over possible sums a+b and check if (a+b)^2 gives back
    # a number whose left and right halves sum to a+b.
    # The number has n digits, so it ranges from 0 to 10^n - 1.
    # (a+b)^2 must be < 10^n, so a+b < 10^(n/2) * ... let's just iterate.
    # Actually simpler: iterate s from 0 to max possible sum.
    # a can be 0..10^(n/2)-1, b can be 0..10^(n/2)-1
    # so s = a + b ranges from 0 to 2*(10^(n/2)-1)
    # Then check if s^2 is an n-digit number (with leading zeros, so 0 to 10^n-1)
    # and if the left half + right half == s.

    max_s = 2 * (divisor - 1)
    for s in range(max_s + 1):
        sq = s * s
        if sq >= upper:
            break
        left = sq // divisor
        right = sq % divisor
        if left + right == s:
            results.append(str(sq).zfill(n))
    return results

def solve():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        results = find_quirksome(n)
        for r in results:
            print(r)

if __name__ == '__main__':
    solve()
