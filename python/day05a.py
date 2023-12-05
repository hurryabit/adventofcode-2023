from dataclasses import dataclass
import io
import os

EXAMPLE_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
EXAMPLE_OUTPUT = 35


class Map:
    @dataclass
    class Entry:
        dest: int
        source: int
        length: int

    entries: list[Entry]

    def __init__(self, reader: io.TextIOBase):
        self.entries = []
        line = reader.readline().strip()
        while line != "":
            [dest, source, length] = [int(word) for word in line.split()]
            self.entries.append(self.Entry(dest, source, length))
            line = reader.readline().strip()

    def __getitem__(self, source: int) -> int:
        for entry in self.entries:
            if entry.source <= source < entry.source + entry.length:
                return entry.dest + source - entry.source
        return source


def solve(reader: io.TextIOBase) -> int:
    line = reader.readline()
    ids = [int(word) for word in line.split()[1:]]
    reader.readline()
    line = reader.readline().strip()
    while line != "":
        map = Map(reader)
        ids = [map[id] for id in ids]
        line = reader.readline().strip()
    return min(ids)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
