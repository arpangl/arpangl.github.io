import sys

def solve(input_data):
    lines = input_data.strip().split('\n')
    idx = 0
    case_num = 0
    results = []

    while idx < len(lines):
        # Skip blank lines
        while idx < len(lines) and lines[idx].strip() == '':
            idx += 1
        if idx >= len(lines):
            break

        n = int(lines[idx].strip())
        idx += 1
        elems = list(map(int, lines[idx].strip().split()))
        idx += 1

        # Skip blank line after test case
        while idx < len(lines) and lines[idx].strip() == '':
            idx += 1

        case_num += 1

        max_prod = 0  # If no positive product, answer is 0
        # Check all contiguous subsequences
        for i in range(n):
            prod = 1
            for j in range(i, n):
                prod *= elems[j]
                if prod > max_prod:
                    max_prod = prod

        results.append(f"Case #{case_num}: The maximum product is {max_prod}.")
        results.append("")  # blank line after each case

    return '\n'.join(results)


if __name__ == '__main__':
    input_data = sys.stdin.read()
    print(solve(input_data), end='')
