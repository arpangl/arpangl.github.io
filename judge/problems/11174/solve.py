import sys

def solve(m, n, t):
    """
    Find max burgers Homer can eat in exactly t minutes.
    Two burger types take m and n minutes respectively.
    Maximize number of burgers (a+b), minimize remaining time (t - a*m - b*n).

    Returns (max_burgers, remaining_time).
    """
    best_burgers = -1
    best_remain = t  # worst case: no burgers at all, all time wasted

    # Try all possible counts of burger type 1 (takes m minutes each)
    # a ranges from 0 to t//m
    for a in range(t // m + 1):
        remaining = t - a * m
        if remaining < 0:
            break
        b = remaining // n
        waste = remaining - b * n
        total = a + b
        if waste < best_remain or (waste == best_remain and total > best_burgers):
            best_remain = waste
            best_burgers = total

    return best_burgers, best_remain

def format_output(burgers, remain):
    if remain == 0:
        return str(burgers)
    else:
        return f"{burgers} {remain}"

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        m, n, t = int(parts[0]), int(parts[1]), int(parts[2])
        burgers, remain = solve(m, n, t)
        print(format_output(burgers, remain))
