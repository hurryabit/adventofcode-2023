import io
import math

DAY = 3
EXAMPLE_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
EXAMPLE_OUTPUT = 467835


def solve(reader: io.TextIOBase) -> int:
    schematic = [line.strip() for line in reader]
    height = len(schematic)
    width = len(schematic[0])

    def extract_num(line: str, i: int) -> int:
        n = len(line)
        start = next(
            filter(lambda j: j <= 0 or not line[j - 1].isdigit(), range(i, -1, -1))
        )
        end = next(
            filter(lambda j: j >= n or not line[j].isdigit(), range(i + 1, n + 1))
        )
        return int(line[start:end])

    result = 0

    for row in range(height):
        for col in range(width):
            if schematic[row][col] != "*":
                continue

            anchors = []
            for r in (row - 1, row, row + 1):
                if not (0 <= r < height):
                    continue
                if schematic[r][col].isdigit():
                    anchors.append((r, col))
                else:
                    for c in (col - 1, col + 1):
                        if not (0 <= c < height):
                            continue
                        if schematic[r][c].isdigit():
                            anchors.append((r, c))

            if len(anchors) == 2:
                result += math.prod(
                    extract_num(schematic[row], col) for (row, col) in anchors
                )

    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY:02}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
