from __future__ import annotations
import io
import math
import os
from collections.abc import Iterable
from typing import NewType

EXAMPLE_INPUT = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
EXAMPLE_OUTPUT = 54


class Graph[V]:
    edges: dict[V, dict[V, int]]

    def __init__(self):
        self.edges = {}

    def add_edge(self, u: V, v: V, w: int) -> None:
        assert u != v
        self.edges.setdefault(u, {}).setdefault(v, 0)
        self.edges[u][v] += w
        self.edges.setdefault(v, {}).setdefault(u, 0)
        self.edges[v][u] += w

    def remove_node(self, v: V) -> None:
        assert v in self.edges
        for u in self.edges[v]:
            del self.edges[u][v]
        del self.edges[v]

    def __getitem__(self, uv: tuple[V, V]) -> int:
        (u, v) = uv
        return self.edges.get(u, {}).get(v, 0)

    def node_count(self) -> int:
        return len(self.edges)

    def nodes(self) -> Iterable[V]:
        return self.edges.keys()

    def neighbours(self, v: V) -> Iterable[V]:
        return self.edges[v].keys()

    def merge_into(self, u: V, v: V) -> None:
        es = self.edges[u]
        for n, w in es.items():
            if n != v:
                self.add_edge(v, n, w)
        self.remove_node(u)


def minimum_cut_phase[V](g: Graph[V], a: V) -> tuple[int, V, V]:
    A = {a}
    B = {v: g[a, v] for v in g.nodes()}
    del B[a]
    b1 = a
    while len(B) > 1:
        (_, v) = max((B[u], u) for u in B)
        A.add(v)
        del B[v]
        for u in g.neighbours(v):
            if u in B:
                B[u] += g[u, v]
        b1 = v
    (b0, cut) = B.popitem()
    return (cut, b0, b1)


def minimum_cut[V](g: Graph[V]) -> tuple[int, int]:
    assert g.node_count() >= 2
    a = next(iter(g.nodes()))
    cluster_sizes = {v: 1 for v in g.nodes()}
    min_cut: int = math.inf  # type: ignore
    min_split = 0
    while g.node_count() > 1:
        print(f"starting loop with {g.node_count()} nodes")
        (cut, b0, b1) = minimum_cut_phase(g, a)
        if cut < min_cut:
            min_cut = cut
            min_split = cluster_sizes[b0]
        g.merge_into(b1, b0)
        cluster_sizes[b0] += cluster_sizes[b1]
        del cluster_sizes[b1]
    return (min_cut, min_split)


Node = NewType("Node", str)


def solve(reader: io.TextIOBase) -> int:
    g = Graph[Node]()
    for line in reader:
        [v, *us] = line.rstrip().split()
        v = v.rstrip(":")
        for u in us:
            g.add_edge(Node(u), Node(v), 1)

    n = g.node_count()
    (cut, split) = minimum_cut(g)
    assert cut == 3

    return split * (n - split)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
