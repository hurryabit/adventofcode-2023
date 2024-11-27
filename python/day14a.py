import io
import os

EXAMPLE_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
EXAMPLE_OUTPUT = 136


def solve(reader: io.TextIOBase) -> int:
    result: int = 0
    num_rocks = 0
    frees: list[int] = []
    row = 0
    for row, line in enumerate(reader):
        line = line.rstrip()
        if row == 0:
            frees = [0] * len(line)
        for col, cell in enumerate(line):
            match cell:
                case "O":
                    result -= frees[col]
                    num_rocks += 1
                    frees[col] += 1
                case "#":
                    frees[col] = row + 1
                case _:
                    pass
    result += num_rocks * (row + 1)
    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
