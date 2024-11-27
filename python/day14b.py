from __future__ import annotations

import io
import os
from typing import Literal

EXAMPLE_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
EXAMPLE_OUTPUT = 64


class Matrix[T]:
    _size: int
    _data: list[T]
    _rota: Literal[0, 1, 2, 3]

    def __init__(self, data: list[list[T]]) -> None:
        self._size = len(data)
        self._data = []
        for line in data:
            assert len(line) == self._size
            self._data.extend(line)
        self._rota = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._size == other._size and (
            (self._rota == other._rota and self._data == other._data)  # type: ignore
            or self.data == other.data  # type: ignore
        )

    def clone(self) -> Matrix[T]:
        return Matrix(self.data)

    def index(self, pos: tuple[int, int]) -> int:
        n = self._size
        (r, c) = pos
        match self._rota:
            case 0:
                return self._size * r + c
            case 1:
                return self._size * (n - 1 - c) + r
            case 2:
                return self._size * (n - 1 - r) + (n - 1 - c)
            case 3:
                return self._size * c + (n - 1 - r)

    def __getitem__(self, pos: tuple[int, int]) -> T:
        return self._data[self.index(pos)]

    def __setitem__(self, pos: tuple[int, int], val: T) -> None:
        self._data[self.index(pos)] = val

    @property
    def size(self) -> int:
        return self._size

    @property
    def data(self) -> list[list[T]]:
        return [[self[r, c] for c in range(self.size)] for r in range(self.size)]

    def rotate_cw(self) -> None:
        self._rota = (self._rota + 1) % 4


m = Matrix([[1, 2], [3, 4]])
assert m.data == [[1, 2], [3, 4]]
m.rotate_cw()
assert m.data == [[3, 1], [4, 2]]
m.rotate_cw()
assert m.data == [[4, 3], [2, 1]]
m.rotate_cw()
assert m.data == [[2, 4], [1, 3]]
m.rotate_cw()
assert m.data == [[1, 2], [3, 4]]


def tilt(m: Matrix[str]) -> None:
    n = m.size
    for c in range(n):
        f = 0
        for r in range(n):
            match m[r, c]:
                case "O":
                    m[r, c] = "."
                    m[f, c] = "O"
                    f += 1
                case "#":
                    f = r + 1
                case _:
                    pass


def spin_cycle(m: Matrix[str]) -> None:
    for _ in range(4):
        tilt(m)
        m.rotate_cw()


def load(m: Matrix[str]) -> int:
    res = 0
    n = m.size
    for c in range(n):
        for r in range(n):
            if m[r, c] == "O":
                res += n - r
    return res


def solve(reader: io.TextIOBase) -> int:
    m1 = Matrix([list(line.rstrip()) for line in reader])
    m2 = m1.clone()

    spin_cycle(m1)
    spin_cycle(m2)
    spin_cycle(m2)

    i = 1
    while m1 != m2:
        spin_cycle(m1)
        spin_cycle(m2)
        spin_cycle(m2)
        i += 1

    for _ in range(1_000_000_000 % i):
        spin_cycle(m1)

    return load(m1)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
