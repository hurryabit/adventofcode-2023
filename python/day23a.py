from __future__ import annotations
import io
import math
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

sys.setrecursionlimit(10000)

EXAMPLE_INPUT = r"""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
EXAMPLE_OUTPUT = 94


def longest_walk[T](start: T, edges: Callable[[T], list[T]], target: T) -> int:
    seen = set[T]()

    def go(node: T) -> int:
        if node == target:
            return 0
        seen.add(node)
        result = 1 + max(
            (go(dest) for dest in edges(node) if dest not in seen), default=-math.inf
        )
        seen.remove(node)
        return result  # type: ignore

    return go(start)


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

    def bottom_right(self) -> Pos:
        return Pos(len(self.data) - 1, len(self.data[0]) - 1)


DELTAS = (Pos(0, 1), Pos(-1, 0), Pos(0, -1), Pos(1, 0))


class Dir(IntEnum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @property
    def delta(self) -> Pos:
        return DELTAS[self]


SLOPES = {
    ">": Dir.RIGHT,
    "^": Dir.UP,
    "<": Dir.LEFT,
    "v": Dir.DOWN,
}


def solve(reader: io.TextIOBase) -> int:
    map = Map([line.rstrip() for line in reader])

    def edges(pos: Pos) -> list[Pos]:
        cell = map[pos]
        dirs = [SLOPES[cell]] if cell in SLOPES else iter(Dir)
        return [
            dest
            for dir in dirs
            if (dest := pos + dir.delta) in map and map[dest] != "#"
        ]

    return longest_walk(Pos(0, 1), edges, map.bottom_right() + Dir.LEFT.delta)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
