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
EXAMPLE_OUTPUT = 405


def analyse_vertically(pattern: list[str]) -> int:
    for i in range(1, len(pattern)):
        if all(
            pattern[i - 1 - j] == pattern[i + j]
            for j in range(min(i, len(pattern) - i))
        ):
            return i
    return -1


def analyse(pattern: list[str]) -> int:
    v = analyse_vertically(pattern)
    if v != -1:
        return 100 * v
    else:
        return analyse_vertically(["".join(row) for row in zip(*pattern)])


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
