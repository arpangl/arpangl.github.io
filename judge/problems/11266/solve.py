import sys

def count_sequence(a0):
    seen = set()
    a = a0
    while a not in seen:
        seen.add(a)
        # Square it, pad to 8 digits, take middle 4
        sq = a * a
        sq_str = f"{sq:08d}"
        a = int(sq_str[2:6])
    return len(seen)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    a0 = int(line)
    if a0 == 0:
        break
    print(count_sequence(a0))
