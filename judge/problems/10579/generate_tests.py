import random
import string
import os

TESTCASES_DIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10579/testcases'

def solve(input_data):
    lines = input_data.strip().split('\n')
    idx = 0
    m, n = map(int, lines[idx].split())
    idx += 1

    dictionary = {}
    for i in range(m):
        parts = lines[idx].split()
        word = parts[0]
        value = int(parts[1])
        dictionary[word] = value
        idx += 1

    results = []
    for _ in range(n):
        total = 0
        while idx < len(lines):
            line = lines[idx]
            idx += 1
            if line.strip() == '.':
                break
            words = line.split()
            for w in words:
                if w in dictionary:
                    total += dictionary[w]
        results.append(str(total))

    return '\n'.join(results)


def random_word(min_len=1, max_len=16):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def write_case(case_num, input_text, output_text):
    prefix = f"{case_num:02d}"
    with open(os.path.join(TESTCASES_DIR, f"{prefix}.in"), 'w') as f:
        f.write(input_text)
    with open(os.path.join(TESTCASES_DIR, f"{prefix}.out"), 'w') as f:
        f.write(output_text)


def generate_case(case_num, input_text):
    output_text = solve(input_text)
    write_case(case_num, input_text, output_text + '\n')
    # Verify by solving again
    assert solve(input_text) == output_text
    print(f"  Case {case_num:02d}: OK")


case_num = 0

# Case 01: Sample test case
case_num += 1
inp = """7 2
administer 100000
spending 200000
manage 50000
responsibility 25000
expertise 100
skill 50
money 75000
the incumbent will administer the spending of kindergarden milk money
and exercise responsibility for making change he or she will share
responsibility for the task of managing the money with the assistant
whose skill and expertise shall ensure the successful spending exercise
.
this individual must have the skill to perform a heart transplant and
expertise in rocket science
."""
generate_case(case_num, inp)

# Case 02: Empty dictionary (m=0), single job description with words -> all 0
case_num += 1
inp = """0 1
hello world this is a test
."""
generate_case(case_num, inp)

# Case 03: Single dictionary word, single job with that word repeated
case_num += 1
inp = """1 1
budget 500000
budget budget budget
."""
generate_case(case_num, inp)

# Case 04: Single dictionary word, word not in job description
case_num += 1
inp = """1 1
budget 500000
no matching words here
."""
generate_case(case_num, inp)

# Case 05: Multiple job descriptions, some empty (just a period on a line)
case_num += 1
inp = """2 3
alpha 10
beta 20
alpha beta alpha
.
.
beta beta
."""
generate_case(case_num, inp)

# Case 06: Words with numbers mixed in (alphanumeric tokens)
case_num += 1
inp = """3 1
manage 100
budget 200
level3 50
manage the budget at level3 priority
."""
generate_case(case_num, inp)

# Case 07: Dictionary word appears as substring of another word (should NOT match)
case_num += 1
inp = """2 1
man 100
age 200
manage the manager
."""
generate_case(case_num, inp)

# Case 08: Large dictionary values, multiple occurrences
case_num += 1
inp = """3 2
supervise 1000000
control 999999
plan 500000
supervise and control the plan
.
supervise supervise supervise control control plan plan plan
."""
generate_case(case_num, inp)

# Case 09: Single character dictionary words
case_num += 1
inp = """3 1
a 1
b 2
c 3
a b c a b c a b c
."""
generate_case(case_num, inp)

# Case 10: Job description with only non-dictionary words -> salary 0
case_num += 1
inp = """5 1
alpha 100
beta 200
gamma 300
delta 400
epsilon 500
this job has no matching keywords at all
."""
generate_case(case_num, inp)

# Case 11: Multiple lines in a job description, each with dictionary words
case_num += 1
inp = """4 1
lead 50000
team 30000
project 20000
deliver 10000
lead the team on this project
deliver the project on time
lead and deliver
."""
generate_case(case_num, inp)

# Case 12: Value of 0 for a dictionary word
case_num += 1
inp = """3 1
important 0
trivial 100
key 200
important important important trivial key
."""
generate_case(case_num, inp)

# Case 13: Multiple jobs, varying sizes
case_num += 1
inp = """5 4
manage 100
budget 200
skill 50
lead 300
team 150
manage budget skill lead team
.
manage
.
skill skill skill
.
lead team budget
."""
generate_case(case_num, inp)

# Case 14: Larger random test
case_num += 1
random.seed(42)
m = 50
n = 10
dict_words = []
lines_out = []
lines_out.append(f"{m} {n}")
used_words = set()
for _ in range(m):
    w = random_word(3, 10)
    while w in used_words:
        w = random_word(3, 10)
    used_words.add(w)
    val = random.randint(0, 1000000)
    dict_words.append((w, val))
    lines_out.append(f"{w} {val}")

all_dict_words = [w for w, v in dict_words]
filler_words = ["the", "and", "of", "for", "in", "to", "with", "on", "at", "by",
                 "this", "that", "from", "will", "has", "have", "been", "are", "is"]

for _ in range(n):
    num_lines = random.randint(1, 5)
    for _ in range(num_lines):
        num_words = random.randint(3, 12)
        line_words = []
        for _ in range(num_words):
            if random.random() < 0.4:
                line_words.append(random.choice(all_dict_words))
            else:
                line_words.append(random.choice(filler_words))
        lines_out.append(' '.join(line_words))
    lines_out.append('.')

inp = '\n'.join(lines_out)
generate_case(case_num, inp)

# Case 15: Stress test with many dictionary words and many jobs
case_num += 1
random.seed(123)
m = 200
n = 50
dict_words = []
lines_out = []
lines_out.append(f"{m} {n}")
used_words = set()
for _ in range(m):
    w = random_word(2, 16)
    while w in used_words:
        w = random_word(2, 16)
    used_words.add(w)
    val = random.randint(1, 1000000)
    dict_words.append((w, val))
    lines_out.append(f"{w} {val}")

all_dict_words = [w for w, v in dict_words]
filler_words = ["the", "and", "of", "for", "in", "to", "with", "on", "at", "by",
                 "this", "that", "from", "will", "has", "have", "been", "are", "is",
                 "a", "an", "their", "our", "such", "which", "or", "but", "if"]

for _ in range(n):
    num_lines = random.randint(1, 8)
    for _ in range(num_lines):
        num_words = random.randint(3, 15)
        line_words = []
        for _ in range(num_words):
            if random.random() < 0.35:
                line_words.append(random.choice(all_dict_words))
            else:
                line_words.append(random.choice(filler_words))
        lines_out.append(' '.join(line_words))
    lines_out.append('.')

inp = '\n'.join(lines_out)
generate_case(case_num, inp)

# Case 16: Job description with lines that have extra spaces (multiple spaces between words)
case_num += 1
inp = """2 1
hello 100
world 200
hello  world  hello  world
."""
generate_case(case_num, inp)

# Case 17: Dictionary word is same as a number token in job description
case_num += 1
inp = """2 1
123 500
abc 100
123 abc 456 abc 123
."""
generate_case(case_num, inp)

# Case 18: Many jobs all empty (just period)
case_num += 1
inp = """3 5
x 10
y 20
z 30
.
.
.
.
."""
generate_case(case_num, inp)

# Case 19: Single job with a very long line
case_num += 1
random.seed(999)
m = 5
dict_words_19 = [("alpha", 1), ("beta", 2), ("gamma", 3), ("delta", 4), ("epsilon", 5)]
lines_out = [f"{m} 1"]
for w, v in dict_words_19:
    lines_out.append(f"{w} {v}")

# Generate a long line with ~500 words
words_in_line = []
for _ in range(500):
    if random.random() < 0.3:
        words_in_line.append(random.choice([w for w, v in dict_words_19]))
    else:
        words_in_line.append(random_word(3, 8))
lines_out.append(' '.join(words_in_line))
lines_out.append('.')
inp = '\n'.join(lines_out)
generate_case(case_num, inp)

# Case 20: Maximum value words appearing many times
case_num += 1
inp = """1 1
money 1000000
money money money money money money money money money money
."""
generate_case(case_num, inp)

print(f"\nGenerated {case_num} test cases successfully.")
