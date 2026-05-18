import sys

def solve(input_text):
    """
    Uncompress: Given compressed text, reproduce the original.

    Compression scheme:
    - Maintain a list of words (most recently used at front).
    - When reading compressed text:
      - Non-alphabetic, non-digit characters are copied directly.
      - Words (sequences of letters) are copied directly and placed at front of list.
      - Numbers (sequences of digits) represent a 1-based index into the list;
        replace with the word at that position, then move that word to front of list.
    - Input ends with "0" on a line by itself.
    """
    lines = input_text.split('\n')
    word_list = []
    output_lines = []

    for line in lines:
        # Check for terminating 0
        if line.strip() == '0':
            break

        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch.isalpha():
                # Read a word
                j = i
                while j < len(line) and line[j].isalpha():
                    j += 1
                word = line[i:j]
                # First occurrence: just add to front
                # The word is always placed at front of list
                # If it already exists, it's moved to front
                # But according to the problem: if first occurrence, copy directly and put at front
                # If not first occurrence... but wait, in the compressed file,
                # non-first occurrences are replaced by numbers. So if we see a word in
                # compressed input, it IS a first occurrence.
                # Actually re-reading: in the compressed file, words appear only on first occurrence.
                # Subsequent occurrences are replaced by their position number.
                # So when decompressing:
                # - If we see a word (letters), it's a new word. Put at front of list. Output it.
                # - If we see a number (digits), look up that position in list, output that word,
                #   move it to front.
                word_list.insert(0, word)
                result.append(word)
                i = j
            elif ch.isdigit():
                # Read a number
                j = i
                while j < len(line) and line[j].isdigit():
                    j += 1
                num = int(line[i:j])
                # Position is 1-based
                word = word_list[num - 1]
                # Move to front
                word_list.pop(num - 1)
                word_list.insert(0, word)
                result.append(word)
                i = j
            else:
                result.append(ch)
                i += 1

        output_lines.append(''.join(result))

    return '\n'.join(output_lines)


if __name__ == '__main__':
    input_text = sys.stdin.read()
    print(solve(input_text), end='')
