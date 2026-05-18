import math
import os

BASE = "/Users/lambert/Documents/GPE-Helper/judge/problems/10465/testcases"

def solve(v_total, v0):
    if v_total <= v0:
        return 0

    max_n = int(v_total / v0)
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

test_cases = []

# Test 1: Sample test case
test_cases.append([
    (10, 1),
    (10, 2),
])

# Test 2: V_total = V0, no disc possible
test_cases.append([
    (5, 5),
    (1, 1),
    (600, 600),
])

# Test 3: V_total < V0, no disc possible
test_cases.append([
    (1, 2),
    (3, 5),
    (100, 600),
])

# Test 4: V_total just barely above V0, only n=1 possible
test_cases.append([
    (6, 5),
    (2, 1),
    (601, 600),
])

# Test 5: Tie cases - V = V0*(2k+1) produces ties at k and k+1
# Output should be 0
test_cases.append([
    (3, 1),   # tie at n=1,2
    (5, 1),   # tie at n=2,3
    (7, 1),   # tie at n=3,4
    (30, 10), # tie at n=1,2
    (50, 10), # tie at n=2,3
])

# Test 6: Even multiples - V = V0*2k, unique optimum at n=k
test_cases.append([
    (4, 1),   # n_opt=2
    (6, 1),   # n_opt=3
    (8, 1),   # n_opt=4
    (20, 10), # n_opt=1
    (40, 10), # n_opt=2
])

# Test 7: Large V_total, small V0
test_cases.append([
    (60000, 1),
    (60000, 600),
    (59999, 1),
])

# Test 8: Large V_total with ties
# V = V0*(2k+1) => for V0=1, V=2k+1 (odd)
test_cases.append([
    (59999, 1),   # odd, V0=1 => tie at n=29999, 30000
    (59001, 1),   # odd => tie
    (60000, 2),   # 60000/(2*2)=15000, even multiple => unique at n=15000
])

# Test 9: V0 at max (600), various V_total
test_cases.append([
    (601, 600),  # only n=1
    (1200, 600), # n_opt = 1200/1200 = 1 => unique
    (1800, 600), # 1800 = 600*3 => tie at n=1,2
    (2400, 600), # n_opt = 2400/1200 = 2 => unique
])

# Test 10: V_total = 2*V0 exactly => only n=1 valid (n=2 gives V/n=V0, not valid)
test_cases.append([
    (2, 1),
    (10, 5),
    (1200, 600),
    (20, 10),
])

# Test 11: Small values
test_cases.append([
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (8, 1),
    (9, 1),
    (10, 1),
])

# Test 12: V_total = 3*V0 => tie (V0*(2*1+1))
test_cases.append([
    (3, 1),
    (30, 10),
    (300, 100),
    (1800, 600),
])

# Test 13: Larger numbers, unique answer
test_cases.append([
    (10000, 100),
    (20000, 200),
    (30000, 300),
    (50000, 500),
])

# Test 14: Boundary - V_total=1, V0=1 (no disc)
# and V_total=60000, V0=1 (many discs possible)
test_cases.append([
    (1, 1),
    (60000, 1),
    (60000, 300),
    (59400, 300),  # 59400 = 300*(2*99) = 300*198 => n_opt=99
])

# Test 15: Various tie and non-tie patterns
test_cases.append([
    (100, 3),
    (200, 7),
    (500, 11),
    (1000, 23),
    (5000, 47),
])

# Test 16: Edge: V0=1 with even and odd V_total near boundaries
test_cases.append([
    (2, 1),   # even, n_opt=1
    (3, 1),   # odd=2*1+1, tie
    (100, 1), # even, n_opt=50
    (101, 1), # odd=2*50+1, tie
    (1000, 1),  # even, n_opt=500
    (1001, 1),  # odd, tie
])

# Test 17: Cases where max_n is 1 (barely above V0)
test_cases.append([
    (11, 10),
    (51, 50),
    (599, 300),  # 599/2 = 299.5 < 300, so only n=1
    (601, 600),
])

# Test 18: Random medium cases
test_cases.append([
    (123, 45),
    (456, 78),
    (789, 12),
    (1000, 1),
    (999, 500),
])

for idx, cases in enumerate(test_cases):
    case_num = f"{idx+1:02d}"
    in_lines = []
    out_lines = []
    for v, v0 in cases:
        in_lines.append(f"{v} {v0}")
        out_lines.append(str(solve(v, v0)))
    in_lines.append("0 0")

    in_path = os.path.join(BASE, f"{case_num}.in")
    out_path = os.path.join(BASE, f"{case_num}.out")

    with open(in_path, "w") as f:
        f.write("\n".join(in_lines) + "\n")
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")

    print(f"Test {case_num}: {len(cases)} sub-cases")
    for i, (v, v0) in enumerate(cases):
        print(f"  V={v}, V0={v0} => {out_lines[i]}")

print(f"\nTotal test files: {len(test_cases)} pairs")
