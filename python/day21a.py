from __future__ import annotations
import io
import os
from dataclasses import dataclass
from enum import IntEnum

EXAMPLE_INPUT = r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
EXAMPLE_STEPS = 6
EXAMPLE_OUTPUT = 16


@dataclass(frozen=True, order=True)
class Pos:
    row: int
    col: int

    def __add__(self, other: Pos) -> Pos:
        return Pos(self.row + other.row, self.col + other.col)


class Map:
    data: list[str]

    def __init__(self, data: list[str]) -> None:
        self.data = data

    def dims(self) -> tuple[int, int]:
        return (len(self.data), len(self.data[0]))

    def __contains__(self, pos: Pos) -> bool:
        return 0 <= pos.row < len(self.data) and 0 <= pos.col < len(self.data[pos.row])

    def __getitem__(self, pos: Pos) -> str:
        return self.data[pos.row][pos.col]

    def index(self, cell: str) -> Pos:
        assert len(cell) == 1
        for row, line in enumerate(self.data):
            col = line.find(cell)
            if col >= 0:
                return Pos(row, col)
        else:
            raise ValueError(f"{cell!r} not found")


class Dir(IntEnum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @property
    def delta(self) -> Pos:
        return DELTAS[self]


DELTAS = (Pos(0, 1), Pos(-1, 0), Pos(0, -1), Pos(1, 0))


def solve(reader: io.TextIOBase, steps: int) -> int:
    map = Map([line.rstrip() for line in reader])
    start = map.index("S")
    plots = {start}
    for _ in range(steps):
        plots = {
            pos
            for plot in plots
            for dir in Dir
            if (pos := plot + dir.delta) in map and map[pos] != "#"
        }
    return len(plots)


assert solve(io.StringIO(EXAMPLE_INPUT), EXAMPLE_STEPS) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file, 64)
        print(solution)


if __name__ == "__main__":
    main()
