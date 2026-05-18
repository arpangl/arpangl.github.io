import sys

def solve(input_data):
    tokens = input_data.split()
    idx = 0
    results = []
    while idx < len(tokens):
        n = int(tokens[idx]); idx += 1
        if n == 0:
            break
        bets = []
        for i in range(n):
            bets.append(int(tokens[idx])); idx += 1
        # Kadane's algorithm for maximum subarray sum
        max_ending_here = 0
        max_so_far = 0
        for b in bets:
            max_ending_here = max(0, max_ending_here + b)
            max_so_far = max(max_so_far, max_ending_here)
        if max_so_far > 0:
            results.append(f"The maximum winning streak is {max_so_far}.")
        else:
            results.append("Losing streak.")
    return "\n".join(results) + "\n"

if __name__ == "__main__":
    data = sys.stdin.read()
    print(solve(data), end="")
