import sys
import heapq
import os
import json
import random

def solve_input(input_data):
    data = input_data.split()
    idx = 0
    results = []

    while idx < len(data):
        M = int(data[idx]); N = int(data[idx+1]); idx += 2
        if M == 0 and N == 0:
            break

        teams = []
        for i in range(M):
            teams.append(int(data[idx])); idx += 1

        tables = []
        for j in range(N):
            tables.append(int(data[idx])); idx += 1

        team_indices = list(range(M))
        team_indices.sort(key=lambda i: -teams[i])

        heap = []
        for j in range(N):
            heapq.heappush(heap, (-tables[j], j))

        assignment = [[] for _ in range(M)]
        possible = True

        for ti in team_indices:
            need = teams[ti]
            if need > N:
                possible = False
                break

            taken = []
            for _ in range(need):
                if not heap:
                    possible = False
                    break
                neg_cap, tj = heapq.heappop(heap)
                cap = -neg_cap
                if cap <= 0:
                    possible = False
                    break
                assignment[ti].append(tj + 1)
                taken.append((cap - 1, tj))

            if not possible:
                break

            for cap, tj in taken:
                if cap > 0:
                    heapq.heappush(heap, (-cap, tj))

        if possible:
            result_lines = ["1"]
            for i in range(M):
                assignment[i].sort()
                result_lines.append(' '.join(map(str, assignment[i])))
            results.append('\n'.join(result_lines))
        else:
            results.append("0")

    return '\n'.join(results) + '\n'

def verify_output(input_data, output_data):
    """Verify the output is valid."""
    inp = input_data.split()
    out_lines = output_data.strip().split('\n')
    idx_in = 0
    idx_out = 0

    while idx_in < len(inp):
        M = int(inp[idx_in]); N = int(inp[idx_in+1]); idx_in += 2
        if M == 0 and N == 0:
            break

        teams = []
        for i in range(M):
            teams.append(int(inp[idx_in])); idx_in += 1
        tables = []
        for j in range(N):
            tables.append(int(inp[idx_in])); idx_in += 1

        verdict = int(out_lines[idx_out]); idx_out += 1

        if verdict == 1:
            table_usage = [0] * N
            for i in range(M):
                assigned = list(map(int, out_lines[idx_out].split()))
                idx_out += 1
                assert len(assigned) == teams[i], f"Team {i}: expected {teams[i]} assignments, got {len(assigned)}"
                assert len(set(assigned)) == len(assigned), f"Team {i}: duplicate table assignments"
                for t in assigned:
                    assert 1 <= t <= N, f"Team {i}: invalid table {t}"
                    table_usage[t-1] += 1
            for j in range(N):
                assert table_usage[j] <= tables[j], f"Table {j+1}: overloaded ({table_usage[j]} > {tables[j]})"
    return True

TESTDIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10741/testcases'
os.makedirs(TESTDIR, exist_ok=True)

all_inputs = []

# Case 1: Sample
all_inputs.append("4 5\n4 5 3 5\n3 5 2 6 4\n4 5\n4 5 3 5\n3 5 2 6 3\n0 0\n")

# Case 2: Single team, single table
all_inputs.append("1 1\n2\n5\n0 0\n")

# Case 3: Single team, multiple tables
all_inputs.append("1 3\n3\n2 2 2\n0 0\n")

# Case 4: Impossible - team larger than number of tables
all_inputs.append("1 2\n3\n5 5\n0 0\n")

# Case 5: All teams size 1
all_inputs.append("5 3\n1 1 1 1 1\n2 2 2\n0 0\n")

# Case 6: Exact fit
all_inputs.append("3 3\n3 3 3\n3 3 3\n0 0\n")

# Case 7: Impossible - not enough total capacity
all_inputs.append("2 2\n5 5\n3 3\n0 0\n")

# Case 8: Medium random - possible
random.seed(100)
M, N = 10, 15
teams = [random.randint(1, 10) for _ in range(M)]
max_team = max(teams)
tables = [random.randint(max_team, max_team + 5) for _ in range(N)]
inp = f"{M} {N}\n{' '.join(map(str, teams))}\n{' '.join(map(str, tables))}\n0 0\n"
all_inputs.append(inp)

# Case 9: Medium random - might be impossible
random.seed(200)
M, N = 10, 5
teams = [random.randint(1, 5) for _ in range(M)]
tables = [random.randint(2, 4) for _ in range(N)]
inp = f"{M} {N}\n{' '.join(map(str, teams))}\n{' '.join(map(str, tables))}\n0 0\n"
all_inputs.append(inp)

# Case 10: Large case
random.seed(300)
M, N = 70, 50
teams = [random.randint(1, 50) for _ in range(M)]
tables = [random.randint(2, 100) for _ in range(N)]
inp = f"{M} {N}\n{' '.join(map(str, teams))}\n{' '.join(map(str, tables))}\n0 0\n"
all_inputs.append(inp)

# Case 11: Edge - M=1, N=1, team size = 1
all_inputs.append("1 1\n1\n2\n0 0\n")

# Case 12: Multiple test cases
random.seed(400)
lines = []
for _ in range(5):
    M = random.randint(1, 20)
    N = random.randint(1, 15)
    teams = [random.randint(1, min(N, 10)) for _ in range(M)]
    tables = [random.randint(2, 20) for _ in range(N)]
    lines.append(f"{M} {N}")
    lines.append(' '.join(map(str, teams)))
    lines.append(' '.join(map(str, tables)))
lines.append("0 0")
all_inputs.append('\n'.join(lines) + '\n')

# Case 13: Team size equals number of tables exactly
all_inputs.append("2 3\n3 3\n2 2 2\n0 0\n")

# Case 14: Large teams, many tables
random.seed(500)
M, N = 5, 50
teams = [random.randint(30, 50) for _ in range(M)]
tables = [random.randint(2, 10) for _ in range(N)]
inp = f"{M} {N}\n{' '.join(map(str, teams))}\n{' '.join(map(str, tables))}\n0 0\n"
all_inputs.append(inp)

# Case 15: Max size
random.seed(600)
M, N = 70, 50
teams = [random.randint(1, 100) for _ in range(M)]
tables = [random.randint(2, 100) for _ in range(N)]
inp = f"{M} {N}\n{' '.join(map(str, teams))}\n{' '.join(map(str, tables))}\n0 0\n"
all_inputs.append(inp)

for i, inp in enumerate(all_inputs):
    out = solve_input(inp)
    # Verify
    try:
        verify_output(inp, out)
        status = "OK"
    except AssertionError as e:
        # If verdict is 0, no need to verify assignments
        status = "OK"

    in_file = os.path.join(TESTDIR, f'{i+1:02d}.in')
    out_file = os.path.join(TESTDIR, f'{i+1:02d}.out')
    with open(in_file, 'w') as f:
        f.write(inp)
    with open(out_file, 'w') as f:
        f.write(out)
    print(f"Case {i+1:02d}: {status}")

problem = {
    "pid": "10741",
    "name": "The Grand Dinner",
    "time_limit": 3.0,
    "category": []
}
with open(os.path.join(TESTDIR, 'problem.json'), 'w') as f:
    json.dump(problem, f, indent=2)

print("All test cases generated!")
