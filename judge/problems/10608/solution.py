import sys

def solve():
    input_data = sys.stdin.read().split('\n')
    idx = 0

    def next_line():
        nonlocal idx
        while idx < len(input_data):
            line = input_data[idx].strip()
            idx += 1
            return line
        return None

    T = None
    # Read number of test cases, skipping blank lines
    while T is None:
        line = next_line()
        if line is None:
            return
        if line != '':
            T = int(line)

    results = []

    for t in range(T):
        # Skip blank lines before test case
        M = None
        while M is None:
            line = next_line()
            if line is None:
                break
            if line != '':
                M = int(line)

        if M is None:
            break

        segments = []
        while True:
            line = next_line()
            if line is None:
                break
            if line == '':
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            l, r = int(parts[0]), int(parts[1])
            if l == 0 and r == 0:
                break
            segments.append((l, r))

        # Greedy interval covering of [0, M]
        # Sort segments by left endpoint, then by right endpoint descending
        segments.sort(key=lambda x: (x[0], -x[1]))

        chosen = []
        current_end = 0
        i = 0
        n = len(segments)

        while current_end < M:
            # Find the segment that starts <= current_end and extends the farthest
            best_r = current_end
            best_seg = None

            while i < n and segments[i][0] <= current_end:
                if segments[i][1] > best_r:
                    best_r = segments[i][1]
                    best_seg = segments[i]
                i += 1

            if best_seg is None or best_r == current_end:
                # Can't extend further
                chosen = None
                break

            chosen.append(best_seg)
            current_end = best_r

        if chosen is None or current_end < M:
            results.append("0")
        else:
            # Sort chosen by left endpoint
            chosen.sort(key=lambda x: (x[0], -x[1]))
            lines = [str(len(chosen))]
            for seg in chosen:
                lines.append(f"{seg[0]} {seg[1]}")
            results.append('\n'.join(lines))

    print('\n\n'.join(results))

solve()
