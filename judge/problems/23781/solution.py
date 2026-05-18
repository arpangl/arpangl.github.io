import sys
from itertools import product

def solve():
    """
    Making Change (UVa 166)

    Coins: 5c, 10c, 20c, 50c, $1(100c), $2(200c)
    You have limited coins. Shopkeeper has unlimited coins.

    For each amount you could tender (>= price), compute:
      - coins_paid: number of your coins used to make up that tender amount
      - coins_change: minimum coins shopkeeper gives back (greedy on change amount)
      - total = coins_paid + coins_change
    Minimize total.

    The shopkeeper gives change optimally (greedy works for NZ coin system).
    """
    coin_values = [5, 10, 20, 50, 100, 200]

    results = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 7:
            continue

        counts = [int(parts[i]) for i in range(6)]

        # Check termination
        if all(c == 0 for c in counts):
            break

        # Parse amount - it's in dollars, convert to cents
        amount_dollars = float(parts[6])
        amount = int(round(amount_dollars * 100))

        # Compute the maximum amount we could tender
        max_tender = sum(counts[i] * coin_values[i] for i in range(6))

        # For the shopkeeper's change, greedy works for NZ coins
        def min_change_coins(change):
            """Minimum coins to make change (shopkeeper has unlimited coins)."""
            if change < 0:
                return float('inf')
            coins = 0
            for v in [200, 100, 50, 20, 10, 5]:
                coins += change // v
                change %= v
            if change != 0:
                return float('inf')
            return coins

        # DP approach: for each possible tender amount (in multiples of 5c),
        # find the minimum number of our coins to make that amount.
        # Then total = our_coins + shopkeeper_change_coins(tender - amount)

        # We use DP over the 6 coin types.
        # dp[value] = minimum number of coins to make exactly 'value' cents
        # using our available coins.

        # Maximum possible tender we'd consider:
        # The change the shopkeeper gives back costs coins too, so we wouldn't
        # want to overpay by too much. But to be safe, consider up to max_tender.
        # However max_tender can be large. Let's bound it:
        # amount < 500 (always < $5.00)
        # max_tender could be up to ~some reasonable bound
        # With at most say 100 of each coin, max_tender could be large.
        # But the problem says amount < $5.00 and coins are enough to pay.
        # Overpaying by more than 200c (one $2 coin) beyond the next round amount
        # is unlikely to help. But let's be safe and go up to max_tender,
        # capped at a reasonable limit.

        # Actually, the key insight: we never need to overpay by more than
        # the largest coin denomination minus 5c = 195c. Because any overpay
        # beyond that could be reduced. But to be safe, let's consider up to
        # amount + 500 (or max_tender, whichever is smaller).

        upper = min(max_tender, amount + 500)
        # Make sure upper is at least amount
        upper = max(upper, amount)

        # DP: bounded knapsack
        # dp[v] = min coins from our wallet to make exactly v cents
        INF = float('inf')
        dp = [INF] * (upper + 1)
        dp[0] = 0

        for i in range(6):
            cv = coin_values[i]
            cnt = counts[i]
            if cnt == 0:
                continue
            # Bounded knapsack using binary decomposition
            # Split cnt into powers of 2
            remaining = cnt
            k = 1
            while remaining > 0:
                take = min(k, remaining)
                weight = take * cv
                cost = take
                # 0-1 knapsack step: iterate backwards
                for v in range(upper, weight - 1, -1):
                    if dp[v - weight] + cost < dp[v]:
                        dp[v] = dp[v - weight] + cost
                remaining -= take
                k *= 2

        # Now find minimum total coins
        best = INF
        for tender in range(amount, upper + 1, 5):
            if dp[tender] < INF:
                change_coins = min_change_coins(tender - amount)
                total = dp[tender] + change_coins
                if total < best:
                    best = total

        results.append(best)

    for r in results:
        print(f"{r:3d}")

solve()
