import io
import itertools
import os

EXAMPLE_INPUT = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
EXAMPLE_OUTPUT = 2


def solve(reader: io.TextIOBase) -> int:
    dirs = itertools.cycle(next(reader).strip())
    next(reader)
    network = {line[0:3]: {"L": line[7:10], "R": line[12:15]} for line in reader}
    count = 0
    loc = "AAA"
    while loc != "ZZZ":
        dir = next(dirs)
        loc = network[loc][dir]
        count += 1
    return count


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
