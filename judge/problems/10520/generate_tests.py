import random
import os
from collections import Counter

def solve(input_data):
    lines = input_data.strip().split('\n')
    idx = 0
    results = []
    while idx < len(lines):
        n = int(lines[idx].strip())
        idx += 1
        if n == 0:
            break
        combos = Counter()
        for i in range(n):
            courses = tuple(sorted(lines[idx].strip().split()))
            combos[courses] += 1
            idx += 1
        max_pop = max(combos.values())
        total = sum(v for v in combos.values() if v == max_pop)
        results.append(str(total))
    return '\n'.join(results)

def random_combo():
    """Generate a random combination of 5 distinct courses (100-499)."""
    return sorted(random.sample(range(100, 500), 5))

def combo_to_str(combo):
    return ' '.join(str(c) for c in combo)

def generate_test_cases():
    base_dir = '/Users/lambert/Documents/GPE-Helper/judge/problems/10520/testcases'
    test_cases = []

    # ---- Test 1: Sample input ----
    tc1 = """3
100 101 102 103 488
100 200 300 101 102
103 102 101 488 100
3
200 202 204 206 208
123 234 345 456 321
100 200 300 400 444
0"""
    test_cases.append(tc1)

    # ---- Test 2: n=1, single frosh ----
    tc2 = """1
100 200 300 400 499
0"""
    test_cases.append(tc2)

    # ---- Test 3: n=2, both same combo (different order) ----
    tc3 = """2
300 200 100 400 499
100 200 300 400 499
0"""
    test_cases.append(tc3)

    # ---- Test 4: n=2, all different combos (tie => all win) ----
    tc4 = """2
100 101 102 103 104
200 201 202 203 204
0"""
    test_cases.append(tc4)

    # ---- Test 5: All frosh pick the same combo ----
    tc5_lines = ["5"]
    for _ in range(5):
        # same combo in different orders
        combo = [100, 200, 300, 400, 499]
        random.shuffle(combo)
        tc5_lines.append(' '.join(str(c) for c in combo))
    tc5_lines.append("0")
    test_cases.append('\n'.join(tc5_lines))

    # ---- Test 6: Multiple combos tied for most popular ----
    tc6 = """6
100 101 102 103 104
100 101 102 103 104
200 201 202 203 204
200 201 202 203 204
300 301 302 303 304
300 301 302 303 304
0"""
    test_cases.append(tc6)

    # ---- Test 7: One combo clearly dominates ----
    tc7_lines = ["10"]
    for _ in range(7):
        tc7_lines.append("100 200 300 400 499")
    for i in range(3):
        tc7_lines.append(combo_to_str([110+i*10, 210+i*10, 310+i*10, 410+i*10, 490+i]))
    tc7_lines.append("0")
    test_cases.append('\n'.join(tc7_lines))

    # ---- Test 8: Two combos tied, one less popular ----
    tc8 = """7
100 101 102 103 104
100 101 102 103 104
100 101 102 103 104
200 201 202 203 204
200 201 202 203 204
200 201 202 203 204
300 301 302 303 304
0"""
    test_cases.append(tc8)

    # ---- Test 9: Large test, n=10000, all unique combos (everyone wins) ----
    random.seed(42)
    tc9_lines = ["10000"]
    used = set()
    while len(used) < 10000:
        combo = tuple(sorted(random.sample(range(100, 500), 5)))
        if combo not in used:
            used.add(combo)
            tc9_lines.append(combo_to_str(combo))
    tc9_lines.append("0")
    test_cases.append('\n'.join(tc9_lines))

    # ---- Test 10: Large test, n=10000, one dominant combo ----
    random.seed(43)
    tc10_lines = ["10000"]
    dominant = [100, 200, 300, 400, 499]
    for i in range(5001):
        shuffled = dominant[:]
        random.shuffle(shuffled)
        tc10_lines.append(' '.join(str(c) for c in shuffled))
    used = set()
    used.add(tuple(sorted(dominant)))
    remaining = 10000 - 5001
    while remaining > 0:
        combo = tuple(sorted(random.sample(range(100, 500), 5)))
        if combo not in used:
            used.add(combo)
            tc10_lines.append(combo_to_str(combo))
            remaining -= 1
    tc10_lines.append("0")
    test_cases.append('\n'.join(tc10_lines))

    # ---- Test 11: All frosh unique except a pair at the end ----
    random.seed(44)
    tc11_lines = ["6"]
    used = set()
    for _ in range(4):
        while True:
            combo = tuple(sorted(random.sample(range(100, 500), 5)))
            if combo not in used:
                used.add(combo)
                tc11_lines.append(combo_to_str(combo))
                break
    # add a duplicate pair
    pair_combo = [150, 250, 350, 450, 498]
    tc11_lines.append(combo_to_str(pair_combo))
    shuffled = pair_combo[:]
    random.shuffle(shuffled)
    tc11_lines.append(' '.join(str(c) for c in shuffled))
    tc11_lines.append("0")
    test_cases.append('\n'.join(tc11_lines))

    # ---- Test 12: Courses in reverse order (test sorting) ----
    tc12 = """4
499 400 300 200 100
100 200 300 400 499
200 300 400 499 100
499 100 400 200 300
0"""
    test_cases.append(tc12)

    # ---- Test 13: Multiple test cases in one input, mixed sizes ----
    random.seed(45)
    tc13_parts = []
    for size in [1, 2, 3, 5, 10]:
        tc13_parts.append(str(size))
        for _ in range(size):
            tc13_parts.append(combo_to_str(random.sample(range(100, 500), 5)))
    tc13_parts.append("0")
    test_cases.append('\n'.join(tc13_parts))

    # ---- Test 14: Edge case - minimum courses (100-104) ----
    tc14 = """4
100 101 102 103 104
104 103 102 101 100
100 101 102 103 105
100 101 102 103 105
0"""
    test_cases.append(tc14)

    # ---- Test 15: Large with many ties (each combo appears exactly 2 times) ----
    random.seed(46)
    n = 100
    tc15_lines = [str(n)]
    combos = []
    for _ in range(n // 2):
        combo = sorted(random.sample(range(100, 500), 5))
        # add twice, second time in shuffled order
        combos.append(combo_to_str(combo))
        shuffled = combo[:]
        random.shuffle(shuffled)
        combos.append(' '.join(str(c) for c in shuffled))
    random.shuffle(combos)
    tc15_lines.extend(combos)
    tc15_lines.append("0")
    test_cases.append('\n'.join(tc15_lines))

    # ---- Test 16: Three-way tie for top ----
    tc16 = """9
100 101 102 103 104
100 101 102 103 104
100 101 102 103 104
200 201 202 203 204
200 201 202 203 204
200 201 202 203 204
300 301 302 303 304
300 301 302 303 304
300 301 302 303 304
0"""
    test_cases.append(tc16)

    # ---- Test 17: Large random with multiple test cases ----
    random.seed(47)
    tc17_parts = []
    for _ in range(3):
        n = random.randint(500, 2000)
        tc17_parts.append(str(n))
        # create a pool of combos
        pool_size = random.randint(10, 50)
        pool = []
        for _ in range(pool_size):
            pool.append(sorted(random.sample(range(100, 500), 5)))
        for _ in range(n):
            combo = random.choice(pool)
            shuffled = combo[:]
            random.shuffle(shuffled)
            tc17_parts.append(' '.join(str(c) for c in shuffled))
    tc17_parts.append("0")
    test_cases.append('\n'.join(tc17_parts))

    # ---- Test 18: n=10000, two combos tied at top ----
    random.seed(48)
    tc18_lines = ["10000"]
    combo_a = [100, 200, 300, 400, 499]
    combo_b = [110, 210, 310, 410, 498]
    # 2500 of each
    entries = []
    for _ in range(2500):
        s = combo_a[:]
        random.shuffle(s)
        entries.append(' '.join(str(c) for c in s))
    for _ in range(2500):
        s = combo_b[:]
        random.shuffle(s)
        entries.append(' '.join(str(c) for c in s))
    # remaining 5000 are all unique
    used = set()
    used.add(tuple(sorted(combo_a)))
    used.add(tuple(sorted(combo_b)))
    while len(used) - 2 < 5000:
        combo = tuple(sorted(random.sample(range(100, 500), 5)))
        if combo not in used:
            used.add(combo)
            entries.append(combo_to_str(combo))
    random.shuffle(entries)
    tc18_lines.extend(entries)
    tc18_lines.append("0")
    test_cases.append('\n'.join(tc18_lines))

    # Now write all test cases and verify
    for i, tc_input in enumerate(test_cases, 1):
        tc_output = solve(tc_input)
        fname_in = os.path.join(base_dir, f'{i:02d}.in')
        fname_out = os.path.join(base_dir, f'{i:02d}.out')
        with open(fname_in, 'w') as f:
            f.write(tc_input + '\n')
        with open(fname_out, 'w') as f:
            f.write(tc_output + '\n')
        # Verify by re-solving
        with open(fname_in, 'r') as f:
            verify_input = f.read()
        verify_output = solve(verify_input)
        assert verify_output == tc_output, f"Test case {i} verification failed!"
        # Print summary
        lines = tc_input.strip().split('\n')
        print(f"Test {i:02d}: input lines={len(lines)}, output={tc_output}")

    print(f"\nGenerated {len(test_cases)} test cases successfully.")

if __name__ == '__main__':
    generate_test_cases()
