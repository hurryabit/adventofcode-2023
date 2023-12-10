from __future__ import annotations
from enum import Enum
import io
import os

EXAMPLE_INPUT = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
EXAMPLE_OUTPUT = 8

Point = tuple[int, int]

class Dir(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def flip(self) -> Dir:
        return Dir((-self.value[0], -self.value[1]))

    def move(self, p: Point) -> Point:
        return (p[0] + self.value[0], p[1] + self.value[1])

PIPES = {
    "|": (Dir.NORTH, Dir.SOUTH),
    "-": (Dir.EAST, Dir.WEST),
    "L": (Dir.NORTH, Dir.EAST),
    "J": (Dir.NORTH, Dir.WEST),
    "7": (Dir.SOUTH, Dir.WEST),
    "F": (Dir.SOUTH, Dir.EAST),
}


def at(map: list[str], p) -> str:
    return map[p[0]][p[1]]


def solve(reader: io.TextIOBase) -> int:
    map = list(reader)
    start = (-1, -1)
    for i, row in enumerate(map):
        j = row.find("S")
        if j >= 0:
            start = (i, j)
            break
    prev, curr = start, (-1, -1)
    for dir in Dir:
        curr = dir.move(prev)
        char = at(map, curr)
        if char not in PIPES:
            continue
        if dir.flip() in PIPES[char]:
            break
    count = 1
    while curr != start:
        next = (-1, -1)
        for dir in PIPES[at(map, curr)]:
            next = dir.move(curr)
            if next != prev:
                break
        prev, curr = curr, next
        count += 1
    assert count % 2 == 0
    return count // 2


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
