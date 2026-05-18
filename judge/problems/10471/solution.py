import sys

def is_palindromic_time(h, m):
    """
    Check if HH:MM is palindromic.
    When determining if HH:MM is palindromic, ignore all leading zeroes in HH.
    If HH is zero then ignore all leading zeroes in MM.

    So the string to check is formed by:
    - Take HH as a number (strip leading zeros), convert to string
    - Take MM as a two-digit string (with leading zero if needed)
    - Concatenate: str(HH) + str(MM_two_digit)
    - But if HH == 0, then also strip leading zeros from MM

    Wait, let me re-read: "ignore all leading zeroes in HH. If HH is zero then ignore all leading zeroes in MM."

    So the string is formed by removing leading zeros from HH.
    If HH becomes "0" (i.e., the hour is 0), then also remove leading zeros from MM.

    Actually "ignore all leading zeroes in HH" means if HH=05, treat as "5".
    If HH=00, that's "0", but then "if HH is zero then ignore all leading zeroes in MM"
    means if HH=0, MM=05 becomes "5", and the full string is "05" -> no wait.

    Let me think about this with examples:
    - 00:00 -> HH=0, strip leading zeros -> "0", but HH is zero so strip leading zeros from MM too -> "0"
      Combined: "00" with colon removed...

    Actually let me re-read more carefully. The time is "HH:MM". When checking palindrome:
    1. Remove the colon, giving a 4-char string like "0000", "2330", "1459"
    2. Ignore leading zeroes in HH part
    3. If HH is zero, ignore leading zeroes in MM part

    So for "00:00" -> remove colon -> "0000" -> strip leading zeros from HH -> HH part is "",
    but HH is zero so strip leading zeros from MM -> MM part is "0" -> full string is "0"
    Is "0" a palindrome? Yes.

    But sample says 00:00 -> next is 00:01.
    00:01 -> HH is 0, strip leading zeros from HH -> "", HH is zero so strip leading zeros from MM "01" -> "1"
    Is "1" a palindrome? Yes! So 00:01 is palindromic. That matches.

    Let me verify 23:32:
    HH = 23, strip leading zeros -> "23". MM = "32". Combined: "2332".
    Is "2332" a palindrome? Yes! Good.

    15:51:
    HH = 15, strip leading zeros -> "15". MM = "51". Combined: "1551".
    Is "1551" a palindrome? Yes! Good.

    Let me verify 23:30 is NOT palindromic:
    HH = 23 -> "23", MM = "30" -> combined "2330". Is "2330" a palindrome? No. Correct.

    14:59:
    HH = 14 -> "14", MM = "59" -> "1459". Palindrome? No. Correct.

    So the rule is:
    - Form string: str(HH) + (MM as two digits, but if HH==0 then str(int(MM)))

    Wait, that's not right either. Let me reconsider.

    "ignore all leading zeroes in HH" -> str(h)  (h as integer, no leading zeros)
    "If HH is zero then ignore all leading zeroes in MM" -> if h == 0: str(m) else "%02d" % m

    But what about the combined string? Let me re-check:

    For HH=0, MM=0: str(0) + str(0) = "00"? No...

    Hmm, I think the approach is:
    - The time string without colon and without leading zeros based on rules
    - For HH != 0: remove leading zeros from HH, keep MM as-is (2 digits)
      e.g., 05:50 -> "550", 15:51 -> "1551"
    - For HH == 0: remove leading zeros from HH (becomes empty or "0"?),
      and remove leading zeros from MM

    Actually I think "ignore leading zeroes in HH" means when HH is "05",
    ignore the leading "0" so it becomes "5". When HH is "00", both are leading zeros
    so it becomes... empty? Or just "0"?

    Let me think about it differently. "HH" = the hour number. "Ignore leading zeroes"
    means represent it without leading zeros. So 0 -> "0", 5 -> "5", 15 -> "15", 23 -> "23".

    Then if HH is zero, also represent MM without leading zeros: 0 -> "0", 5 -> "5", etc.
    Otherwise MM keeps its two-digit format: 0 -> "00", 5 -> "05", etc.

    So the combined string (ignoring the colon) is:
    - If h == 0: str(h) + str(m) = "0" + str(m)
      Wait, but that gives "00" for 00:00, "01" for 00:01...
      "0" is NOT a palindrome... "00" IS. "01" is NOT.

    But sample says next palindrome after 00:00 is 00:01.

    Hmm, maybe when HH is zero, we drop HH entirely?
    "If HH is zero then ignore all leading zeroes in MM"
    So when HH = 0: the string is just MM with leading zeros removed.
    00:00 -> "0" (palindrome)
    00:01 -> "1" (palindrome)
    00:10 -> "10" (not palindrome)
    00:11 -> "11" (palindrome)

    And when HH != 0:
    The string is str(h) + "%02d" % m
    05:50 -> "550" (palindrome? "550" reversed is "055" -> no)
    05:50 -> "5" + "50" = "550" -> not palindrome

    Hmm wait, let me reconsider. Maybe with colon:

    The time is displayed as "HH:MM". Palindrome means reads same left-to-right and right-to-left.
    With the colon included? Let me check:

    23:32 -> "23:32" reversed is "23:32" -> YES palindrome!
    15:51 -> "15:51" reversed is "15:51" -> YES!

    But "ignore leading zeroes in HH":
    05:50 -> ignore leading zero -> "5:50" reversed is "05:5" -> hmm that doesn't work well.

    Let me try without colon:
    23:32 -> "2332" reversed "2332" -> palindrome
    15:51 -> "1551" reversed "1551" -> palindrome

    With leading zero removal (no colon):
    05:50 -> "550" reversed "055" -> not palindrome
    5:05 -> "505" reversed "505" -> palindrome! So 05:05 would be palindromic.

    For HH=0:
    00:00 -> HH is zero, ignore leading zeros in MM -> just "0" -> palindrome
    00:01 -> just "1" -> palindrome

    This matches the sample! Let me verify all samples again:

    Sample 1: 00:00. Current time is palindromic (string "0").
    Next: 00:01 -> string "1" -> palindrome. Output 00:01. MATCHES.

    Sample 2: 23:30. String "2330", not palindrome.
    23:31 -> "2331" no, 23:32 -> "2332" yes! Output 23:32. MATCHES.

    Sample 3: 14:59. String "1459" not palindrome.
    15:00 -> "1500" no, ... 15:51 -> "1551" yes! Output 15:51. MATCHES.
    """
    if h == 0:
        s = str(m)
    else:
        s = str(h) + "%02d" % m
    return s == s[::-1]

def next_time(h, m):
    """Advance time by 1 minute."""
    m += 1
    if m >= 60:
        m = 0
        h += 1
        if h >= 24:
            h = 0
    return h, m

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    results = []
    for _ in range(n):
        time_str = input_data[idx]; idx += 1
        parts = time_str.split(':')
        h = int(parts[0])
        m = int(parts[1])
        # Advance at least one minute
        h, m = next_time(h, m)
        while not is_palindromic_time(h, m):
            h, m = next_time(h, m)
        results.append("%02d:%02d" % (h, m))
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
