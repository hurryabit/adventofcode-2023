import io
import itertools
import os

EXAMPLE_INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
EXAMPLE_OUTPUT = 114


def next_number(numbers: list[int]) -> int:
    result = 0
    while not all(number == 0 for number in numbers):
        result += numbers[-1]
        numbers = [y - x for (x, y) in itertools.pairwise(numbers)]
    return result


def solve(reader: io.TextIOBase) -> int:
    return sum(next_number([int(n) for n in line.split()]) for line in reader)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
