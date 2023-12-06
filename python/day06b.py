import io
import math
import os

EXAMPLE_INPUT = """Time:      7  15   30
Distance:  9  40  200"""
EXAMPLE_OUTPUT = 71503


def ways(time: int, dist: int) -> int:
    disc = math.sqrt(time * time / 4 - dist)
    return math.floor(time / 2 + disc) - math.ceil(time / 2 - disc) + 1


def solve(reader: io.TextIOBase) -> int:
    time = int("".join(reader.readline().split()[1:]))
    dist = int("".join(reader.readline().split()[1:]))
    return ways(time, dist)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
