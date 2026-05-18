import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(data):
        n = int(data[idx]); idx += 1
        nums = []
        for i in range(n):
            nums.append(int(data[idx])); idx += 1
        nums.sort()

        if n % 2 == 1:
            # Odd: unique median
            median = nums[n // 2]
            # Count how many input numbers equal median
            count_in_input = nums.count(median)
            # Only 1 integer value achieves minimum
            num_values = 1
            results.append(f"{median} {count_in_input} {num_values}")
        else:
            # Even: any integer in [nums[n//2 - 1], nums[n//2]] achieves minimum
            lower = nums[n // 2 - 1]
            upper = nums[n // 2]
            # The "minimum A" is the smallest such value = lower
            a_val = lower
            # Count how many input numbers equal a_val
            count_in_input = nums.count(a_val)
            # Number of distinct integer values for A
            num_values = upper - lower + 1
            results.append(f"{a_val} {count_in_input} {num_values}")

    print('\n'.join(results))

solve()
