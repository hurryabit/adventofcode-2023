import io
import os

EXAMPLE_INPUT = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
EXAMPLE_OUTPUT = 952408144115

DELTA = {
    "0": (1, 0),
    "3": (0, 1),
    "2": (-1, 0),
    "1": (0, -1),
}


def solve(reader: io.TextIOBase) -> int:
    (x0, y0) = (0, 0)
    area = 0
    perimeter = 0
    for line in reader:
        _, _, instr = line.split()
        l = int(instr[2:7], 16)
        (dx, dy) = DELTA[instr[7]]
        (x1, y1) = (x0 + l * dx, y0 + l * dy)
        area += x0 * y1 - x1 * y0
        perimeter += l
        (x0, y0) = (x1, y1)
    return (abs(area) + perimeter + 2) // 2


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
