def parse_number(token: str) -> bool:
    state = 0  # See JFLAP NFA diagram for state numbers

    for c in token:
        match state:
            case 0:  # Initial state
                if '1' <= c <= '9':
                    state = 1
                elif c == ".":
                    state = 2
                elif c == '0':
                    state = 3
                else:
                    return False
            case 1:  # Decimal state
                if '0' <= c <= '9':
                    state = 1
                elif c == "_":
                    state = 8
                elif c == ".":
                    state = 11
                elif c in ["e", "E"]:
                    state = 12
                else:
                    return False
            case 2:  # Point transition state
                if '0' <= c <= '9':
                    state = 11
                else:
                    return False
            case 3:  # Octal/hexadecimal transition & "0" state
                if c in ['o', 'O']:
                    state = 4
                elif c in ['x', 'X']:
                    state = 6
                elif c == ".":
                    state = 11
                elif c in ['e', 'E']:
                    state = 12
                elif '0' <= c <= '9':
                    state = 15
                else:
                    return False
            case 4 | 5:  # Octal state
                if '0' <= c <= '7':
                    state = 5
                elif c == "_":
                    state = 9
                else:
                    return False
            case 6 | 7:  # Hexadecimal state
                if '0' <= c <= '9' or 'A' <= c <= 'F' or 'a' <= c <= 'f':
                    state = 7
                elif c == "_":
                    state = 10
                else:
                    return False
            case 8:  # Decimal underscore state
                if '0' <= c <= '9':
                    state = 1
                else:
                    return False
            case 9:  # Octal underscore state
                if '0' <= c <= '7':
                    state = 5
                else:
                    return False
            case 10:  # Hexadecimal underscore state
                if '0' <= c <= '9' or 'A' <= c <= 'F' or 'a' <= c <= 'f':
                    state = 7
                else:
                    return False
            case 11:  # Fractional state
                if '0' <= c <= '9':
                    state = 11
                elif c in ['e', 'E']:
                    state = 12
                elif c == "_":
                    state = 16
                else:
                    return False
            case 12:  # Exponent transition state
                if '0' <= c <= '9':
                    state = 13
                elif c in ['-', '+']:
                    state = 14
                else:
                    return False
            case 13:  # Exponent state
                if '0' <= c <= '9':
                    state = 13
                elif c == "_":
                    state = 14
                else:
                    return False
            case 14:  # Exponent underscore/sign state
                if '0' <= c <= '9':
                    state = 13
                else:
                    return False
            case 15:  # Point state
                if '0' <= c <= '9':
                    state = 15
                elif c == ".":
                    state = 11
                elif c == "_":
                    state = 17
                else:
                    return False
            case 16:  # Fractional underscore state
                if '0' <= c <= '9':
                    state = 11
                else:
                    return False
            case 17:  # Point underscore state
                if '0' <= c <= '9':
                    state = 15
                else:
                    return False
    
    # End of string; return true if state is an accept state
    if state in [1, 3, 5, 7, 11, 13]:
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

    # Floating point literal examples from Python documentation
    ("3.14", True),
    ("10.", True),
    (".001", True),
    ("1e100", True),
    ("3.14e-10", True),
    ("0e0", True),
    ("3.14_15_93", True),
    
    # Decimal cases
    ("", False),
    ("0", True),
    ("00", False),
    ("1_0_0", True),
    ("_", False),
    ("1__0", False),
    ("_0", False),

    # Octal cases
    ("2o0", False),
    ("0o", False),
    ("0o0", True),
    ("0o0_", False),
    ("0o_0", True),
    ("0og", False),
    ("0o8", False),

    # Hexadecimal cases
    ("2x0", False),
    ("0x", False),
    ("0x0", True),
    ("0x0_", False),
    ("0x_0", True),
    ("0xg", False),

    # Floating point cases
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
    ("001", False),
    ("3_14.15", True)
]


def main():
    # Print options and get input from user
    print("1) Run tests")
    print("2) Enter numbers manually")
    option = input("Enter an option: ")
    match option:
        case "1":
            # Verify test data
            for string, expected in TEST_DATA:
                try:
                    eval(string)
                except:
                    if expected and string != "":
                        print(f"Invalid number in test data: {string}")
                        exit(1)
            
            # Run tests
            for string, expected in TEST_DATA:
                result = parse_number(string)
                print(f"{'PASS' if result == expected else '***FAIL***'}: {string} (Result: {result}, Expected: {expected})")
        case "2":
            print("Press Ctrl + C to exit.")
            while True:
                try:
                    input_num = input("Enter a number: ")
                    result = parse_number(input_num)
                    print(f"{input_num} is {'a' if result else 'not a'} valid number.")
                    print()
                except KeyboardInterrupt:
                    break
        case _:
            print("Invalid option; exiting...")
            exit(1)


if __name__ == "__main__":
    main()
