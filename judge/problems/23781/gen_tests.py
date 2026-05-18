#!/usr/bin/env python3
"""
Generate test cases for Making Change (23781).

Coins: 5c, 10c, 20c, 50c, $1, $2
Amount is always < $5.00 and a multiple of 5c.
Total coin value >= amount.
Terminated by 0 0 0 0 0 0.
"""

import os
import subprocess
import random

SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/23781/solution.py"
OUTDIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/23781/testcases"

coin_values = [5, 10, 20, 50, 100, 200]

def total_value(counts):
    return sum(c * v for c, v in zip(counts, coin_values))

def make_case(counts, amount_cents):
    """Create a single test line. amount_cents must be multiple of 5, < 500."""
    assert amount_cents % 5 == 0
    assert 0 < amount_cents < 500
    assert total_value(counts) >= amount_cents
    amount_dollars = amount_cents / 100.0
    # Format amount: always show 2 decimal places
    return f"{counts[0]} {counts[1]} {counts[2]} {counts[3]} {counts[4]} {counts[5]}  {amount_dollars:.2f}"

def run_solution(input_text):
    result = subprocess.run(
        ["python3", SOLUTION],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout

def write_test(case_num, lines):
    """Write a test case with multiple transaction lines."""
    input_lines = lines + ["0 0 0 0 0 0"]
    input_text = "\n".join(input_lines) + "\n"

    output_text = run_solution(input_text)

    in_file = os.path.join(OUTDIR, f"{case_num:02d}.in")
    out_file = os.path.join(OUTDIR, f"{case_num:02d}.out")

    with open(in_file, "w") as f:
        f.write(input_text)
    with open(out_file, "w") as f:
        f.write(output_text)

    print(f"Test {case_num:02d}: {len(lines)} line(s)")
    for l in lines:
        print(f"  IN:  {l}")
    for l in output_text.strip().split("\n"):
        print(f"  OUT: '{l}'")


def gen_random_case(max_each=10, max_amount=495):
    """Generate a random valid case."""
    while True:
        counts = [random.randint(0, max_each) for _ in range(6)]
        tv = total_value(counts)
        if tv < 5:
            continue
        # Pick a random amount that is multiple of 5, <= tv, < 500
        max_a = min(tv, max_amount)
        if max_a < 5:
            continue
        amount = random.randint(1, max_a // 5) * 5
        return make_case(counts, amount)


# ========== TEST CASES ==========

cases = []

# Case 01: Sample test case
cases.append([
    make_case([2, 4, 2, 2, 1, 0], 95),
    make_case([2, 4, 2, 0, 1, 0], 55),
])

# Case 02: Exact payment possible (no change needed)
cases.append([
    make_case([1, 0, 0, 0, 0, 0], 5),     # Exactly 5c with one 5c coin
    make_case([0, 1, 0, 0, 0, 0], 10),    # Exactly 10c
    make_case([0, 0, 1, 0, 0, 0], 20),    # Exactly 20c
    make_case([0, 0, 0, 1, 0, 0], 50),    # Exactly 50c
    make_case([0, 0, 0, 0, 1, 0], 100),   # Exactly $1
    make_case([0, 0, 0, 0, 0, 1], 200),   # Exactly $2
])

# Case 03: Must overpay (only large coins, small amount)
cases.append([
    make_case([0, 0, 0, 0, 0, 1], 5),     # Pay $2, get $1.95 change
    make_case([0, 0, 0, 0, 1, 0], 5),     # Pay $1, get 95c change
    make_case([0, 0, 0, 1, 0, 0], 5),     # Pay 50c, get 45c change
])

# Case 04: Minimum amount (5c)
cases.append([
    make_case([1, 0, 0, 0, 0, 0], 5),
    make_case([0, 0, 0, 0, 0, 1], 5),
    make_case([1, 1, 1, 1, 1, 1], 5),
])

# Case 05: Maximum amount close to $5.00 (495c)
cases.append([
    make_case([1, 0, 0, 0, 0, 3], 495),   # 5+600=605 >= 495
    make_case([19, 0, 0, 0, 0, 2], 495),  # 95+400=495, exact
])

# Case 06: All coins are 5c (many small coins)
cases.append([
    make_case([20, 0, 0, 0, 0, 0], 55),   # 20*5=100 >= 55, must use 11 5c coins or overpay
    make_case([10, 0, 0, 0, 0, 0], 30),   # 10*5=50 >= 30
    make_case([99, 0, 0, 0, 0, 0], 495),  # 99*5=495, exact: 99 coins. Or overpay?
])

# Case 07: Overpay is better than exact
# Example: pay 55c. Have 2*20c + 10c + 5c = 55c exact (4 coins).
# Or pay 100c (1*$1 if available) get 45c change (50c-5c=no, 20c+20c+5c=3 coins) total=4
# Or pay 60c (20+20+10+10) get 5c back: 4+1=5 coins
# The problem sample shows 1.05 -> 50c change = 3 coins total
cases.append([
    make_case([2, 4, 2, 0, 1, 0], 55),    # From sample: answer 3
    make_case([0, 0, 0, 0, 2, 0], 55),    # Pay $1, get 45c (4 coins change) = 5. Pay $2, get 145c (7 coins) = 8. Best = 5
    make_case([1, 0, 0, 0, 2, 0], 55),    # Pay $1+5c=105c, get 50c back: 2+1=3
])

# Case 08: Only $2 coins
cases.append([
    make_case([0, 0, 0, 0, 0, 3], 5),     # Pay $2, change $1.95 = 200-5=195: 100+50+20+20+5=5 coins. total=6
    make_case([0, 0, 0, 0, 0, 3], 200),   # Pay $2, no change: 1 coin
    make_case([0, 0, 0, 0, 0, 3], 400),   # Pay $4: 2 coins
    make_case([0, 0, 0, 0, 0, 3], 395),   # Pay $4, change 5c: 2+1=3
])

# Case 09: Mix where greedy on your coins is suboptimal
cases.append([
    make_case([3, 3, 3, 0, 0, 0], 75),    # 75c: 20+20+20+10+5=5 coins exact. Or 50+20+5=75 but no 50c. Best exact = 5? Or overpay 80c(20*3+10*2=80) get 5c back = 5+1=6. So 5.
    make_case([0, 0, 5, 0, 0, 0], 60),    # Only 20c coins. Can't make 60 exactly. Pay 80c (4*20c), change 20c (1 coin), total=5
    make_case([1, 0, 3, 0, 0, 0], 45),    # 5+3*20=65. Pay 45: can't with 5+20+20=45, exact 3 coins.
])

# Case 10: Large number of coins
cases.append([
    make_case([50, 50, 50, 50, 50, 2], 495),
    make_case([99, 99, 99, 99, 99, 2], 490),
    make_case([1, 1, 1, 1, 1, 1], 385),   # 5+10+20+50+100+200=385, exact
])

# Case 11: Cases where change amount is tricky
cases.append([
    make_case([0, 1, 0, 0, 1, 0], 15),    # Have 10c+$1=110c. Pay 20c? no. Pay 10c, get -5 no. Pay $1, change 85c=50+20+10+5=4, total=5. Pay $1+10c=110c, change 95c=50+20+20+5=4, total=6. Best=5
    make_case([0, 0, 0, 0, 0, 2], 195),   # Pay $2, change 5c=1, total=2. Pay $4, change 205c=200+5=2, total=4. Best=2
    make_case([10, 10, 0, 0, 0, 0], 35),  # 5*10+10*10=150. Pay 35c: 5+10+10+10=4 or 5+10+20(no 20c)... best = 5c+10c+10c+10c=35c, 4 coins. Or 40c (10*4), change 5c=1, total=5. Best=4? Wait, 5+10+10+10=35, 4 coins exact.
])

# Case 12: Single coin type tests
cases.append([
    make_case([0, 10, 0, 0, 0, 0], 50),   # 5*10c = 50c, exact, 5 coins. Or overpay?
    make_case([0, 0, 0, 10, 0, 0], 150),  # 3*50c=150, exact, 3 coins
    make_case([0, 0, 0, 0, 5, 0], 300),   # 3*$1=300, exact, 3 coins
])

# Case 13: Stress test with many lines
random.seed(42)
stress_lines = []
for _ in range(15):
    stress_lines.append(gen_random_case(max_each=20))
cases.append(stress_lines)

# Case 14: Edge near $5.00
cases.append([
    make_case([0, 0, 0, 0, 0, 3], 495),   # 600c. Pay 500c? can't make 500 with 200c coins. Pay 600c, change 105c=100+5=2, total=3+2=5
    make_case([1, 0, 0, 0, 1, 2], 495),   # 5+100+400=505. Pay 500? 200+200+100=500=3 coins, change 5c=1, total=4. Pay 505? 200+200+100+5=505=4, change 10c=1, total=5. Best=4
    make_case([0, 0, 0, 0, 5, 0], 495),   # 500c. Pay 500, change 5c=1, total=5+1=6
])

# Case 15: Very constrained wallets
cases.append([
    make_case([1, 0, 0, 0, 0, 1], 5),     # Pay 5c: 1 coin, no change. Best=1
    make_case([0, 0, 0, 0, 1, 1], 100),   # Pay $1: 1 coin, no change. Best=1
    make_case([0, 0, 1, 0, 0, 1], 215),   # 20+200=220. Pay 220, change 5c=1, total=2+1=3
])

# Case 16: Random medium difficulty
random.seed(123)
med_lines = []
for _ in range(10):
    med_lines.append(gen_random_case(max_each=15))
cases.append(med_lines)

# Case 17: Exact multiples of coin values
cases.append([
    make_case([0, 0, 0, 2, 2, 2], 100),   # $1 exact: 1 coin
    make_case([0, 0, 0, 2, 2, 2], 200),   # $2 exact: 1 coin
    make_case([0, 0, 0, 2, 2, 2], 300),   # $2+$1=3: 2 coins
    make_case([0, 0, 0, 2, 2, 2], 250),   # $2+50c=250: 2 coins
    make_case([0, 0, 0, 2, 2, 2], 150),   # $1+50c=150: 2 coins
])

# Case 18: Overpay significantly better
cases.append([
    make_case([20, 0, 0, 0, 0, 1], 95),   # 20*5=100, $2=200, total avail=300
    # Exact: 19*5c=95c, 19 coins. Overpay: $2, change $1.05=100+5=2 coins, total=3. MUCH better.
    make_case([10, 0, 0, 0, 1, 0], 45),   # Exact: 9*5c=45c, 9 coins. Or $1, change 55c=50+5=2, total=3. Or 50c(pay $1-50c=no)... Best probably 3.
    make_case([0, 10, 0, 0, 0, 1], 70),   # 10c*10=100, $2=200. Pay 100c(10*10c), change 30c=20+10=2, total=12. Or pay $2, change 130c=100+20+10=3, total=4. Best=4
])

# Write all test cases
for i, lines in enumerate(cases, 1):
    write_test(i, lines)

print(f"\nGenerated {len(cases)} test cases.")
