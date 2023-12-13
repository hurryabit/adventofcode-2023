import io
import os

EXAMPLE_INPUT = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
EXAMPLE_OUTPUT = 400


def analyse_vertically(pattern: list[str]) -> int | None:
    for i in range(1, len(pattern)):
        defects = 0
        for j in range(min(i, len(pattern) - i)):
            upper = pattern[i - 1 - j]
            lower = pattern[i + j]
            defects += sum(1 for k in range(len(upper)) if upper[k] != lower[k])
        if defects == 1:
            return i
    return None


def analyse(pattern: list[str]) -> int:
    v = analyse_vertically(pattern)
    if v is not None:
        return 100 * v
    h = analyse_vertically(["".join(row) for row in zip(*pattern)])
    if h is not None:
        return h
    raise ValueError(f"analyse(pattern={pattern}) failed")


def solve(reader: io.TextIOBase) -> int:
    result = 0
    pattern: list[str] = []
    for line in reader:
        line = line.rstrip()
        if len(line) == 0:
            result += analyse(pattern)
            pattern = []
        else:
            pattern.append(line)
    result += analyse(pattern)
    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
