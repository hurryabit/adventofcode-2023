from __future__ import annotations
import io
import os
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from heapq import heappop, heappush
import math

EXAMPLE_INPUT = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
EXAMPLE_OUTPUT = 102


def dijkstra[
    T
](
    start: T,
    is_target: Callable[[T], bool],
    edges: Callable[[T], list[tuple[int, T]]],
) -> int:
    cheapest = dict[T, int]()
    queue = list[tuple[int, T]]()
    cheapest[start] = 0
    heappush(queue, (0, start))
    count = 0
    while queue:
        count += 1
        (node_cost, node) = heappop(queue)
        if is_target(node):
            print(f"{count=}")
            return node_cost
        for edge_cost, dest in edges(node):
            dest_cost = node_cost + edge_cost
            if dest_cost < cheapest.get(dest, math.inf):
                cheapest[dest] = dest_cost
                heappush(queue, (dest_cost, dest))
    raise Exception("target not found")


@dataclass(frozen=True, order=True)
class Pos:
    row: int
    col: int

    def __add__(self, other: Pos) -> Pos:
        return Pos(self.row + other.row, self.col + other.col)


class Map:
    data: list[list[int]]

    def __init__(self, data: list[list[int]]) -> None:
        self.data = data

    def dims(self) -> tuple[int, int]:
        return (len(self.data), len(self.data[0]))

    def __contains__(self, pos: Pos) -> bool:
        return 0 <= pos.row < len(self.data) and 0 <= pos.col < len(self.data[pos.row])

    def __getitem__(self, pos: Pos) -> int:
        return self.data[pos.row][pos.col]


class Dir(IntEnum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @property
    def delta(self) -> Pos:
        return DELTAS[self]

    def turned(self) -> tuple[Dir, Dir]:
        return TURNS[self]


DELTAS = (Pos(0, 1), Pos(-1, 0), Pos(0, -1), Pos(1, 0))
TURNS = 2 * ((Dir.UP, Dir.DOWN), (Dir.RIGHT, Dir.LEFT))


@dataclass(frozen=True, order=True)
class Node:
    pos: Pos
    dir: Dir
    rem: int  # Remaining moves in same direction


def solve(reader: io.TextIOBase) -> int:
    map = Map([[int(char) for char in line.rstrip()] for line in reader])
    (rows, cols) = map.dims()

    start = Node(Pos(0, 0), Dir.RIGHT, 3)
    target = Pos(rows - 1, cols - 1)
    is_target: Callable[[Node], bool] = lambda node: node.pos == target

    def edges(node: Node) -> list[tuple[int, Node]]:
        dests = list[Node]()
        if node.rem > 0:
            dests.append(Node(node.pos + node.dir.delta, node.dir, node.rem - 1))
        for dir in node.dir.turned():
            dests.append(Node(node.pos + dir.delta, dir, 2))
        return [(map[dest.pos], dest) for dest in dests if dest.pos in map]

    return dijkstra(start, is_target, edges)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
