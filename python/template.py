import io
import os

EXAMPLE_INPUT = """"""
EXAMPLE_OUTPUT = 0


def solve(reader: io.TextIOBase) -> int:
    return 0


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
