from __future__ import annotations
import io
import os
from collections.abc import Iterable, Iterator
from typing import NamedTuple, NewType

EXAMPLE_INPUT = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
EXAMPLE_OUTPUT = 5


class Point2D(NamedTuple):
    x: int
    y: int


class Span2D(Iterable[Point2D]):
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def __init__(self, start: Point2D, end: Point2D) -> None:
        self.xmin, self.xmax = min(start.x, end.x), max(start.x, end.x)
        self.ymin, self.ymax = min(start.y, end.y), max(start.y, end.y)

    def __iter__(self) -> Iterator[Point2D]:
        for x in range(self.xmin, self.xmax + 1):
            for y in range(self.ymin, self.ymax + 1):
                yield Point2D(x, y)


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def parse(input: str) -> Point3D:
        [x, y, z] = input.split(",")
        return Point3D(int(x), int(y), int(z))

    def proj_xy(self) -> Point2D:
        return Point2D(self.x, self.y)


Id = NewType("Id", int)


class Brick(NamedTuple):
    id: Id
    start: Point3D
    end: Point3D

    @property
    def zmin(self) -> int:
        return min(self.start.z, self.end.z)

    @property
    def zmax(self) -> int:
        return max(self.start.z, self.end.z)

    @staticmethod
    def parse(id: int, input: str) -> Brick:
        [start, end] = input.split("~")
        return Brick(Id(id), Point3D.parse(start), Point3D.parse(end))


def solve(reader: io.TextIOBase) -> int:
    bricks = [Brick.parse(id, line.rstrip()) for id, line in enumerate(reader)]
    bricks.sort(key=lambda b: b.zmin)

    required = set[Id]()
    heights = dict[Point2D, tuple[int, Brick]]()

    for brick in bricks:
        span = Span2D(brick.start.proj_xy(), brick.end.proj_xy())
        max_height = max((heights[p][0] for p in span if p in heights), default=0)
        support = {
            hb[1].id
            for p in span
            if p in heights and (hb := heights[p])[0] == max_height
        }
        if len(support) == 1:
            required |= support
        new_height = max_height + brick.zmax - brick.zmin + 1
        heights |= {p: (new_height, brick) for p in span}

    return len(bricks) - len(required)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
