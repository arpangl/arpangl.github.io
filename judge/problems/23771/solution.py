import sys
import math

def solve():
    input_data = sys.stdin.read().split('\n')
    idx = 0
    T = int(input_data[idx]); idx += 1
    for case_num in range(1, T + 1):
        parts = input_data[idx].split(); idx += 1
        s = parts[0]
        k = int(parts[1])
        n = len(s)

        # s is the k-th (1-based) lexicographic permutation of n symbols
        # under some unknown alphabet ordering.
        # We need to find that alphabet ordering.
        #
        # Key insight: The k-th permutation of n items (in some order) tells us
        # which item is in each position. We can "decode" k into the permutation
        # indices (factoradic representation), which tells us for each position
        # which element (by rank in the remaining pool) was chosen.
        #
        # Given s and k, we know s is the result. The alphabet order is what we seek.
        #
        # If the alphabet order is alpha[0] < alpha[1] < ... < alpha[n-1],
        # then the k-th permutation picks from this sorted list.
        #
        # The k-th permutation (1-based) of a sorted list works as follows:
        # - Convert k-1 to factoradic: digits d[0], d[1], ..., d[n-1]
        #   where d[i] is in range [0, n-1-i]
        # - For position i, pick the d[i]-th element from the remaining sorted list.
        #
        # So if we decode k into factoradic digits, we know:
        #   s[i] = alpha[d[i]-th remaining element]
        #
        # We need to find alpha. Since s[i] is the d[i]-th remaining element of alpha,
        # we can reverse this: alpha is the sorted order, and we know the selection
        # sequence. We need to find the ordering of the original letters such that
        # applying the selection sequence d[0], d[1], ..., d[n-1] to the sorted list
        # yields s.
        #
        # Actually, let's think differently. The factoradic digits tell us the
        # "Lehmer code" of the permutation. From k, we get the Lehmer code.
        # The Lehmer code tells us: for position i, the element at position i
        # is the d[i]-th smallest among the remaining unused elements.
        #
        # So if the alphabet in order is alpha[], and we apply the Lehmer code:
        #   position 0 gets alpha[d[0]] (d[0]-th from all n elements)
        #   position 1 gets the d[1]-th from remaining n-1 elements
        #   etc.
        # And this must equal s.
        #
        # So s[0] = the d[0]-th element of alpha (0-based among all)
        # s[1] = the d[1]-th element of alpha minus {s[0]}
        # etc.
        #
        # We need to find alpha such that this holds.
        #
        # Equivalently: we know which "rank among remaining" each s[i] has.
        # So s[i] has rank d[i] among the remaining elements in alpha's order.
        #
        # This means: in the final alpha ordering, s[0] must be at overall rank d[0].
        # Then s[1] must be at rank d[1] among {all} \ {s[0]}, etc.
        #
        # But we can reverse this! We rebuild alpha by reversing the selection process.
        #
        # Reverse: start with an empty list. Process from last to first.
        # At step i (from n-1 down to 0):
        #   Insert s[i] at position d[i] in the list.
        # The final list is alpha in order.

        # Step 1: compute factoradic (Lehmer code) from k
        k -= 1  # 0-based
        lehmer = []
        for i in range(n):
            fact = math.factorial(n - 1 - i)
            digit = k // fact
            k = k % fact
            lehmer.append(digit)

        # Step 2: reverse the selection process
        # Process from last position to first, inserting s[i] at position lehmer[i]
        alpha = []
        for i in range(n - 1, -1, -1):
            alpha.insert(lehmer[i], s[i])

        print(f"Case {case_num}: {''.join(alpha)}")

solve()
