import sys

def solve(input_lines):
    idx = 0
    T = int(input_lines[idx]); idx += 1
    results = []
    for _ in range(T):
        n = int(input_lines[idx]); idx += 1
        instructions = []  # store the resolved delta for each instruction
        pos = 0
        for i in range(n):
            line = input_lines[idx].strip(); idx += 1
            if line == "LEFT":
                delta = -1
            elif line == "RIGHT":
                delta = 1
            else:
                # SAME AS i
                ref = int(line.split()[-1])
                delta = instructions[ref - 1]  # 1-indexed
            instructions.append(delta)
            pos += delta
        results.append(str(pos))
    return "\n".join(results)

if __name__ == "__main__":
    input_data = sys.stdin.read().strip().split("\n")
    print(solve(input_data))
