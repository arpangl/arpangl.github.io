import subprocess
import os

TESTCASE_DIR = "/Users/lambert/Documents/GPE-Helper/judge/problems/22351/testcases"
SOLUTION = "/Users/lambert/Documents/GPE-Helper/judge/problems/22351/solution.py"

test_cases = [
    # 01: Sample input
    "2\n2\n",
    # 02: Single 2
    "2\n",
    # 03: Single 4
    "4\n",
    # 04: Single 6
    "6\n",
    # 05: Single 8
    "8\n",
    # 06: All four values in order
    "2\n4\n6\n8\n",
    # 07: All four values in reverse order
    "8\n6\n4\n2\n",
    # 08: Repeated 4s
    "4\n4\n4\n",
    # 09: Repeated 6s
    "6\n6\n",
    # 10: Repeated 8s
    "8\n8\n",
    # 11: Mixed with repeats
    "2\n4\n2\n4\n",
    # 12: Alternating 2 and 8
    "2\n8\n2\n8\n",
    # 13: All 2s (stress on smallest)
    "2\n2\n2\n2\n2\n",
    # 14: All 8s (stress on largest)
    "8\n8\n8\n8\n8\n",
    # 15: Mixed order
    "6\n2\n8\n4\n",
    # 16: Single 2 then single 8
    "2\n8\n",
    # 17: 4 then 6
    "4\n6\n",
    # 18: Long sequence of mixed
    "2\n4\n6\n8\n8\n6\n4\n2\n",
]

for i, inp in enumerate(test_cases, 1):
    in_file = os.path.join(TESTCASE_DIR, f"{i:02d}.in")
    out_file = os.path.join(TESTCASE_DIR, f"{i:02d}.out")

    with open(in_file, 'w') as f:
        f.write(inp)

    result = subprocess.run(
        ["python3", SOLUTION],
        input=inp,
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        print(f"ERROR on test {i:02d}: {result.stderr}")
    else:
        with open(out_file, 'w') as f:
            f.write(result.stdout)
        # Count lines for verification
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        print(f"Test {i:02d}: input lines={inp.strip().count(chr(10))+1}, output lines={len(lines)}")

print("\nDone generating all test cases.")
