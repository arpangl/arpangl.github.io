import sys
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

if __name__ == '__main__':
    input_data = sys.stdin.read()
    print(solve(input_data))
