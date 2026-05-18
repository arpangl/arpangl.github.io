#!/usr/bin/env python3
"""Generate test cases for Disk Tree problem."""
import random
import string
import subprocess
import os

BASE = "/Users/lambert/Documents/GPE-Helper/judge/problems/10038"
TC_DIR = os.path.join(BASE, "testcases")

# Valid characters for directory names: uppercase letters, digits, and special chars
VALID_CHARS = string.ascii_uppercase + string.digits + "!#$%&'()-@^_`{}~"

def random_dirname(min_len=1, max_len=8):
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(VALID_CHARS) for _ in range(length))

def generate_input(paths):
    """Given a list of path strings, return input text."""
    lines = [str(len(paths))]
    for p in paths:
        lines.append(p)
    return '\n'.join(lines) + '\n'

def solve(input_text):
    """Run the solution and return output."""
    result = subprocess.run(
        ['python3', os.path.join(BASE, 'solution.py')],
        input=input_text, capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError(f"Solution failed: {result.stderr}")
    return result.stdout

def write_testcase(idx, input_text, output_text):
    """Write .in and .out files."""
    in_path = os.path.join(TC_DIR, f"{idx:02d}.in")
    out_path = os.path.join(TC_DIR, f"{idx:02d}.out")
    with open(in_path, 'w') as f:
        f.write(input_text)
    with open(out_path, 'w') as f:
        f.write(output_text)
    print(f"  Test {idx:02d}: {len(input_text.strip().split(chr(10)))-1} paths")

test_cases = []

# ========== Test 01: Sample test case ==========
test_cases.append([
    r"WINNT\SYSTEM32\CONFIG",
    "GAMES",
    r"WINNT\DRIVERS",
    "HOME",
    r"WIN\SOFT",
    r"GAMES\DRIVERS",
    r"WINNT\SYSTEM32\CERTSRV\CERTCO~1\X86",
])

# ========== Test 02: Single directory (minimal) ==========
test_cases.append(["A"])

# ========== Test 03: Single deep path ==========
test_cases.append([r"A\B\C\D\E\F\G\H"])

# ========== Test 04: Multiple top-level dirs only ==========
test_cases.append(["ZEBRA", "APPLE", "MANGO", "BANANA", "CHERRY"])

# ========== Test 05: Duplicate paths (same path given multiple times) ==========
test_cases.append([
    r"A\B\C",
    r"A\B\C",
    r"A\B",
    r"A\B",
    "A",
])

# ========== Test 06: All directories share a common root ==========
test_cases.append([
    r"ROOT\A",
    r"ROOT\B",
    r"ROOT\C",
    r"ROOT\A\X",
    r"ROOT\A\Y",
    r"ROOT\B\X",
])

# ========== Test 07: Lexicographic ordering test (tricky) ==========
test_cases.append([
    r"B\A",
    r"A\B",
    r"A\A",
    r"B\B",
    r"C",
    r"A",
    r"B",
])

# ========== Test 08: Single character directory names ==========
test_cases.append([
    r"Z\Y\X",
    r"A\B\C",
    r"M",
    r"Z\A",
    r"A\B\D",
])

# ========== Test 09: Deep nesting with single dirs ==========
# Each level has a single child - long chain
parts = []
name = ""
for i in range(10):
    name = chr(ord('A') + i)
    if parts:
        parts.append(parts[-1] + '\\' + name)
    else:
        parts.append(name)
# Only add the deepest path - all ancestors should appear
test_cases.append([parts[-1]])

# ========== Test 10: Wide tree - many siblings ==========
paths10 = []
for c1 in "ABCDE":
    for c2 in "XYZ":
        paths10.append(f"{c1}\\{c2}")
test_cases.append(paths10)

# ========== Test 11: Paths with special characters ==========
test_cases.append([
    r"HOME\$DATA",
    r"HOME\#TEMP",
    r"HOME\~BACKUP",
    r"SYS\@LOG",
    r"SYS\%CACHE",
    r"SYS\&CONF",
])

# ========== Test 12: Overlapping prefixes ==========
test_cases.append([
    r"AB\CD\EF",
    r"AB\CD",
    r"AB",
    r"ABC\DE",
    r"A\BCD",
    r"ABCD",
])

# ========== Test 13: Large random test ==========
random.seed(42)
paths13 = set()
for _ in range(200):
    depth = random.randint(1, 6)
    parts = [random_dirname(1, 8) for _ in range(depth)]
    path = '\\'.join(parts)
    if len(path) <= 80:
        paths13.add(path)
test_cases.append(list(paths13))

# ========== Test 14: Maximum depth with short names ==========
# Try to get max depth within 80 char limit: "A\B\C\..." = 2 chars per level except first
# 80 chars -> (80+1)/2 = ~40 levels
parts14 = []
for i in range(40):
    parts14.append(chr(ord('A') + (i % 26)))
deep_path = '\\'.join(parts14)
# Also add some branches
test_cases.append([
    deep_path,
    '\\'.join(parts14[:20]) + '\\Z',
    '\\'.join(parts14[:10]) + '\\Z',
    '\\'.join(parts14[:5]) + '\\Z',
])

# ========== Test 15: Stress test - many paths ==========
random.seed(123)
paths15 = set()
roots = [random_dirname(2, 5) for _ in range(10)]
for _ in range(500):
    root = random.choice(roots)
    depth = random.randint(1, 5)
    parts = [root] + [random_dirname(1, 6) for _ in range(depth)]
    path = '\\'.join(parts)
    if len(path) <= 80:
        paths15.add(path)
# Cap at 500
paths15_list = list(paths15)[:500]
test_cases.append(paths15_list)

# ========== Test 16: N=1, single long path (near 80 chars) ==========
# Build a path close to 80 characters
p16 = "ABCDEFGH"  # 8 chars
while len(p16) < 75:
    p16 += '\\' + random_dirname(1, min(8, 79 - len(p16)))
test_cases.append([p16])

# ========== Test 17: Directories that are numeric ==========
test_cases.append([
    r"2026\03\28",
    r"2026\03\27",
    r"2025\12\31",
    r"2025\01\01",
    r"2026\03\28\LOG",
    r"2025\12\31\BACKUP",
])

# ========== Test 18: Lexicographic order with special chars and digits ==========
# ASCII order: ! # $ % & ' ( ) - 0-9 @ A-Z ^ _ ` { | } ~
test_cases.append([
    "!DIR",
    "#DIR",
    "$DIR",
    "0DIR",
    "9DIR",
    "@DIR",
    "ADIR",
    "ZDIR",
    "^DIR",
    "_DIR",
    "`DIR",
    r"{DIR",
    "}DIR",
    "~DIR",
])

# ========== Test 19: Many duplicates, only a few unique paths ==========
base_paths = [
    r"USR\LOCAL\BIN",
    r"USR\LOCAL\LIB",
    r"USR\SHARE",
    r"ETC\CONF",
    r"VAR\LOG",
]
paths19 = []
for _ in range(100):
    paths19.append(random.choice(base_paths))
test_cases.append(paths19)

# ========== Test 20: Branching at every level ==========
test_cases.append([
    r"A\B\C",
    r"A\B\D",
    r"A\E\F",
    r"A\E\G",
    r"H\I\J",
    r"H\I\K",
    r"H\L\M",
    r"H\L\N",
])

# ========== Generate all test cases ==========
print("Generating test cases...")
for idx, paths in enumerate(test_cases, start=1):
    input_text = generate_input(paths)
    output_text = solve(input_text)
    write_testcase(idx, input_text, output_text)

print(f"\nDone! Generated {len(test_cases)} test cases.")
