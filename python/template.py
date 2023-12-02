import io

DAY = 100
EXAMPLE_INPUT = """"""
EXAMPLE_OUTPUT = 0


def solve(reader: io.TextIOBase) -> int:
    return 0


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY:02}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
