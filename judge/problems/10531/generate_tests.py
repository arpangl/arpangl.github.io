#!/usr/bin/env python3
"""
Generate test cases for Zipf's Law (10531).
"""
import os
import re
import random
import string

TESTCASE_DIR = '/Users/lambert/Documents/GPE-Helper/judge/problems/10531/testcases'

def solve(input_text):
    lines = input_text.split('\n')
    results = []
    i = 0
    first_case = True
    while i < len(lines):
        line = lines[i].strip()
        if line == '':
            i += 1
            continue
        n = int(line)
        i += 1
        word_count = {}
        while i < len(lines):
            text_line = lines[i]
            i += 1
            if text_line.strip() == 'EndOfText':
                break
            words = re.findall(r'[a-zA-Z]+', text_line)
            for w in words:
                w_lower = w.lower()
                word_count[w_lower] = word_count.get(w_lower, 0) + 1
        matching = sorted([w for w, c in word_count.items() if c == n])
        if not first_case:
            results.append('')
        first_case = False
        if matching:
            for w in matching:
                results.append(w)
        else:
            results.append('There is no such word.')
    return '\n'.join(results)

def write_case(case_num, input_text):
    inp = input_text.rstrip('\n') + '\n'
    out = solve(inp)
    in_path = os.path.join(TESTCASE_DIR, f'{case_num:02d}.in')
    out_path = os.path.join(TESTCASE_DIR, f'{case_num:02d}.out')
    with open(in_path, 'w') as f:
        f.write(inp)
    with open(out_path, 'w') as f:
        f.write(out + '\n')
    # Print summary
    out_lines = out.split('\n')
    print(f"  Case {case_num:02d}: input {len(inp.splitlines())} lines, output {len(out_lines)} lines")
    for line in out_lines[:5]:
        print(f"    {line}")
    if len(out_lines) > 5:
        print(f"    ... ({len(out_lines) - 5} more lines)")

case_num = 1

# --- Test 1: Sample test case ---
print("Test 1: Sample test case")
write_case(case_num, """2

In practice, the difference between theory and practice is always
greater than the difference between theory and practice in theory.
\t- Anonymous

Man will occasionally stumble over the truth, but most of the
time he will pick himself up and continue on.
        - W. S. L. Churchill
EndOfText""")
case_num += 1

# --- Test 2: n=1, simple case ---
print("Test 2: n=1, unique words only")
write_case(case_num, """1
hello world
EndOfText""")
case_num += 1

# --- Test 3: No matching words ---
print("Test 3: No words with count n")
write_case(case_num, """5
the cat sat on the mat
EndOfText""")
case_num += 1

# --- Test 4: All words appear exactly n times ---
print("Test 4: All words appear exactly n=2 times")
write_case(case_num, """2
apple banana apple banana
EndOfText""")
case_num += 1

# --- Test 5: Case insensitivity ---
print("Test 5: Case insensitivity")
write_case(case_num, """2
Hello hello HELLO HeLLo
World world WORLD
EndOfText""")
case_num += 1

# --- Test 6: Words separated by various non-letters ---
print("Test 6: Non-letter separators (digits, punctuation, tabs)")
write_case(case_num, """1
well-known... isn't it? yes123no 42abc
EndOfText""")
case_num += 1

# --- Test 7: Single word repeated many times ---
print("Test 7: Single word repeated n times")
write_case(case_num, """3
test test test
EndOfText""")
case_num += 1

# --- Test 8: n=1, no unique words (all repeated) ---
print("Test 8: n=1 but all words repeat")
write_case(case_num, """1
go go stop stop
EndOfText""")
case_num += 1

# --- Test 9: Multiple test cases in one input ---
print("Test 9: Multiple test cases")
write_case(case_num, """2
to be or not to be
EndOfText
1
the quick brown fox jumps over the lazy dog
EndOfText
3
aaa bbb aaa bbb aaa bbb ccc
EndOfText""")
case_num += 1

# --- Test 10: Large n that nothing matches ---
print("Test 10: Very large n, nothing matches")
write_case(case_num, """1000
just a few words here
EndOfText""")
case_num += 1

# --- Test 11: Empty text (no words at all) ---
print("Test 11: Empty text block")
write_case(case_num, """1

EndOfText""")
case_num += 1

# --- Test 12: Only non-letter characters ---
print("Test 12: Only non-letter characters in text")
write_case(case_num, """1
123 456 --- *** !!!
EndOfText""")
case_num += 1

# --- Test 13: Single character words ---
print("Test 13: Single character words with case mixing")
write_case(case_num, """2
a A b B c C a b c
EndOfText""")
case_num += 1

# --- Test 14: Very long words ---
print("Test 14: Very long words")
long_word_a = "a" * 100
long_word_b = "b" * 100
write_case(case_num, f"""2
{long_word_a} {long_word_b} {long_word_a} {long_word_b}
EndOfText""")
case_num += 1

# --- Test 15: Alphabetical ordering check ---
print("Test 15: Alphabetical ordering verification")
write_case(case_num, """1
zebra apple mango banana kiwi cherry
EndOfText""")
case_num += 1

# --- Test 16: Mixed case with same word different cases ---
print("Test 16: Same word in many case variants, n matches exactly")
write_case(case_num, """5
Cat CAT cat cAt CaT dog DOG Dog dOg doG
EndOfText""")
case_num += 1

# --- Test 17: Multiple cases, one with no match, one with match ---
print("Test 17: Multiple cases alternating match/no-match")
write_case(case_num, """3
one two three
EndOfText
1
one two three
EndOfText
2
one one two two three
EndOfText""")
case_num += 1

# --- Test 18: Larger text with many words, moderate n ---
print("Test 18: Larger generated text")
random.seed(42)
vocab = ['the', 'a', 'an', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
         'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
         'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
         'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
         'from', 'up', 'about', 'into', 'over', 'after', 'cat', 'dog', 'bird',
         'fish', 'tree', 'house', 'car', 'book', 'word', 'page', 'line', 'text',
         'code', 'test', 'data', 'file', 'name', 'time', 'year', 'people',
         'way', 'day', 'man', 'woman', 'child', 'world', 'life', 'hand',
         'part', 'place', 'case', 'week', 'company', 'system', 'program',
         'question', 'work', 'government', 'number', 'night', 'point', 'home',
         'water', 'room', 'mother', 'area', 'money', 'story', 'fact', 'month',
         'lot', 'right', 'study', 'problem', 'game', 'member', 'city', 'end']
text_words = [random.choice(vocab) for _ in range(500)]
lines = []
for i in range(0, len(text_words), 12):
    lines.append(' '.join(text_words[i:i+12]))
text_block = '\n'.join(lines)
write_case(case_num, f"""4
{text_block}
EndOfText""")
case_num += 1

# --- Test 19: Words with embedded digits as separators ---
print("Test 19: Words separated by digits")
write_case(case_num, """2
abc1abc2abc def3def
EndOfText""")
case_num += 1

# --- Test 20: Three test cases, stress blank line between ---
print("Test 20: Three cases testing blank line formatting")
write_case(case_num, """1
alpha
EndOfText
1
beta
EndOfText
1
gamma
EndOfText""")
case_num += 1

print(f"\nGenerated {case_num - 1} test cases total.")
