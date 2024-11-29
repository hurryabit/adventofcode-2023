from __future__ import annotations
import io
import re
import os
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

EXAMPLE_INPUT = """19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
EXAMPLE_RANGE = (Fraction(7), Fraction(27))
EXAMPLE_OUTPUT = 2


@dataclass
class Point2D:
    x: Fraction
    y: Fraction

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        return Point2D(self.x - other.x, self.y - other.y)

    def __rmul__(self, scale: Fraction) -> Point2D:
        return Point2D(scale * self.x, scale * self.y)

    def __str__(self) -> str:
        return f"({self.x.numerator}/{self.x.denominator}, {self.y.numerator}/{self.y.denominator})"


def det(a: Point2D, b: Point2D) -> Fraction:
    return a.x * b.y - a.y * b.x


POINT3D_RE = re.compile(r"(-?\d+),\s*(-?\d+),\s*(-?\d+)")


@dataclass
class Point3D:
    x: Fraction
    y: Fraction
    z: Fraction

    def proj_xy(self) -> Point2D:
        return Point2D(self.x, self.y)

    @staticmethod
    def parse(input: str) -> Point3D:
        m = POINT3D_RE.fullmatch(input)
        assert m is not None, f"bad input: «{input}»"
        return Point3D(Fraction(m[1]), Fraction(m[2]), Fraction(m[3]))


@dataclass
class Ray2D:
    pos: Point2D
    dir: Point2D

    def __call__(self, at: Fraction) -> Point2D:
        return self.pos + at * self.dir

    def intersection(self, other: Ray2D) -> tuple[Point2D, Fraction, Fraction] | None:
        d = det(self.dir, other.dir)
        if d == 0:
            return None
        s = det(other.pos - self.pos, other.dir) / d
        t = -det(self.dir, other.pos - self.pos) / d
        return (self(s), s, t)

    def __str__(self) -> str:
        return f"{self.pos} + λ⋅{self.dir}"


assert Ray2D(
    Point2D(Fraction(19), Fraction(13)), Point2D(Fraction(-2), Fraction(1))
).intersection(
    Ray2D(Point2D(Fraction(18), Fraction(19)), Point2D(Fraction(-1), Fraction(-1)))
) == (
    Point2D(Fraction(43, 3), Fraction(46, 3)),
    Fraction(7, 3),
    Fraction(11, 3),
)


@dataclass
class Ray3D:
    pos: Point3D
    dir: Point3D

    def proj_xy(self) -> Ray2D:
        return Ray2D(self.pos.proj_xy(), self.dir.proj_xy())

    @staticmethod
    def parse(input: str) -> Ray3D:
        [pos, dir] = input.split("@")
        return Ray3D(Point3D.parse(pos.strip()), Point3D.parse(dir.strip()))


def solve(reader: io.TextIOBase, range: tuple[Fraction, Fraction]) -> int:
    rays = [Ray3D.parse(line).proj_xy() for line in reader]
    count = 0
    for r1, r2 in combinations(rays, 2):
        pst = r1.intersection(r2)
        if pst is None:
            continue
        (p, s, t) = pst
        if (
            0 <= s
            and 0 <= t
            and range[0] <= p.x <= range[1]
            and range[0] <= p.y <= range[1]
        ):
            count += 1
    return count


assert solve(io.StringIO(EXAMPLE_INPUT), EXAMPLE_RANGE) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(
            file, (Fraction(200_000_000_000_000), Fraction(400_000_000_000_000))
        )
        print(solution)


if __name__ == "__main__":
    main()
