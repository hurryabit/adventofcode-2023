import io

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
EXAMPLE_OUTPUT = 4361


def is_symbol(c: str) -> bool:
    return not c.isdigit() and c != "."

def solve(reader: io.TextIOBase) -> int:
    schematic = [line.strip() for line in reader]
    height = len(schematic)
    width = len(schematic[0])
    result = 0

    for row in range(height):
        col = 0
        while col < width:
            if not schematic[row][col].isdigit():
                col += 1
                continue
            start_col = col
            while col < width and schematic[row][col].isdigit():
                col += 1
            is_relevant = any(
                is_symbol(schematic[r][c])
                for r in range(row-1, row+2) if 0 <= r < height
                for c in range(start_col-1, col+1) if 0 <= c < width
            )
            if is_relevant:
                result += int(schematic[row][start_col:col])

    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY:02}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
