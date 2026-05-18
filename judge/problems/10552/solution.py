import sys
import re

def solve(input_data):
    lines = input_data.split('\n')
    idx = 0
    run_num = 0
    results = []

    while idx < len(lines):
        line = lines[idx].strip()
        idx += 1
        if not line:
            continue
        n = int(line)
        if n == 0:
            break

        # Read n lines of standard solution
        standard_lines = []
        for _ in range(n):
            if idx < len(lines):
                standard_lines.append(lines[idx])
                idx += 1
            else:
                standard_lines.append('')

        # Read m
        while idx < len(lines) and lines[idx].strip() == '':
            idx += 1
        m = int(lines[idx].strip())
        idx += 1

        # Read m lines of team output
        team_lines = []
        for _ in range(m):
            if idx < len(lines):
                team_lines.append(lines[idx])
                idx += 1
            else:
                team_lines.append('')

        run_num += 1

        # Join all lines with newline to form the full text
        standard_text = '\n'.join(standard_lines)
        team_text = '\n'.join(team_lines)

        if standard_text == team_text:
            results.append(f"Run #{run_num}: Accepted")
        else:
            # Extract numeric characters
            standard_nums = re.sub(r'[^0-9]', '', standard_text)
            team_nums = re.sub(r'[^0-9]', '', team_text)
            if standard_nums == team_nums:
                results.append(f"Run #{run_num}: Presentation Error")
            else:
                results.append(f"Run #{run_num}: Wrong Answer")

    return '\n'.join(results) + '\n' if results else ''

if __name__ == '__main__':
    data = sys.stdin.read()
    print(solve(data), end='')
