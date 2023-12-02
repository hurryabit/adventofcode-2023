import io

DAY = 1
EXAMPLE_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
EXAMPLE_OUTPUT = 142


def solve(reader: io.TextIOBase) -> int:
    result = 0
    for line in reader:
        digits = list(c for c in line if c.isdigit())
        result += 10 * int(digits[0]) + int(digits[-1])
    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY:02}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
