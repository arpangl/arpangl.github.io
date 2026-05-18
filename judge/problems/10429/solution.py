import sys
from collections import defaultdict

def solve(lines):
    """Solve one test case given a list of submission lines."""
    # For each contestant, track per-problem state
    # contestants[team][problem] = { 'solved': bool, 'penalty': int, 'wrong': int }
    contestants = defaultdict(lambda: defaultdict(lambda: {'solved': False, 'penalty': 0, 'wrong': 0}))
    seen_teams = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 4:
            continue
        team = int(parts[0])
        prob = int(parts[1])
        time = int(parts[2])
        verdict = parts[3]

        seen_teams.add(team)

        if verdict == 'C':
            if not contestants[team][prob]['solved']:
                contestants[team][prob]['solved'] = True
                contestants[team][prob]['penalty'] = time
        elif verdict == 'I':
            if not contestants[team][prob]['solved']:
                contestants[team][prob]['wrong'] += 1
        # R, U, E do not affect scoring

    results = []
    for team in seen_teams:
        total_solved = 0
        total_penalty = 0
        for prob in contestants[team]:
            info = contestants[team][prob]
            if info['solved']:
                total_solved += 1
                total_penalty += info['penalty'] + 20 * info['wrong']
        results.append((team, total_solved, total_penalty))

    # Sort: more problems solved first, then less penalty, then smaller team number
    results.sort(key=lambda x: (-x[1], x[2], x[0]))

    output_lines = []
    for team, solved, penalty in results:
        output_lines.append(f"{team} {solved} {penalty}")
    return output_lines


def main():
    input_data = sys.stdin.read()
    lines = input_data.split('\n')
    idx = 0
    # Read number of test cases
    while idx < len(lines) and lines[idx].strip() == '':
        idx += 1
    num_cases = int(lines[idx].strip())
    idx += 1
    # Skip blank line after number of cases
    while idx < len(lines) and lines[idx].strip() == '':
        idx += 1

    all_outputs = []
    for case_num in range(num_cases):
        case_lines = []
        while idx < len(lines) and lines[idx].strip() != '':
            case_lines.append(lines[idx])
            idx += 1
        # Skip blank lines between cases
        while idx < len(lines) and lines[idx].strip() == '':
            idx += 1
        all_outputs.append(solve(case_lines))

    for i, output in enumerate(all_outputs):
        if i > 0:
            print()
        print('\n'.join(output))


if __name__ == '__main__':
    main()
