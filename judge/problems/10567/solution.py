import sys
from collections import Counter

def solve(a, b):
    ca = Counter(a)
    cb = Counter(b)
    result = []
    for ch in 'abcdefghijklmnopqrstuvwxyz':
        count = min(ca.get(ch, 0), cb.get(ch, 0))
        result.append(ch * count)
    return ''.join(result)

def main():
    lines = sys.stdin.read().strip().split('\n')
    i = 0
    while i + 1 < len(lines):
        a = lines[i]
        b = lines[i + 1]
        print(solve(a, b))
        i += 2

if __name__ == '__main__':
    main()
