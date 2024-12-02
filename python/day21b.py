import io
import os
import networkx as nx


def solve(reader: io.TextIOBase) -> int:
    lines = [line.rstrip() for line in reader]
    N = len(lines)
    assert N == 131
    n = N // 2
    G = nx.grid_2d_graph(range(-n, n + 1), range(-n, n + 1))
    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell == "#":
                G.remove_node((i - n, j - n))
    dist = nx.single_source_shortest_path_length(G, (0, 0))
    even = {(i, j) for i, j in dist if (i + j) % 2 == 0}
    odd = set(dist) - even
    even_corners = {v for v in even if dist[v] > 65}
    odd_corners = {v for v in odd if dist[v] > 65}

    K = 202300
    return (
        (K + 1) ** 2 * len(odd)
        - (K + 1) * len(odd_corners)
        + K**2 * len(even)
        + K * len(even_corners)
    )


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
