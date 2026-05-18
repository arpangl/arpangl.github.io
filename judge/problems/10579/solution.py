import sys

def solve(input_data):
    lines = input_data.strip().split('\n')
    idx = 0
    m, n = map(int, lines[idx].split())
    idx += 1

    dictionary = {}
    for i in range(m):
        parts = lines[idx].split()
        word = parts[0]
        value = int(parts[1])
        dictionary[word] = value
        idx += 1

    results = []
    for _ in range(n):
        total = 0
        while idx < len(lines):
            line = lines[idx]
            idx += 1
            if line.strip() == '.':
                break
            words = line.split()
            for w in words:
                if w in dictionary:
                    total += dictionary[w]
        results.append(str(total))

    return '\n'.join(results)


if __name__ == '__main__':
    input_data = sys.stdin.read()
    print(solve(input_data))
