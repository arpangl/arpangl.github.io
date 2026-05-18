import sys

def solve(input_data):
    lines = input_data.split('\n')
    idx = 0
    case_num = 0
    results = []

    while idx < len(lines):
        # Read the binary string
        # Skip completely empty lines that are terminators
        if idx >= len(lines):
            break
        s = lines[idx]
        idx += 1

        # Empty string or end of input => stop
        if s == '' or s.strip() == '':
            break

        case_num += 1
        results.append(f"Case {case_num}:")

        # Build prefix sums for count of '1's
        n = len(s)
        prefix = [0] * (n + 1)
        for k in range(n):
            prefix[k + 1] = prefix[k] + (1 if s[k] == '1' else 0)

        # Read number of queries
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
            # Count of 1's in range [lo, hi]
            ones = prefix[hi + 1] - prefix[lo]
            length = hi - lo + 1
            # All same if all 0's (ones==0) or all 1's (ones==length)
            if ones == 0 or ones == length:
                results.append("Yes")
            else:
                results.append("No")

    return '\n'.join(results)


if __name__ == '__main__':
    input_data = sys.stdin.read()
    print(solve(input_data))
