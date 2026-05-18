import sys
import math

def solve_case(n):
    if n == 0:
        # Edge case: 0 pickups
        return "0.000000 0"

    # Probability of picking both red at step k (0-indexed):
    # p_k = 1/(1+k) * 1/(2+k)  for k = 0, 1, ..., n-1
    # After step k, one white ball added to each urn.
    # Step 0: urn1 has 1 ball, urn2 has 2 balls -> p = 1/1 * 1/2 = 1/2
    # Step 1: urn1 has 2 balls, urn2 has 3 balls -> p = 1/2 * 1/3 = 1/6
    # etc.

    # Probability all picks are red = product of p_k for k=0..n-1
    # = product(1/((1+k)*(2+k))) for k=0..n-1
    # = product(1/(k+1) * 1/(k+2)) for k=0..n-1
    # = 1/(n! * (n+1)!)  * 1!*2! ... hmm let me compute differently

    # p_k = 1/((k+1)*(k+2))
    # Product = product_{k=0}^{n-1} 1/((k+1)*(k+2))
    # = 1 / (product_{k=0}^{n-1} (k+1) * product_{k=0}^{n-1} (k+2))
    # = 1 / (n! * (n+1)!/1!)
    # = 1 / (n! * (n+1)!)

    # For the number of consecutive zeros after decimal point in this probability:
    # We need floor(-log10(product)) - but that might lose precision.
    # log10(product) = -sum_{k=0}^{n-1} log10((k+1)*(k+2))

    # For "probability at least one pickup has both red":
    # P(at least one) = 1 - P(none)
    # P(none both red) = product_{k=0}^{n-1} (1 - p_k)
    # = product_{k=0}^{n-1} (1 - 1/((k+1)*(k+2)))
    # = product_{k=0}^{n-1} ((k+1)*(k+2) - 1) / ((k+1)*(k+2))
    # = product_{k=0}^{n-1} (k^2 + 3k + 1) / ((k+1)*(k+2))

    # Let me compute P(none) iteratively
    prob_none = 1.0
    log_all = 0.0  # log10 of P(all red)

    for k in range(n):
        pk = 1.0 / ((k + 1) * (k + 2))
        prob_none *= (1.0 - pk)
        log_all += math.log10(pk)

    prob_at_least_one = 1.0 - prob_none

    # Number of consecutive zeros after decimal point in P(all red)
    # P(all red) = 10^(log_all)
    # If log_all = -5.3, then P = 0.000005..., zeros = 5
    # zeros = floor(-log_all) - 1 if it's exact power, otherwise floor(-log_all - 1)?
    # Actually: if P = 0.00...0X where X is first non-zero digit
    # Number of zeros = floor(-log10(P)) - 1? No.
    # If P = 0.5, log10(P) = -0.301, zeros = 0
    # If P = 0.05, log10(P) = -1.301, zeros = 1
    # zeros = ceil(-log10(P)) - 1 = ceil(0.301) - 1 = 1 - 1 = 0 for P=0.5 ✓
    # zeros = ceil(1.301) - 1 = 2 - 1 = 1 for P=0.05 ✓
    # But if P = 0.1, log10(P) = -1, zeros = 0
    # zeros = ceil(1) - 1 = 0 ✓
    # If P = 0.01, log10(P) = -2, zeros = 1
    # zeros = ceil(2) - 1 = 1 ✓

    # So zeros = ceil(-log10(P)) - 1 = ceil(-log_all) - 1
    # But we need to be careful with exact values
    # Actually: floor(-log10(P) - epsilon) for small epsilon?
    # Let me think again:
    # zeros after decimal = number of 0s before first nonzero digit after "0."
    # If P = A * 10^(-m) where 1 <= A < 10, then P = 0.000...0A... with (m-1) zeros
    # log10(P) = log10(A) + (-m), so m = -floor(log10(P))
    # zeros = m - 1 = -floor(log10(P)) - 1

    # For P=0.5: log10(0.5) = -0.301, floor = -1, -(-1)-1 = 0 ✓
    # For P=0.05: log10(0.05) = -1.301, floor = -2, -(-2)-1 = 1 ✓
    # For P=0.1: log10(0.1) = -1, floor = -1, -(-1)-1 = 0 ✓

    zeros = int(-math.floor(log_all)) - 1
    if zeros < 0:
        zeros = 0

    return f"{prob_at_least_one:.6f} {zeros}"

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    n = int(line)
    print(solve_case(n))
