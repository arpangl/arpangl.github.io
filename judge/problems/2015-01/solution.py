import sys

def solve(input_data):
    """Solve the Missing Numbers problem."""
    lines = input_data.strip().split('\n')
    first = lines[0].split()
    M = int(first[0])
    N = int(first[1])

    results = []
    prev_list = list(map(int, lines[1].split()))

    for i in range(2, M + 1):
        curr_list = list(map(int, lines[i].split()))
        # The missing number is the one in prev_list but not in curr_list
        # Using sum difference is the most efficient approach
        prev_sum = sum(prev_list)
        curr_sum = sum(curr_list)
        missing = prev_sum - curr_sum
        results.append(str(missing))
        prev_list = curr_list

    return '\n'.join(results) + '\n' if results else ''


if __name__ == '__main__':
    input_data = sys.stdin.read()
    print(solve(input_data), end='')
