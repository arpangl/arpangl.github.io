import sys
import math

def extended_gcd(a, b):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y

def solve(n, c1, n1, c2, n2):
    """
    Find non-negative m1, m2 such that m1*n1 + m2*n2 = n
    minimizing m1*c1 + m2*c2.
    Returns (m1, m2) or None if impossible.
    """
    if n == 0:
        return (0, 0)

    g = math.gcd(n1, n2)
    if n % g != 0:
        return None

    # Reduce: n1' = n1/g, n2' = n2/g, n' = n/g
    # m1*n1' + m2*n2' = n'
    N1 = n1 // g
    N2 = n2 // g
    N = n // g

    # Extended GCD: N1*x0 + N2*y0 = 1
    _, x0, y0 = extended_gcd(N1, N2)

    # Particular solution: m1 = x0*N, m2 = y0*N
    # General solution: m1 = x0*N + k*N2, m2 = y0*N - k*N1
    # We need m1 >= 0 and m2 >= 0

    # m1 = x0*N + k*N2 >= 0  =>  k >= -x0*N / N2
    # m2 = y0*N - k*N1 >= 0  =>  k <= y0*N / N1

    # k_min = ceil(-x0*N / N2)
    # k_max = floor(y0*N / N1)

    base_m1 = x0 * N
    base_m2 = y0 * N

    # k_min: smallest k such that base_m1 + k*N2 >= 0
    # k >= -base_m1 / N2 => k_min = ceil(-base_m1 / N2)
    def ceildiv(a, b):
        """Ceiling division for integers, handles negative correctly."""
        if b > 0:
            return (a + b - 1) // b if a >= 0 else -((-a) // b)
        else:
            return ceildiv(-a, -b)  # should not happen since N1, N2 > 0

    def floordiv(a, b):
        """Floor division for integers."""
        if b > 0:
            return a // b if a >= 0 else -(((-a) + b - 1) // b)
        else:
            return floordiv(-a, -b)

    k_min = ceildiv(-base_m1, N2)
    k_max = floordiv(base_m2, N1)

    if k_min > k_max:
        return None

    # Cost = m1*c1 + m2*c2
    #       = (base_m1 + k*N2)*c1 + (base_m2 - k*N1)*c2
    #       = base_m1*c1 + base_m2*c2 + k*(N2*c1 - N1*c2)
    # To minimize cost:
    # If N2*c1 - N1*c2 > 0, we want smallest k => k = k_min
    # If N2*c1 - N1*c2 < 0, we want largest k => k = k_max
    # If N2*c1 - N1*c2 == 0, any k works (cost is same), pick k_min

    coeff = N2 * c1 - N1 * c2
    if coeff > 0:
        k = k_min
    elif coeff < 0:
        k = k_max
    else:
        k = k_min

    m1 = base_m1 + k * N2
    m2 = base_m2 - k * N1

    assert m1 >= 0 and m2 >= 0
    assert m1 * n1 + m2 * n2 == n

    return (m1, m2)

def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(input_data):
        n = int(input_data[idx]); idx += 1
        if n == 0:
            break
        c1 = int(input_data[idx]); idx += 1
        n1 = int(input_data[idx]); idx += 1
        c2 = int(input_data[idx]); idx += 1
        n2 = int(input_data[idx]); idx += 1

        res = solve(n, c1, n1, c2, n2)
        if res is None:
            results.append("failed")
        else:
            results.append(f"{res[0]} {res[1]}")

    print('\n'.join(results))

if __name__ == '__main__':
    main()
