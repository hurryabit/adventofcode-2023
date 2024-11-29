from __future__ import annotations
import io
import os
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum

sys.setrecursionlimit(1000000)

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
EXAMPLE_OUTPUT = 154


def longest_walk[T](graph: dict[T, dict[T, int]], start: T, target: T) -> int:
    seen = set[T]()
    result = -1

    def go(node: T, dist: int) -> None:
        if node == target:
            nonlocal result
            result = max(result, dist)
            return
        seen.add(node)
        for dest, weight in graph[node].items():
            if dest not in seen:
                go(dest, dist + weight)
        seen.remove(node)
        return

    go(start, 0)
    return result


@dataclass(frozen=True, order=True)
class Pos:
    row: int
    col: int

    def __add__(self, other: Pos) -> Pos:
        return Pos(self.row + other.row, self.col + other.col)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


class Map:
    data: list[str]
    rows: int
    cols: int

    def __init__(self, data: list[str]) -> None:
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __getitem__(self, pos: Pos) -> str:
        if 0 <= pos.row < self.rows and 0 <= pos.col < self.cols:
            return self.data[pos.row][pos.col]
        return "#"

    def nodes(self) -> Iterator[Pos]:
        rows = len(self.data)
        cols = len(self.data[0])
        return (
            pos
            for row in range(rows)
            for col in range(cols)
            if self[pos := Pos(row, col)] != "#"
        )

    def neighbours(self, pos: Pos) -> list[Pos]:
        return [n for dir in Dir if self[n := pos + dir.delta] != "#"]

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


def solve(reader: io.TextIOBase) -> int:
    map = Map([line.rstrip() for line in reader])
    graph = dict[Pos, dict[Pos, int]]()
    for node in map.nodes():
        if len(map.neighbours(node)) != 2:
            graph[node] = {}
    start = Pos(0, 1)
    target = map.bottom_right() + Dir.LEFT.delta
    assert start in graph and target in graph

    for node in graph:
        for curr in map.neighbours(node):
            prev = node
            dist = 1
            while curr not in graph:
                next = (set(map.neighbours(curr)) - {prev}).pop()
                prev = curr
                curr = next
                dist += 1
            graph[node][curr] = max(graph[node].get(curr, 0), dist)

    # lines = ["graph {"]
    # for node, edges in graph.items():
    #     shape = " shape=box" if node in {start, target} else ""
    #     lines.append(f'    n_{node.row}_{node.col}[label="{node}"{shape}];')
    #     for dest, weight in edges.items():
    #         if node <= dest:
    #             lines.append(
    #                 f'    n_{node.row}_{node.col} -- n_{dest.row}_{dest.col} [label="{weight}"];'
    #             )
    # lines.append("}\n")
    # with open("python/day23.dot", "w") as file:
    #     file.write("\n".join(lines))

    return longest_walk(graph, start, target)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
