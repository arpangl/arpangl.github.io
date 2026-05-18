import random
import os

# We'll reuse the solve function
def solve(input_lines):
    idx = 0
    T = int(input_lines[idx]); idx += 1
    results = []
    for _ in range(T):
        n = int(input_lines[idx]); idx += 1
        instructions = []
        pos = 0
        for i in range(n):
            line = input_lines[idx].strip(); idx += 1
            if line == "LEFT":
                delta = -1
            elif line == "RIGHT":
                delta = 1
            else:
                ref = int(line.split()[-1])
                delta = instructions[ref - 1]
            instructions.append(delta)
            pos += delta
        results.append(str(pos))
    return "\n".join(results)


def gen_random_case(n):
    """Generate a single test case with n instructions."""
    lines = []
    for i in range(n):
        r = random.random()
        if i == 0:
            # First instruction must be LEFT or RIGHT
            if random.random() < 0.5:
                lines.append("LEFT")
            else:
                lines.append("RIGHT")
        else:
            if r < 0.33:
                lines.append("LEFT")
            elif r < 0.66:
                lines.append("RIGHT")
            else:
                ref = random.randint(1, i)  # 1-indexed, referencing previous instructions
                lines.append(f"SAME AS {ref}")
    return lines


test_cases = []

# TC 1: Sample test case
test_cases.append({
    "desc": "sample",
    "input": "2\n3\nLEFT\nRIGHT\nSAME AS 2\n5\nLEFT\nSAME AS 1\nSAME AS 2\nSAME AS 1\nSAME AS 4"
})

# TC 2: Single test case, single instruction LEFT
test_cases.append({
    "desc": "single LEFT",
    "input": "1\n1\nLEFT"
})

# TC 3: Single test case, single instruction RIGHT
test_cases.append({
    "desc": "single RIGHT",
    "input": "1\n1\nRIGHT"
})

# TC 4: All LEFT instructions
test_cases.append({
    "desc": "all LEFT n=100",
    "input": "1\n100\n" + "\n".join(["LEFT"] * 100)
})

# TC 5: All RIGHT instructions
test_cases.append({
    "desc": "all RIGHT n=100",
    "input": "1\n100\n" + "\n".join(["RIGHT"] * 100)
})

# TC 6: Alternating LEFT RIGHT -> should cancel out (even count = 0)
n = 100
instrs = []
for i in range(n):
    instrs.append("LEFT" if i % 2 == 0 else "RIGHT")
test_cases.append({
    "desc": "alternating LEFT/RIGHT n=100",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 7: All SAME AS 1, where instruction 1 is LEFT
n = 100
instrs = ["LEFT"] + [f"SAME AS 1" for _ in range(n - 1)]
test_cases.append({
    "desc": "all SAME AS 1 (LEFT) n=100",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 8: All SAME AS 1, where instruction 1 is RIGHT
n = 100
instrs = ["RIGHT"] + [f"SAME AS 1" for _ in range(n - 1)]
test_cases.append({
    "desc": "all SAME AS 1 (RIGHT) n=100",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 9: Chain of SAME AS: each instruction references the previous one, first is LEFT
n = 100
instrs = ["LEFT"] + [f"SAME AS {i}" for i in range(1, n)]
test_cases.append({
    "desc": "chain SAME AS previous (LEFT) n=100",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 10: Chain of SAME AS: each references previous, first is RIGHT
n = 100
instrs = ["RIGHT"] + [f"SAME AS {i}" for i in range(1, n)]
test_cases.append({
    "desc": "chain SAME AS previous (RIGHT) n=100",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 11: Mixed - first half LEFT, second half SAME AS random from first half
n = 50
instrs = ["LEFT"] * 25
for i in range(25):
    ref = random.randint(1, 25)
    instrs.append(f"SAME AS {ref}")
test_cases.append({
    "desc": "half LEFT, half SAME AS random n=50",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 12: T=100, each with n=1 (max number of test cases, minimal instructions)
lines = ["100"]
for _ in range(100):
    lines.append("1")
    if random.random() < 0.5:
        lines.append("LEFT")
    else:
        lines.append("RIGHT")
test_cases.append({
    "desc": "T=100, n=1 each",
    "input": "\n".join(lines)
})

# TC 13: T=1, n=100, random mix of all three instruction types
random.seed(42)
instrs = gen_random_case(100)
test_cases.append({
    "desc": "T=1 n=100 random mix seed=42",
    "input": f"1\n100\n" + "\n".join(instrs)
})

# TC 14: T=10, various n, random instructions
random.seed(123)
lines = ["10"]
for _ in range(10):
    n = random.randint(1, 100)
    lines.append(str(n))
    instrs = gen_random_case(n)
    lines.extend(instrs)
test_cases.append({
    "desc": "T=10 various n random seed=123",
    "input": "\n".join(lines)
})

# TC 15: SAME AS with deep chaining: 1->LEFT, 2->SAME AS 1, 3->SAME AS 2, etc. All resolve to LEFT
n = 50
instrs = ["LEFT"]
for i in range(2, n + 1):
    instrs.append(f"SAME AS {i - 1}")
test_cases.append({
    "desc": "deep chain n=50",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 16: Instruction that cancels: LEFT RIGHT LEFT RIGHT ... with SAME AS pointing to both
n = 20
instrs = ["LEFT", "RIGHT"]
for i in range(2, n):
    ref = random.randint(1, i)
    instrs.append(f"SAME AS {ref}")
test_cases.append({
    "desc": "cancel with SAME AS n=20",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 17: Multiple test cases with position = 0
test_cases.append({
    "desc": "result zero",
    "input": "3\n2\nLEFT\nRIGHT\n4\nLEFT\nRIGHT\nSAME AS 1\nSAME AS 2\n2\nRIGHT\nLEFT"
})

# TC 18: Large: T=50, n up to 100
random.seed(999)
T = 50
lines = [str(T)]
for _ in range(T):
    n = random.randint(1, 100)
    lines.append(str(n))
    instrs = gen_random_case(n)
    lines.extend(instrs)
test_cases.append({
    "desc": "T=50 large random seed=999",
    "input": "\n".join(lines)
})

# TC 19: SAME AS always referencing the last instruction
n = 100
instrs = ["RIGHT"]
for i in range(1, n):
    instrs.append(f"SAME AS {i}")
test_cases.append({
    "desc": "SAME AS always last n=100",
    "input": f"1\n{n}\n" + "\n".join(instrs)
})

# TC 20: Edge: T=1, n=1, just RIGHT
test_cases.append({
    "desc": "minimal RIGHT",
    "input": "1\n1\nRIGHT"
})

# Now solve each and write files
outdir = "/Users/lambert/Documents/GPE-Helper/judge/problems/24911/testcases"

for i, tc in enumerate(test_cases):
    case_num = f"{i + 1:02d}"
    inp = tc["input"]
    out = solve(inp.strip().split("\n"))

    in_path = os.path.join(outdir, f"{case_num}.in")
    out_path = os.path.join(outdir, f"{case_num}.out")

    with open(in_path, "w") as f:
        f.write(inp.strip() + "\n")
    with open(out_path, "w") as f:
        f.write(out.strip() + "\n")

    print(f"TC {case_num}: {tc['desc']}")
    print(f"  Output: {out}")
    print()

print(f"Total test cases: {len(test_cases)}")
