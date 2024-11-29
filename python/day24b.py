# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
from __future__ import annotations
import io
import re
import os
import z3  # type: ignore
from dataclasses import dataclass
from fractions import Fraction

EXAMPLE_INPUT = """19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
EXAMPLE_RANGE = (Fraction(7), Fraction(27))
EXAMPLE_OUTPUT = 47


POINT3D_RE = re.compile(r"(-?\d+),\s*(-?\d+),\s*(-?\d+)")


@dataclass
class Point3D:
    x: Fraction
    y: Fraction
    z: Fraction

    @staticmethod
    def parse(input: str) -> Point3D:
        m = POINT3D_RE.fullmatch(input)
        assert m is not None, f"bad input: «{input}»"
        return Point3D(Fraction(m[1]), Fraction(m[2]), Fraction(m[3]))


@dataclass
class Ray3D:
    pos: Point3D
    dir: Point3D

    @staticmethod
    def parse(input: str) -> Ray3D:
        [pos, dir] = input.split("@")
        return Ray3D(Point3D.parse(pos.strip()), Point3D.parse(dir.strip()))


def solve(reader: io.TextIOBase, range: tuple[Fraction, Fraction]) -> int:
    rays = [Ray3D.parse(line) for line in reader]
    [px, py, pz, dx, dy, dz] = vars = [
        z3.Int(name) for name in ["px", "py", "pz", "dx", "dy", "dz"]
    ]
    solver = z3.Solver()
    for i, ray in enumerate(rays):
        ti = z3.Int(f"t{i}")
        solver.add(
            ray.pos.x + ray.dir.x * ti == px + ti * dx,
            ray.pos.y + ray.dir.y * ti == py + ti * dy,
            ray.pos.z + ray.dir.z * ti == pz + ti * dz,
        )
    assert solver.check() == z3.sat
    m = solver.model()
    return sum(m[v].as_long() for v in vars[:3])  # type: ignore


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
