import sys
import math

def solve(S, D):
    """
    Groups of size S, S+1, S+2, ... arrive.
    Group of size n stays n days.
    Cumulative days after k groups (0-indexed: group 0 has size S, group 1 has size S+1, ...):
      sum = S + (S+1) + ... + (S+k) = (k+1)*S + k*(k+1)/2

    We need smallest k >= 0 such that (k+1)*S + k*(k+1)/2 >= D.

    Let m = k+1 (number of groups, m >= 1):
      m*S + m*(m-1)/2 >= D
      m^2/2 + m*(S - 1/2) >= D
      m^2 + m*(2S - 1) >= 2D
      m^2 + (2S-1)*m - 2D >= 0

    Using quadratic formula:
      m = (-(2S-1) + sqrt((2S-1)^2 + 8D)) / 2

    The group size on day D is S + k = S + m - 1.
    """
    # Use quadratic formula to get approximate m, then check nearby values
    a = 1
    b = 2 * S - 1
    c = -2 * D

    discriminant = b * b - 4 * a * c  # b^2 + 8D
    m_approx = (-b + math.isqrt(discriminant)) // (2 * a)

    # m_approx might be slightly off, so check m_approx-1, m_approx, m_approx+1
    # We need: m*S + m*(m-1)/2 >= D, and (m-1)*S + (m-1)*(m-2)/2 < D
    # i.e., the cumulative days after m groups >= D, but after m-1 groups < D

    def cumulative(m):
        """Total days occupied by first m groups (sizes S, S+1, ..., S+m-1)."""
        if m <= 0:
            return 0
        return m * S + m * (m - 1) // 2

    m = max(1, m_approx)

    # Adjust downward if we overshot
    while m > 1 and cumulative(m - 1) >= D:
        m -= 1

    # Adjust upward if we undershot
    while cumulative(m) < D:
        m += 1

    # The m-th group has size S + m - 1
    return S + m - 1


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        S = int(parts[0])
        D = int(parts[1])
        print(solve(S, D))


if __name__ == "__main__":
    main()
