"""
Solver for 11041 - Children's Game
Arrange N positive integers to form the largest possible number.
Custom comparator: for two strings a, b, compare a+b vs b+a.
"""
import sys
from functools import cmp_to_key

def compare(a, b):
    ab = a + b
    ba = b + a
    if ab > ba:
        return -1
    elif ab < ba:
        return 1
    else:
        return 0

def solve(numbers):
    nums = sorted(numbers, key=cmp_to_key(compare))
    return ''.join(nums)

def main():
    import io
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while idx < len(input_data):
        n = int(input_data[idx]); idx += 1
        if n == 0:
            break
        nums = []
        for i in range(n):
            nums.append(input_data[idx]); idx += 1
        results.append(solve(nums))
    print('\n'.join(results))

if __name__ == '__main__':
    main()
