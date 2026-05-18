#!/usr/bin/env python3
"""
Generate test cases for Problem 24941: Uncompress
"""
import random
import string
import os

# We generate ORIGINAL (uncompressed) text, then compress it, then verify decompression.

def compress(original_text):
    """
    Compress original text according to the scheme:
    - Maintain a list of words (MRU at front).
    - Non-alpha chars copied directly.
    - Words: if first occurrence, copy directly and put at front of list.
    - Words: if not first occurrence, output its 1-based position in list, move to front.
    """
    word_list = []
    lines = original_text.split('\n')
    compressed_lines = []

    for line in lines:
        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch.isalpha():
                j = i
                while j < len(line) and line[j].isalpha():
                    j += 1
                word = line[i:j]
                if word in word_list:
                    pos = word_list.index(word) + 1  # 1-based
                    result.append(str(pos))
                    word_list.pop(word_list.index(word))
                    word_list.insert(0, word)
                else:
                    result.append(word)
                    word_list.insert(0, word)
                i = j
            else:
                result.append(ch)
                i += 1
        compressed_lines.append(''.join(result))

    return '\n'.join(compressed_lines)


def decompress(compressed_text):
    """Decompress - same as solve.py"""
    lines = compressed_text.split('\n')
    word_list = []
    output_lines = []

    for line in lines:
        if line.strip() == '0':
            break
        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch.isalpha():
                j = i
                while j < len(line) and line[j].isalpha():
                    j += 1
                word = line[i:j]
                word_list.insert(0, word)
                result.append(word)
                i = j
            elif ch.isdigit():
                j = i
                while j < len(line) and line[j].isdigit():
                    j += 1
                num = int(line[i:j])
                word = word_list[num - 1]
                word_list.pop(num - 1)
                word_list.insert(0, word)
                result.append(word)
                i = j
            else:
                result.append(ch)
                i += 1
        output_lines.append(''.join(result))

    return '\n'.join(output_lines)


def random_word(min_len=1, max_len=10):
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def random_word_mixed_case(min_len=1, max_len=10):
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def write_case(case_num, original_text, base_dir):
    """Compress original text, write .in (compressed + "0") and .out (original)."""
    compressed = compress(original_text)
    in_text = compressed + '\n0\n'
    out_text = original_text + '\n'

    # Verify round-trip
    decompressed = decompress(in_text)
    assert decompressed == original_text, (
        f"Case {case_num}: round-trip failed!\n"
        f"Original:\n{repr(original_text)}\n"
        f"Compressed:\n{repr(compressed)}\n"
        f"Decompressed:\n{repr(decompressed)}"
    )

    in_path = os.path.join(base_dir, f'{case_num:02d}.in')
    out_path = os.path.join(base_dir, f'{case_num:02d}.out')
    with open(in_path, 'w') as f:
        f.write(in_text)
    with open(out_path, 'w') as f:
        f.write(out_text)
    print(f"  Case {case_num:02d}: OK ({len(original_text)} chars original)")


def main():
    base_dir = '/Users/lambert/Documents/GPE-Helper/judge/problems/24941/testcases'
    os.makedirs(base_dir, exist_ok=True)

    cases = []

    # ---- Case 01: Sample input ----
    cases.append(
        "Dear Sally,\n"
        "\n"
        "   Please, please do it--it would please\n"
        "Mary very, very much.  And Mary would\n"
        "do everything in Mary's power to make\n"
        "it pay off for you.\n"
        "\n"
        "   -- Thank you very much--"
    )

    # ---- Case 02: Single word ----
    cases.append("hello")

    # ---- Case 03: Single word repeated ----
    cases.append("hello hello hello")

    # ---- Case 04: Empty lines only ----
    cases.append("\n\n\n")

    # ---- Case 05: Only non-alpha characters ----
    cases.append("---...!!!???   ,,,(((")

    # ---- Case 06: Case sensitivity ----
    cases.append("abc Abc ABC abc Abc ABC abc")

    # ---- Case 07: Word with apostrophe (possessive) ----
    cases.append("Mary's cat ate Mary's food and Mary's cat slept")

    # ---- Case 08: Single characters as words ----
    cases.append("a b c a b c a b c a a a b b b c c c")

    # ---- Case 09: Long word (50 chars) ----
    long_word = "a" * 50
    cases.append(f"{long_word} is {long_word} and {long_word}")

    # ---- Case 10: Many different words, no repeats ----
    words = [random_word(3, 8) for _ in range(50)]
    # Ensure all unique
    words = list(dict.fromkeys(words))
    cases.append(' '.join(words))

    # ---- Case 11: Many repeats, words reordering in list ----
    vocab = ["the", "cat", "sat", "on", "mat"]
    sentence_words = [random.choice(vocab) for _ in range(40)]
    cases.append(' '.join(sentence_words))

    # ---- Case 12: Mixed case stress ----
    vocab2 = ["Hello", "hello", "HELLO", "hElLo", "World", "world", "WORLD"]
    sentence_words2 = [random.choice(vocab2) for _ in range(30)]
    cases.append(' '.join(sentence_words2))

    # ---- Case 13: Punctuation heavy ----
    cases.append(
        "well...well...well! What--what--what? "
        "Yes, yes, yes! No, no, no!"
    )

    # ---- Case 14: Multi-line with blank lines and special chars ----
    cases.append(
        "First line here.\n"
        "\n"
        "   Second line with spaces.\n"
        "Third--line--with--dashes.\n"
        "\n"
        "\n"
        "Last line here."
    )

    # ---- Case 15: Larger random test ----
    random.seed(42)
    vocab3 = [random_word_mixed_case(2, 12) for _ in range(30)]
    lines = []
    for _ in range(20):
        n_words = random.randint(3, 10)
        line_words = []
        for _ in range(n_words):
            w = random.choice(vocab3)
            sep = random.choice([' ', ', ', '--', '. ', '! ', '? ', "'s ", ' '])
            line_words.append(w + sep)
        lines.append(''.join(line_words).rstrip())
        if random.random() < 0.2:
            lines.append('')
    cases.append('\n'.join(lines))

    # ---- Case 16: Stress - large number of unique words ----
    random.seed(100)
    big_vocab = list(set(random_word_mixed_case(3, 15) for _ in range(500)))[:300]
    big_lines = []
    for _ in range(30):
        n = random.randint(5, 15)
        ws = [random.choice(big_vocab) for _ in range(n)]
        big_lines.append(' '.join(ws))
    cases.append('\n'.join(big_lines))

    # ---- Case 17: Word at position > 9 (multi-digit numbers in compressed) ----
    words17 = [f"word{chr(ord('a') + i)}" for i in range(20)]
    # introduce them all, then reference them in reverse
    line1 = ' '.join(words17)
    line2 = ' '.join(reversed(words17))
    cases.append(line1 + '\n' + line2)

    # ---- Case 18: Single letter words and punctuation ----
    cases.append("I, a, I; a! I? a. I--a")

    # ---- Case 19: Repeated word on same line many times ----
    cases.append("go go go go go go go go go go go go go go go")

    # ---- Case 20: Very long line ----
    random.seed(200)
    long_vocab = [random_word(3, 8) for _ in range(20)]
    long_line_parts = []
    for _ in range(200):
        long_line_parts.append(random.choice(long_vocab))
    cases.append(' '.join(long_line_parts))

    print(f"Generating {len(cases)} test cases...")
    for i, original in enumerate(cases, 1):
        write_case(i, original, base_dir)

    print(f"\nDone! {len(cases)} test cases written to {base_dir}")


if __name__ == '__main__':
    main()
