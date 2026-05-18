import random
import os
import json
import subprocess

def solve(input_data):
    lines = input_data.strip().split('\n')
    elephants = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            w, s = int(parts[0]), int(parts[1])
            elephants.append((w, s))

    n = len(elephants)
    if n == 0:
        return "0\n"

    indexed = list(range(n))
    indexed.sort(key=lambda i: (elephants[i][0], -elephants[i][1]))

    dp = [1] * n
    parent = [-1] * n

    for i in range(n):
        for j in range(i):
            ii, jj = indexed[i], indexed[j]
            if elephants[jj][0] < elephants[ii][0] and elephants[jj][1] > elephants[ii][1]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

    best_len = max(dp)
    best_idx = dp.index(best_len)

    seq = []
    idx = best_idx
    while idx != -1:
        seq.append(indexed[idx] + 1)
        idx = parent[idx]
    seq.reverse()

    result = [str(best_len)]
    for s in seq:
        result.append(str(s))
    return '\n'.join(result) + '\n'

def verify_output(input_data, output_data):
    """Verify output is valid (weights strictly increasing, IQs strictly decreasing)."""
    lines_in = input_data.strip().split('\n')
    elephants = []
    for line in lines_in:
        parts = line.split()
        if len(parts) >= 2:
            elephants.append((int(parts[0]), int(parts[1])))

    lines_out = output_data.strip().split('\n')
    n = int(lines_out[0])
    if n == 0:
        return True
    indices = [int(lines_out[i+1]) for i in range(n)]

    for i in range(1, len(indices)):
        prev = elephants[indices[i-1]-1]
        curr = elephants[indices[i]-1]
        if curr[0] <= prev[0]:
            return False
        if curr[1] >= prev[1]:
            return False
    return True

def gen_case(case_id):
    random.seed(case_id * 12345 + 42)

    if case_id == 0:
        # Sample case
        return "6008 1300\n6000 2100\n500 2000\n1000 4000\n1100 3000\n6000 2000\n8000 1400\n6000 1200\n2000 1900\n"
    elif case_id == 1:
        # Single elephant
        return "5000 5000\n"
    elif case_id == 2:
        # Two elephants, valid pair
        return "1000 5000\n2000 3000\n"
    elif case_id == 3:
        # Two elephants, no valid pair (both increase)
        return "1000 3000\n2000 5000\n"
    elif case_id == 4:
        # All same weight
        lines = []
        for i in range(10):
            lines.append(f"5000 {random.randint(1000, 9000)}")
        return '\n'.join(lines) + '\n'
    elif case_id == 5:
        # All same IQ
        lines = []
        for i in range(10):
            lines.append(f"{random.randint(1000, 9000)} 5000")
        return '\n'.join(lines) + '\n'
    elif case_id == 6:
        # Perfect anti-correlation (easy long chain)
        lines = []
        for i in range(20):
            w = 100 * (i + 1)
            s = 10000 - 100 * i
            lines.append(f"{w} {s}")
        random.shuffle(lines)
        return '\n'.join(lines) + '\n'
    elif case_id == 7:
        # Medium random
        lines = []
        for _ in range(50):
            w = random.randint(1, 10000)
            s = random.randint(1, 10000)
            lines.append(f"{w} {s}")
        return '\n'.join(lines) + '\n'
    elif case_id == 8:
        # Larger random
        lines = []
        for _ in range(200):
            w = random.randint(1, 10000)
            s = random.randint(1, 10000)
            lines.append(f"{w} {s}")
        return '\n'.join(lines) + '\n'
    elif case_id == 9:
        # Many duplicates
        lines = []
        for _ in range(30):
            w = random.choice([1000, 2000, 3000, 4000, 5000])
            s = random.choice([1000, 2000, 3000, 4000, 5000])
            lines.append(f"{w} {s}")
        return '\n'.join(lines) + '\n'
    elif case_id == 10:
        # All same weight and IQ
        lines = []
        for _ in range(15):
            lines.append("5000 5000")
        return '\n'.join(lines) + '\n'
    elif case_id == 11:
        # Weights increasing, IQs also increasing (answer should be 1)
        lines = []
        for i in range(20):
            lines.append(f"{(i+1)*100} {(i+1)*100}")
        return '\n'.join(lines) + '\n'
    elif case_id == 12:
        # Large case
        lines = []
        for _ in range(500):
            w = random.randint(1, 10000)
            s = random.randint(1, 10000)
            lines.append(f"{w} {s}")
        return '\n'.join(lines) + '\n'
    elif case_id == 13:
        # Edge: boundary values
        lines = []
        lines.append("1 10000")
        lines.append("10000 1")
        lines.append("5000 5000")
        lines.append("1 1")
        lines.append("10000 10000")
        return '\n'.join(lines) + '\n'
    elif case_id == 14:
        # Near-max size
        lines = []
        for _ in range(1000):
            w = random.randint(1, 10000)
            s = random.randint(1, 10000)
            lines.append(f"{w} {s}")
        return '\n'.join(lines) + '\n'

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10658/testcases'
os.makedirs(TESTDIR, exist_ok=True)

test_info = []
for i in range(15):
    inp = gen_case(i)
    out = solve(inp)
    assert verify_output(inp, out), f"Case {i} failed verification!"

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    test_info.append(f"Case {i+1:02d}: OK")

# Write problem.json
problem = {
    "pid": "10658",
    "name": "Is Bigger Smarter?",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

for t in test_info:
    print(t)
print("All test cases generated and verified!")
