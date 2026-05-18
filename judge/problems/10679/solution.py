import sys
import math

def euler_totient(n):
    """Compute Euler's totient function phi(n)."""
    if n == 1:
        return 1
    result = n
    # Find all prime factors
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            # p is a prime factor
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        # temp is a prime factor
        result -= result // temp
    return result

def solve(input_text):
    lines = input_text.strip().split('\n')
    output_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        if n == 0:
            break
        output_lines.append(str(euler_totient(n)))
    return '\n'.join(output_lines) + '\n'

if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text), end='')
