import sys
from itertools import combinations

def solve(arr):
    """
    Given a set of positive integers, find all subsets A' such that
    sum(A') = sum(A - A') = total_sum / 2.

    For n <= 30 and a_i up to 10^12, we use meet-in-the-middle approach.
    Split the array into two halves, enumerate all subsets of each half,
    then combine.
    """
    n = len(arr)
    total = sum(arr)

    if total % 2 != 0:
        return []

    target = total // 2

    # We need subsets of arr that sum to target.
    # Use meet-in-the-middle: split arr into two halves.

    mid = n // 2
    left = arr[:mid]
    right = arr[mid:]
    nl = len(left)
    nr = len(right)

    # Enumerate all subsets of right half: map from sum -> list of bitmasks
    right_sums = {}
    for mask in range(1 << nr):
        s = 0
        for i in range(nr):
            if mask & (1 << i):
                s += right[i]
        if s not in right_sums:
            right_sums[s] = []
        right_sums[s].append(mask)

    results = []

    # Enumerate all subsets of left half
    for lmask in range(1 << nl):
        ls = 0
        for i in range(nl):
            if lmask & (1 << i):
                ls += left[i]

        need = target - ls
        if need in right_sums:
            for rmask in right_sums[need]:
                # Build the subset
                subset = []
                for i in range(nl):
                    if lmask & (1 << i):
                        subset.append(arr[i])
                for i in range(nr):
                    if rmask & (1 << i):
                        subset.append(arr[mid + i])

                # We need A' to be a proper subset (not empty, not full set)
                # Actually, re-reading the problem: A' subset A means A' can be
                # any subset including empty set? But sum must equal sum of complement.
                # If A' is empty, sum(A') = 0, sum(A-A') = total != 0 (since all positive).
                # If A' = A, sum(A-A') = 0 != total. So neither empty nor full set works
                # unless total = 0, which can't happen with positive integers.
                # Also, {A'} and {A - A'} are essentially the same partition.
                # We should only count each partition once: pick the subset with sum = target
                # that is "smaller" in some canonical sense.
                # Looking at the sample: {1,2,3,4,5,6,7}, target=14
                # They list 8 subsets: {1,6,7}, {2,5,7}, etc.
                # Note {1,6,7} and {2,3,4,5} are complements, and both appear.
                # So they list ALL subsets (both A' and A-A'), each partition counted twice.
                # Wait, let me recount: 8 subsets for 4 partitions?
                # {1,6,7} + {2,3,4,5} = partition 1 (both listed)
                # {2,5,7} + {1,3,4,6} = partition 2 (both listed)
                # {3,4,7} + {1,2,5,6} = partition 3 (both listed)
                # {3,5,6} + {1,2,4,7} = partition 4 (both listed)
                # Yes! 4 partitions, 8 subsets total. So we list ALL subsets with sum = target.
                # But we must exclude the empty set and the full set (neither can have sum = target
                # for positive integers anyway).

                if len(subset) > 0 and len(subset) < n:
                    subset.sort()
                    results.append(tuple(subset))

    # Remove duplicates (shouldn't happen if all elements are distinct, but just in case)
    results = sorted(set(results), key=lambda x: (len(x), x))

    return results


def main():
    import fileinput

    lines = []
    for line in sys.stdin:
        lines.append(line.strip())

    # Parse input: each dataset is enclosed by {}, may span multiple lines
    # Terminated by a line containing only '.'

    datasets = []
    buffer = ""
    for line in lines:
        if line == '.':
            break
        buffer += " " + line

    # Extract all {...} blocks from buffer
    i = 0
    while i < len(buffer):
        if buffer[i] == '{':
            j = buffer.index('}', i)
            content = buffer[i+1:j].strip()
            if content:
                arr = list(map(int, content.split()))
            else:
                arr = []
            datasets.append(arr)
            i = j + 1
        else:
            i += 1

    first = True
    for arr in datasets:
        if not first:
            print()
        first = False

        results = solve(arr)

        if not results:
            print("No such subset")
        else:
            print(f"{len(results)} subsets.")
            for subset in results:
                print("{" + " ".join(map(str, subset)) + "}")


if __name__ == "__main__":
    main()
