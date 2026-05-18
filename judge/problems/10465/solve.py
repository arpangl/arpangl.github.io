import sys
import math

def solve(v_total, v0):
    """
    Necklace length with n discs:
      L(n) = n * 0.3 * sqrt(V_total/n - V0)  if V_total/n > V0
      L(n) = 0                                 otherwise

    We need n >= 1 (integer) and V_total/n > V0, i.e. n < V_total/V0.

    Max n we can try: floor(V_total/V0 - epsilon). If V_total/V0 is integer,
    then n = V_total/V0 gives V_total/n = V0 exactly, so D=0, no disc.
    So valid n: 1 <= n <= floor((V_total/V0) - 1e-9) but n must be at least 1.

    If no valid n exists, output 0.
    If the maximum length is achieved by more than one n, output 0.
    """
    # Max valid n: largest integer n such that V_total/n > V0
    # i.e. n < V_total/V0
    if v_total <= v0:
        return 0

    max_n = int(v_total / v0)
    # Check: if max_n * v0 >= v_total, then V_total/max_n <= V0, not valid
    # We need V_total/n > V0 strictly
    while max_n >= 1 and v_total <= max_n * v0:
        max_n -= 1

    if max_n < 1:
        return 0

    best_length = -1.0
    best_n = 0
    unique = True

    for n in range(1, max_n + 1):
        v_each = v_total / n
        if v_each <= v0:
            break
        length = n * 0.3 * math.sqrt(v_each - v0)
        if length > best_length + 1e-9:
            best_length = length
            best_n = n
            unique = True
        elif abs(length - best_length) < 1e-9:
            unique = False

    if not unique:
        return 0
    return best_n

def main():
    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        v_total = int(parts[0])
        v0 = int(parts[1])
        if v_total == 0 and v0 == 0:
            break
        print(solve(v_total, v0))

if __name__ == "__main__":
    main()
