from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import io
import os
from typing import Callable

EXAMPLE_INPUT = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
EXAMPLE_OUTPUT = 10


class Dir(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def __add__(self, other: Point | Dir) -> Point:
        if isinstance(other, Point):
            return Point(self.row + other.row, self.col + other.col)
        if isinstance(other, Dir):
            return Point(self.row + other.value[0], self.col + other.value[1])
        raise TypeError(f"Cannot add Point + {type(other)}")

    def __rmul__(self, s: int) -> Point:
        return Point(s * self.row, s * self.col)


@dataclass
class Map:
    data: list[list[int]]

    @staticmethod
    def sized(m: int, n: int) -> Map:
        return Map([[0 for _ in range(n)] for _ in range(m)])

    def __contains__(self, p: Point) -> bool:
        return 0 <= p.row < len(self.data) and 0 <= p.col < len(self.data[p.row])

    def __getitem__(self, p: Point) -> int:
        return self.data[p.row][p.col]

    def __setitem__(self, p: Point, value: int):
        self.data[p.row][p.col] = value

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.data)

    def search(self, start: Point, pred: Callable[[Point, int], bool]) -> set[Point]:
        queue = [start]
        visited = set([start])
        while len(queue) > 0:
            p = queue.pop()
            for dir in Dir:
                q = p + dir
                if q in self and pred(q, self[q]) and q not in visited:
                    queue.append(q)
                    visited.add(q)
        return visited


ZOOMED = {
    "|": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
    "-": [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
    "L": [[0, 1, 0], [0, 1, 1], [0, 0, 0]],
    "J": [[0, 1, 0], [1, 1, 0], [0, 0, 0]],
    "7": [[0, 0, 0], [1, 1, 0], [0, 1, 0]],
    "F": [[0, 0, 0], [0, 1, 1], [0, 1, 0]],
    ".": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    "S": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
}


def zoom(input: list[str]) -> tuple[Map, Point]:
    m, n = len(input), len(input[0])
    start = Point(-1, -1)
    map = Map.sized(3 * m, 3 * n)
    for i in range(m):
        for j in range(n):
            cell = input[i][j]
            point = 3 * Point(i, j)
            if cell == "S":
                start = point + Point(1, 1)
            zoomed = ZOOMED[cell]
            for di in range(3):
                for dj in range(3):
                    map[point + Point(di, dj)] = zoomed[di][dj]
    for dir in Dir:
        if start + dir + dir in map and map[start + dir + dir] == 1:
            map[start + dir] = 1
    return (map, start)


def solve(reader: io.TextIOBase) -> int:
    input = [line.strip() for line in reader]
    m, n = len(input), len(input[0])
    (map, start) = zoom(input)
    path = map.search(start, lambda _, v: v == 1)
    outer = map.search(Point(0, 0), lambda p, _: p not in path)
    count = 0
    for i in range(m):
        for j in range(n):
            p = 3 * Point(i, j) + Point(1, 1)
            if p not in path and p not in outer:
                count += 1
    return count


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
