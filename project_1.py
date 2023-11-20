import sys

def parse_number(token: str) -> bool:
    state = 0  # See JFLAP NFA diagram for state numbers

    for c in token:
        match state:
            case 0:  # Initial state
                if '1' <= c <= '9':
                    state = 1
                elif c == '0':
                    state = 3
                elif c == '.':
                    state = 1
                else:
                    return False
            case 1:  # Decimal state
                if '0' <= c <= '9':
                    state = 1
                elif c == ".":
                    state = 4
                elif c in ['e', 'E']:
                    state = 5
                elif c == "_":
                    state = 8
                else:
                    return False
            case 2 | 4 | 5:  # Accept states
                return True
            case 3:  # Octal/hexadecimal transition state
                if c in ['o', 'O']:
                    state = 6
                elif c in ['x', 'X']:
                    state = 6
                elif c == ".":
                    state = 4
                else:
                    return False
            case 6 | 7:  # Octal/hexadecimal states
                if '0' <= c <= '7' or 'A' <= c <= 'F' or 'a' <= c <= 'f':
                    state = 7
                elif c == "_":
                    state = 9
                else:
                    return False
            case 8:  # Decimal underscore state
                if '0' <= c <= '9':
                    state = 1
                else:
                    return False
            case 9:  # Octal/hexadecimal underscore state
                if '0' <= c <= '7' or 'A' <= c <= 'F' or 'a' <= c <= 'f':
                    state = 7
                else:
                    return False

    # Epsilon transition to accept states
    if state in [1, 4, 5, 7]:
        return True
    else:
        return False

# (string, expected)
TEST_DATA = [
    # Integer literal examples from Python documentation
    ("7", True),
    ("2147483647", True),
    ("0o177", True),
    ("3", True),
    ("79228162514264337593543950336", True),
    ("0o377", True),
    ("0xdeadbeef", True),
    ("100_000_000_000", True),

    # Floating-point literal examples
    ("3.14", True),
    ("0.5", True),
    (".5", True),
    ("0.", True),
    ("000.", True),
    ("1.23e-4", True),
    ("1e10", True),
    ("1e1_0", True),
    ("1e1__0", False),
    ("1_0e10", True),
    ("1_0e-10", True),
    ("1_0e+10", True),
    ("1_0e+1_0", True),
    ("1.00e+10", True),
    ("1.00e+", False),
    ("1.00e", False),

    # Other cases
    ("_", False),
    ("1__0", False),
    ("1_0", True),
    ("_0", False),

    ("2x0", False),
    ("0x", False),
    ("0x0", True),
    ("0x0_", False),
    ("0x_0", True),
    ("0xg", False),
    ("00x00", False),

    ("2o0", False),
    ("0o", False),
    ("0o0", True),
    ("0o0_", False),
    ("0o_0", True),
    ("0og", False),
    ("0o8", False),
]

def main():
    if sys.argv[-1] != "test":  # Test mode
        # Verify test data
        for string, expected in TEST_DATA:
            try:
                eval(string)
            except:
                if expected:
                    print(f"Invalid number in test data: {string}")
                    exit(1)
        
        # Run tests
        for string, expected in TEST_DATA:
            print(f"{string}: {'PASS' if parse_number(string) == expected else 'FAIL'}")
    else:  # Manual input mode
        while True:
            print("Press Ctrl + C to exit.")
            try:
                input_num = input("Enter a number: ")
                result = parse_number(input_num)
                print(f"{input_num} is {'a' if result else 'not a'} valid number.")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
