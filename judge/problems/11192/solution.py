import sys

def solve():
    """
    Problem: Simple Minded Hashing

    Count the number of strings of length L using lowercase letters in strictly
    ascending order that hash to sum S, where a=1, b=2, ..., z=26.

    This is equivalent to: how many L-element subsets of {1,2,...,26} have sum S?

    DP approach:
    dp[i][j][k] = number of ways to pick j elements from {1..i} with sum k

    Since L can be up to 9999 but we only have 26 letters, if L > 26 the answer is 0.
    The minimum sum for L letters is 1+2+...+L = L*(L+1)/2.
    The maximum sum for L letters is (27-L)+(28-L)+...+26 = sum of last L = L*(53-L)/2.
    If S is outside [min_sum, max_sum], answer is 0.

    We can use dp[letter][count][sum]:
    - letter from 1 to 26
    - count from 0 to min(L, 26)
    - sum from 0 to S (but bounded by 351)

    Since max possible sum = 1+2+...+26 = 351, if S > 351 answer is always 0.
    """
    case_num = 0
    results = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        L, S = int(parts[0]), int(parts[1])
        if L == 0 and S == 0:
            break
        case_num += 1

        # If L > 26 or L <= 0, impossible (but L > 0 per constraints)
        if L > 26:
            results.append(f"Case {case_num}: 0")
            continue

        min_sum = L * (L + 1) // 2
        max_sum = L * (53 - L) // 2

        if S < min_sum or S > max_sum:
            results.append(f"Case {case_num}: 0")
            continue

        # dp[j][k] = number of ways to choose j elements from letters considered so far
        # with sum k
        # We iterate over letters 1..26
        # Max useful sum is min(S, 351)
        target = S
        max_s = min(target, 351)

        # dp[count][sum]
        dp = [[0] * (max_s + 1) for _ in range(L + 1)]
        dp[0][0] = 1

        for letter in range(1, 27):
            # Iterate backwards on count to avoid using same letter twice
            for j in range(min(letter, L), 0, -1):
                for k in range(letter, max_s + 1):
                    dp[j][k] += dp[j-1][k - letter]

        results.append(f"Case {case_num}: {dp[L][target] if target <= max_s else 0}")

    print('\n'.join(results))

solve()
