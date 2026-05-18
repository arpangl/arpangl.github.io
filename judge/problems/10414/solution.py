import sys

def bangla(n):
    """Convert a non-negative integer to Bangla number text."""
    if n == 0:
        return "0"

    parts = []

    # Handle kuti (10^7) - recursive for the upper part
    if n >= 10**7:
        upper = n // 10**7
        parts.append(bangla(upper))
        parts.append("kuti")
        n = n % 10**7

    # Handle lakh (10^5)
    if n >= 10**5:
        parts.append(str(n // 10**5))
        parts.append("lakh")
        n = n % 10**5

    # Handle hajar (10^3)
    if n >= 10**3:
        parts.append(str(n // 10**3))
        parts.append("hajar")
        n = n % 10**3

    # Handle shata (10^2)
    if n >= 10**2:
        parts.append(str(n // 10**2))
        parts.append("shata")
        n = n % 10**2

    # Remainder
    if n > 0:
        parts.append(str(n))

    return " ".join(parts)


def main():
    case_num = 1
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        n = int(line)
        result = bangla(n)
        print(f"{case_num:>4}. {result}")
        case_num += 1


if __name__ == "__main__":
    main()
