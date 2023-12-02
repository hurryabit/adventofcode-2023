import io

DAY = 1
EXAMPLE_INPUT = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
EXAMPLE_OUTPUT = 281


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
} | {str(i): i for i in range(10)}


def find_first_digit(line: str) -> int:
    for i in range(len(line)):
        for name, value in DIGITS.items():
            if line.startswith(name, i):
                return value
    raise ValueError("line does not contain digit")


def find_last_digit(line: str) -> int:
    for i in range(len(line), 0, -1):
        for name, value in DIGITS.items():
            if line.endswith(name, 0, i):
                return value
    raise ValueError("line does not contain digit")


def solve(reader: io.TextIOBase) -> int:
    result = 0
    for line in reader:
        result += 10 * find_first_digit(line) + find_last_digit(line)
    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY:02}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
