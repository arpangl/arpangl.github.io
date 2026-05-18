import sys
from itertools import combinations

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        seq = []
        for i in range(n):
            seq.append(int(input_data[idx])); idx += 1

        # Find all strictly increasing subsequences, track the longest ones
        # n <= 9, so we can enumerate all 2^n subsets
        best_len = 0
        all_lis = []

        for length in range(1, n + 1):
            for combo in combinations(range(n), length):
                subseq = [seq[i] for i in combo]
                # Check strictly increasing
                is_increasing = True
                for i in range(1, len(subseq)):
                    if subseq[i] <= subseq[i - 1]:
                        is_increasing = False
                        break
                if is_increasing:
                    if length > best_len:
                        best_len = length
                        all_lis = [subseq]
                    elif length == best_len:
                        all_lis.append(subseq)

        results.append((len(all_lis), all_lis))

    output_lines = []
    for count, subsequences in results:
        output_lines.append(str(count))
        for subseq in subsequences:
            output_lines.append(" ".join(map(str, subseq)))
    print("\n".join(output_lines))

solve()
