#!/usr/bin/env python3
"""
Generate test cases for problem 10437: Zeros and Ones

The problem:
- Given a binary string (up to 1000000 chars)
- Answer queries: are all chars between positions min(i,j) and max(i,j) the same?
- Multiple test cases per input, terminated by empty line or EOF.

Edge cases to cover:
1. Single character string, query i==j (always Yes)
2. All zeros string
3. All ones string
4. Alternating 0101...
5. i > j (swap needed)
6. i == j (single char, always Yes)
7. Large string (1000000 chars)
8. Many queries
9. Boundary positions (0 and len-1)
10. String of length 1
11. Multiple test cases in one input
12. Runs of same chars then switch
13. Query spanning entire string (all same)
14. Query spanning entire string (mixed)
15. Very short strings with edge queries
"""

import random
import os

# Reuse the solve function
def solve(input_data):
    lines = input_data.split('\n')
    idx = 0
    case_num = 0
    results = []

    while idx < len(lines):
        if idx >= len(lines):
            break
        s = lines[idx]
        idx += 1

        if s == '' or s.strip() == '':
            break

        case_num += 1
        results.append(f"Case {case_num}:")

        n = len(s)
        prefix = [0] * (n + 1)
        for k in range(n):
            prefix[k + 1] = prefix[k] + (1 if s[k] == '1' else 0)

        if idx >= len(lines):
            break
        q = int(lines[idx])
        idx += 1

        for _ in range(q):
            if idx >= len(lines):
                break
            parts = lines[idx].split()
            idx += 1
            i, j = int(parts[0]), int(parts[1])
            lo, hi = min(i, j), max(i, j)
            ones = prefix[hi + 1] - prefix[lo]
            length = hi - lo + 1
            if ones == 0 or ones == length:
                results.append("Yes")
            else:
                results.append("No")

    return '\n'.join(results)


def gen_queries(slen, num_queries, special=None):
    """Generate queries for a string of length slen."""
    queries = []
    if special:
        queries.extend(special)
    while len(queries) < num_queries:
        i = random.randint(0, slen - 1)
        j = random.randint(0, slen - 1)
        queries.append((i, j))
    return queries[:num_queries]


def make_test_case_input(cases):
    """Build input string from list of (string, queries) tuples."""
    lines = []
    for s, qs in cases:
        lines.append(s)
        lines.append(str(len(qs)))
        for i, j in qs:
            lines.append(f"{i} {j}")
    lines.append("")  # empty line terminator
    return '\n'.join(lines)


def write_test(test_id, input_str, outdir):
    output_str = solve(input_str)
    in_path = os.path.join(outdir, f"{test_id:02d}.in")
    out_path = os.path.join(outdir, f"{test_id:02d}.out")
    with open(in_path, 'w') as f:
        f.write(input_str + '\n')
    with open(out_path, 'w') as f:
        f.write(output_str + '\n')
    return in_path, out_path


def main():
    random.seed(42)
    outdir = '/Users/lambert/Documents/GPE-Helper/judge/problems/10437/testcases'
    os.makedirs(outdir, exist_ok=True)

    test_id = 0

    # --- Test 1: Sample test case ---
    test_id += 1
    inp = "0000011111\n3\n0 5\n4 2\n5 9\n01010101010101010101010101111111111111111111111111111111111110000000000000000\n5\n4 4\n25 60\n1 3\n62 76\n24 62\n1\n1\n0 0\n"
    write_test(test_id, inp, outdir)

    # --- Test 2: Single character '0', one query i==j ---
    test_id += 1
    cases = [("0", [(0, 0)])]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 3: Single character '1', one query i==j ---
    test_id += 1
    cases = [("1", [(0, 0)])]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 4: All zeros string ---
    test_id += 1
    s = "0" * 100
    qs = [(0, 99), (50, 50), (0, 0), (99, 99), (30, 70), (99, 0)]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 5: All ones string ---
    test_id += 1
    s = "1" * 100
    qs = [(0, 99), (50, 50), (0, 0), (99, 99), (30, 70), (99, 0)]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 6: Alternating 0101... ---
    test_id += 1
    s = "01" * 50  # length 100
    qs = [(0, 0), (1, 1), (0, 1), (0, 99), (50, 51), (49, 50), (2, 2)]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 7: i > j (reversed indices) ---
    test_id += 1
    s = "0001110001"
    qs = [(9, 0), (5, 3), (3, 5), (7, 9), (0, 2), (2, 0), (4, 4)]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 8: Boundary positions ---
    test_id += 1
    s = "0" * 50 + "1" * 50
    qs = [(0, 49), (50, 99), (49, 50), (0, 99), (0, 0), (99, 99), (48, 51)]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 9: String of length 2 ---
    test_id += 1
    cases = [
        ("00", [(0, 0), (1, 1), (0, 1), (1, 0)]),
        ("01", [(0, 0), (1, 1), (0, 1), (1, 0)]),
        ("10", [(0, 0), (1, 1), (0, 1), (1, 0)]),
        ("11", [(0, 0), (1, 1), (0, 1), (1, 0)]),
    ]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 10: Multiple short cases ---
    test_id += 1
    cases = [
        ("000111", [(0, 2), (3, 5), (2, 3), (0, 5)]),
        ("111000", [(0, 2), (3, 5), (2, 3), (0, 5)]),
        ("010101", [(0, 0), (1, 1), (0, 5), (2, 4)]),
    ]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 11: Runs of varying lengths ---
    test_id += 1
    s = "0" * 10 + "1" * 20 + "0" * 15 + "1" * 5 + "0" * 30 + "1" * 20
    qs = [
        (0, 9), (10, 29), (30, 44), (45, 49), (50, 79), (80, 99),
        (0, 99), (9, 10), (29, 30), (44, 45), (49, 50), (79, 80),
        (5, 15), (25, 35),
    ]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 12: Medium random string, many queries ---
    test_id += 1
    s = ''.join(random.choice('01') for _ in range(500))
    qs = gen_queries(500, 50, [(0, 499), (0, 0), (499, 499), (499, 0)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 13: Large string (100000 chars), stress test ---
    test_id += 1
    s = ''.join(random.choice('01') for _ in range(100000))
    qs = gen_queries(100000, 100, [(0, 99999), (0, 0), (99999, 99999)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 14: Large all-zero string (100000 chars) ---
    test_id += 1
    s = "0" * 100000
    qs = gen_queries(100000, 50, [(0, 99999), (50000, 50000), (99999, 0)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 15: Large all-one string (100000 chars) ---
    test_id += 1
    s = "1" * 100000
    qs = gen_queries(100000, 50, [(0, 99999), (50000, 50000), (99999, 0)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 16: Large alternating string ---
    test_id += 1
    s = ("01" * 50000)  # 100000 chars
    qs = gen_queries(100000, 50, [(0, 99999), (0, 0), (1, 1), (0, 1), (99998, 99999)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 17: Large string with long runs ---
    test_id += 1
    parts = []
    curr = '0'
    total = 0
    while total < 100000:
        run_len = random.randint(100, 5000)
        run_len = min(run_len, 100000 - total)
        parts.append(curr * run_len)
        total += run_len
        curr = '1' if curr == '0' else '0'
    s = ''.join(parts)
    qs = gen_queries(len(s), 80, [(0, len(s)-1), (0, 0), (len(s)-1, len(s)-1)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 18: Maximum string length 1000000, few queries ---
    test_id += 1
    # Build with large runs to keep it fast
    parts = []
    total = 0
    curr = '0'
    while total < 1000000:
        run_len = random.randint(1000, 50000)
        run_len = min(run_len, 1000000 - total)
        parts.append(curr * run_len)
        total += run_len
        curr = '1' if curr == '0' else '0'
    s = ''.join(parts)
    qs = gen_queries(len(s), 20, [(0, len(s)-1), (0, 0), (len(s)-1, len(s)-1), (len(s)//2, len(s)//2)])
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    # --- Test 19: Multiple medium cases in one input ---
    test_id += 1
    all_cases = []
    for _ in range(5):
        slen = random.randint(10, 200)
        s = ''.join(random.choice('01') for _ in range(slen))
        nq = random.randint(5, 15)
        qs = gen_queries(slen, nq)
        all_cases.append((s, qs))
    inp = make_test_case_input(all_cases)
    write_test(test_id, inp, outdir)

    # --- Test 20: Edge - query where i==j at every position of short string ---
    test_id += 1
    s = "01001101"
    qs = [(k, k) for k in range(len(s))]
    # Also add some range queries
    qs += [(0, 7), (0, 1), (2, 3), (3, 5), (6, 7)]
    cases = [(s, qs)]
    inp = make_test_case_input(cases)
    write_test(test_id, inp, outdir)

    print(f"Generated {test_id} test cases in {outdir}")


if __name__ == '__main__':
    main()
