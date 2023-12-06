import io
import math
import os

EXAMPLE_INPUT = """Time:      7  15   30
Distance:  9  40  200"""
EXAMPLE_OUTPUT = 288


def ways(time: int, dist: int) -> int:
    return sum(1 for hold in range(0, time+1) if hold * (time - hold) > dist)


def solve(reader: io.TextIOBase) -> int:
    times = reader.readline().split()[1:]
    dists = reader.readline().split()[1:]
    return math.prod(ways(int(time), int(dist)) for (time, dist) in zip(times, dists))


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
