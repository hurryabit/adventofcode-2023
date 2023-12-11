import io
import os

EXAMPLE_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
EXAMPLE_OUTPUT = 374


def solve(reader: io.TextIOBase) -> int:
    image = [line.rstrip() for line in reader]
    m, n = len(image), len(image[0])
    galaxies = []
    galaxy_is = set()
    galaxy_js = set()
    for i in range(m):
        for j in range(n):
            if image[i][j] == "#":
                galaxies.append((i, j))
                galaxy_is.add(i)
                galaxy_js.add(j)

    i_expansion = m * [0]
    new_i = 0
    for i in range(m):
        i_expansion[i] = new_i
        if i in galaxy_is:
            new_i += 1
        else:
            new_i += 2

    j_expansion = n * [0]
    new_j = 0
    for j in range(n):
        j_expansion[j] = new_j
        if j in galaxy_js:
            new_j += 1
        else:
            new_j += 2

    result = 0
    for k in range(len(galaxies)):
        (i1, j1) = galaxies[k]
        for l in range(k + 1, len(galaxies)):
            (i2, j2) = galaxies[l]
            result += abs(i_expansion[i1] - i_expansion[i2]) + abs(
                j_expansion[j1] - j_expansion[j2]
            )

    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
