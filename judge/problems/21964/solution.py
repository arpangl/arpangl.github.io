import sys

def solve(n, m, vessels):
    """
    Binary search on the answer: the minimal possible maximum container capacity.
    For a given capacity 'cap', check if we can distribute all vessels into <= m containers
    such that each container's total <= cap.
    """
    if m >= n:
        # Each vessel gets its own container (or more), answer is max vessel
        return max(vessels)

    lo = max(vessels)
    hi = sum(vessels)

    while lo < hi:
        mid = (lo + hi) // 2
        # Check if we can fit all vessels into m containers with max capacity = mid
        containers_needed = 1
        current_sum = 0
        for v in vessels:
            if current_sum + v > mid:
                containers_needed += 1
                current_sum = v
            else:
                current_sum += v

        if containers_needed <= m:
            hi = mid
        else:
            lo = mid + 1

    return lo

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(input_data):
        n = int(input_data[idx]); idx += 1
        m = int(input_data[idx]); idx += 1
        vessels = []
        for i in range(n):
            vessels.append(int(input_data[idx])); idx += 1
        results.append(str(solve(n, m, vessels)))
    print('\n'.join(results))

if __name__ == '__main__':
    main()
