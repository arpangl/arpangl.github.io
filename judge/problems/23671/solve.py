import sys
import re

def solve(expr):
    """
    Given an expression like "1+2*3*4+5" with no parentheses,
    find the maximum and minimum values by choosing how to parenthesize.

    Key insight:
    - To MAXIMIZE: do all additions first, then multiplications.
      e.g., 1+2*3*4+5 -> (1+2)*(3)*(4+5) = 3*3*9 = 81
      Split by '*', sum each group, then multiply all sums.
    - To MINIMIZE: do all multiplications first, then additions.
      e.g., 1+2*3*4+5 -> 1+(2*3*4)+5 = 1+24+5 = 30
      Split by '+', multiply each group, then sum all products.
    """
    # Parse the expression into numbers and operators
    # For maximum: split by '*', evaluate '+' within each group, then multiply
    # For minimum: split by '+', evaluate '*' within each group, then add

    # Maximum: additions first, then multiplications
    # Split by '*' to get groups connected by '+'
    mul_groups = expr.split('*')
    max_val = 1
    for group in mul_groups:
        nums = list(map(int, group.split('+')))
        max_val *= sum(nums)

    # Minimum: multiplications first, then additions
    # Split by '+' to get groups connected by '*'
    add_groups = expr.split('+')
    min_val = 0
    for group in add_groups:
        nums = list(map(int, group.split('*')))
        product = 1
        for n in nums:
            product *= n
        min_val += product

    return max_val, min_val

def main():
    input_data = sys.stdin.read().strip().split('\n')
    n = int(input_data[0])
    for i in range(1, n + 1):
        expr = input_data[i].strip()
        mx, mn = solve(expr)
        print(f"The maximum and minimum are {mx} and {mn}.")

if __name__ == '__main__':
    main()
