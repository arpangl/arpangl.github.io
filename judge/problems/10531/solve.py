#!/usr/bin/env python3
"""
Zipf's Law - Problem 10531
Find all words occurring exactly n times in a text.
A word is a sequence of letters. Capitalization ignored.
"""
import sys
import re

def solve(input_text):
    lines = input_text.split('\n')
    results = []
    i = 0
    first_case = True
    while i < len(lines):
        # Skip empty lines before n
        line = lines[i].strip()
        if line == '':
            i += 1
            continue
        # Read n
        n = int(line)
        i += 1
        # Read text until EndOfText
        word_count = {}
        while i < len(lines):
            text_line = lines[i]
            i += 1
            if text_line.strip() == 'EndOfText':
                break
            # Extract words (sequences of letters)
            words = re.findall(r'[a-zA-Z]+', text_line)
            for w in words:
                w_lower = w.lower()
                word_count[w_lower] = word_count.get(w_lower, 0) + 1
        # Find words with count == n
        matching = sorted([w for w, c in word_count.items() if c == n])
        if not first_case:
            results.append('')  # blank line between cases
        first_case = False
        if matching:
            for w in matching:
                results.append(w)
        else:
            results.append('There is no such word.')
    return '\n'.join(results)

if __name__ == '__main__':
    data = sys.stdin.read()
    print(solve(data))
