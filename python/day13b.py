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


def flipped_at(pattern: list[str], i: int, j: int) -> list[str]:
    row = pattern[i]
    flipped_row = row[:j] + ("#" if row[j] == "." else ".") + row[j + 1 :]
    return pattern[:i] + [flipped_row] + pattern[i + 1 :]


def analyse_vertically(pattern: list[str]) -> set[int]:
    result = set()
    for i in range(1, len(pattern)):
        if all(
            pattern[i - 1 - j] == pattern[i + j]
            for j in range(min(i, len(pattern) - i))
        ):
            result.add(i)
    return result


def analyse_both(pattern: list[str]) -> set[int]:
    vs = analyse_vertically(pattern)
    hs = analyse_vertically(["".join(row) for row in zip(*pattern)])
    return {100 * v for v in vs} | hs


def analyse(pattern: list[str]) -> int:
    old = analyse_both(pattern).pop()
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            flipped_pattern = flipped_at(pattern, i, j)
            res = analyse_both(flipped_pattern) - {old}
            if len(res) > 0:
                return res.pop()
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
