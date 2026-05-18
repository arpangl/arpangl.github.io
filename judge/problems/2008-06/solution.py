import sys
import math

class Parser:
    def __init__(self, s):
        self.s = s
        self.pos = 0
        self.error = False

    def peek(self):
        if self.pos < len(self.s):
            return self.s[self.pos]
        return None

    def consume(self):
        ch = self.s[self.pos]
        self.pos += 1
        return ch

    def parse_E(self):
        """E -> T ((+|-) T)*   (left-associative addition/subtraction)"""
        val = self.parse_T()
        if self.error:
            return 0
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_T()
            if self.error:
                return 0
            if op == '+':
                val = val + right
            else:
                val = val - right
        return val

    def parse_T(self):
        """T -> M ((*|/) M)*   (left-associative multiplication/division)"""
        val = self.parse_M()
        if self.error:
            return 0
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_M()
            if self.error:
                return 0
            if op == '*':
                val = val * right
            else:
                if right == 0:
                    self.error = True
                    return 0
                # C-style integer division: truncate toward zero
                val = int(val / right)
        return val

    def parse_M(self):
        """M -> F (% F)*   (left-associative modulo, higher priority than * /)"""
        val = self.parse_F()
        if self.error:
            return 0
        while self.peek() == '%':
            self.consume()
            right = self.parse_F()
            if self.error:
                return 0
            if right == 0:
                self.error = True
                return 0
            # C-style modulo: sign follows dividend
            val = int(math.fmod(val, right))
        return val

    def parse_F(self):
        """F -> ( E ) | - F | + F | N"""
        ch = self.peek()
        if ch == '(':
            self.consume()  # consume '('
            val = self.parse_E()
            if self.error:
                return 0
            if self.peek() != ')':
                self.error = True
                return 0
            self.consume()  # consume ')'
            return val
        elif ch == '-':
            self.consume()
            val = self.parse_F()
            return -val
        elif ch == '+':
            self.consume()
            val = self.parse_F()
            return val
        elif ch is not None and ch.isdigit():
            return self.parse_N()
        else:
            self.error = True
            return 0

    def parse_N(self):
        """N -> D | DN (one or more digits)"""
        if self.peek() is None or not self.peek().isdigit():
            self.error = True
            return 0
        num_str = ''
        while self.peek() is not None and self.peek().isdigit():
            num_str += self.consume()
        return int(num_str)

    def parse(self):
        val = self.parse_E()
        if self.error or self.pos != len(self.s):
            return None
        return val


def solve():
    case_num = 0
    for line in sys.stdin:
        line = line.rstrip('\n').rstrip('\r').rstrip()

        case_num += 1
        parser = Parser(line)
        result = parser.parse()
        if result is None:
            print(f"case {case_num}:")
            print("syntactically incorrect")
            print()
        else:
            print(f"case {case_num}:")
            print(result)
            print()


if __name__ == '__main__':
    solve()
