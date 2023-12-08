from __future__ import annotations
from dataclasses import dataclass
import functools
import io
import itertools
import math
import os

EXAMPLE_INPUT = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
EXAMPLE_OUTPUT = 6


@dataclass(frozen=True)
class Loop:
    start: int
    length: int

    def combine(self, other: Loop) -> Loop:
        if self.length < other.length:
            return other.combine(self)
        k = 0
        while (self.start + k * self.length - other.start) % other.length != 0:
            k += 1
        return Loop(self.start + k * self.length, math.lcm(self.length, other.length))

assert Loop(1, 1).combine(Loop(2, 5)) == Loop(2, 5)
assert Loop(2, 5).combine(Loop(4, 7)) == Loop(32, 35)


def loop_shape(dirs: str, network: dict[str, dict[str, str]], loc: str) -> Loop:
    dirs_it = itertools.cycle(dirs)
    seen: dict[str, int] = {}
    count = 0
    while loc not in seen:
        if loc.endswith("Z"):
            seen[loc] = count
        loc = network[loc][next(dirs_it)]
        count += 1
    start = seen[loc]
    return Loop(start, count - start)


def solve(reader: io.TextIOBase) -> int:
    dirs = next(reader).strip()
    next(reader)
    network = {line[0:3]: {"L": line[7:10], "R": line[12:15]} for line in reader}
    locs = [loc for loc in network if loc.endswith("A")]
    shapes = [loop_shape(dirs, network, loc) for loc in locs]
    shape = functools.reduce(Loop.combine, shapes, Loop(1, 1))
    return shape.start


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
