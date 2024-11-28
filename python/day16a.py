from __future__ import annotations
import io
import os
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

EXAMPLE_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
EXAMPLE_OUTPUT = 46


def dfs[T](init: T, succs: Callable[[T], list[T]]) -> set[T]:
    seen = {init}
    stack = [init]
    while stack:
        node = stack.pop()
        for succ in succs(node):
            if succ not in seen:
                seen.add(succ)
                stack.append(succ)
    return seen


@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def __add__(self, other: Pos) -> Pos:
        return Pos(self.row + other.row, self.col + other.col)


class Map:
    data: list[str]

    def __init__(self, data: list[str]) -> None:
        self.data = data

    def __contains__(self, pos: Pos) -> bool:
        return 0 <= pos.row < len(self.data) and 0 <= pos.col < len(self.data[pos.row])

    def __getitem__(self, pos: Pos) -> str:
        return self.data[pos.row][pos.col]


DELTAS = (Pos(0, 1), Pos(-1, 0), Pos(0, -1), Pos(1, 0))


class Dir(IntEnum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @property
    def delta(self) -> Pos:
        return DELTAS[self]


@dataclass(frozen=True)
class Beam:
    pos: Pos
    dir: Dir


EFFECTS = {
    ".": [[Dir.RIGHT], [Dir.UP], [Dir.LEFT], [Dir.DOWN]],
    "/": [[Dir.UP], [Dir.RIGHT], [Dir.DOWN], [Dir.LEFT]],
    "\\": [[Dir.DOWN], [Dir.LEFT], [Dir.UP], [Dir.RIGHT]],
    "-": [[Dir.RIGHT], [Dir.RIGHT, Dir.LEFT], [Dir.LEFT], [Dir.RIGHT, Dir.LEFT]],
    "|": [[Dir.UP, Dir.DOWN], [Dir.UP], [Dir.UP, Dir.DOWN], [Dir.DOWN]],
}


def solve(reader: io.TextIOBase) -> int:
    map = Map([line.rstrip() for line in reader])

    def succs(beam: Beam) -> list[Beam]:
        return [
            next
            for dir in EFFECTS[map[beam.pos]][beam.dir]
            if (next := Beam(beam.pos + dir.delta, dir)).pos in map
        ]

    beams = dfs(Beam(Pos(0, 0), Dir.RIGHT), succs)
    return len({beam.pos for beam in beams})


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
