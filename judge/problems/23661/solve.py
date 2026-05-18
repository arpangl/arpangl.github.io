import sys

def solve(N, L, U):
    """
    Find minimum M in [L, U] such that N OR M is maximized.

    Strategy: We want to maximize N | M. Bits where N already has a 1 don't matter
    for the OR value, so we focus on bits where N has a 0 -- we want those to be 1 in M.

    We build M bit by bit from MSB to LSB. At each bit position:
    - If N has a 1 at this bit: the OR result has 1 regardless. We prefer M to have 0
      here (to keep M small), but only if M stays in [L, U].
    - If N has a 0 at this bit: we want M to have 1 here (to maximize OR), but only
      if M stays in [L, U].

    We use a greedy approach: maintain a candidate M, and at each bit from high to low,
    try the preferred choice. If it's feasible (i.e., we can still find a value in [L, U]
    with the bits we've fixed so far), keep it; otherwise, take the other choice.
    """
    # Greedy bit-by-bit from bit 31 down to bit 0
    M = 0
    for bit in range(31, -1, -1):
        mask = 1 << bit
        n_bit = (N >> bit) & 1

        if n_bit == 1:
            # OR is 1 regardless. Prefer M bit = 0 (minimize M).
            # Try setting this bit to 0
            candidate = M  # bit is already 0
            # Check: can we find a value in [L, U] with these high bits fixed?
            # The minimum value with current prefix and remaining bits all 0 is candidate
            # The maximum value with current prefix and remaining bits all 1 is candidate | (mask - 1)
            lo = candidate
            hi = candidate | (mask - 1)
            if lo <= U and hi >= L:
                M = candidate  # keep bit 0
            else:
                M = M | mask  # must set bit 1
        else:
            # N bit is 0. Prefer M bit = 1 (maximize OR).
            candidate = M | mask
            lo = candidate
            hi = candidate | (mask - 1)
            if lo <= U and hi >= L:
                M = candidate  # set bit 1
            else:
                M = M  # keep bit 0

    return M

def brute_force(N, L, U):
    """Brute force for verification on small ranges."""
    best_or = -1
    best_m = -1
    for m in range(L, U + 1):
        val = N | m
        if val > best_or or (val == best_or and m < best_m):
            best_or = val
            best_m = m
    return best_m

# Read from stdin and produce output
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) < 3:
        continue
    N, L, U = int(parts[0]), int(parts[1]), int(parts[2])
    print(solve(N, L, U))
