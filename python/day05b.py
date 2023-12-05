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
EXAMPLE_OUTPUT = 46


@dataclass(order=True)
class I:
    start: int
    end: int


def condense(intervals: list[I]) -> list[I]:
    if len(intervals) == 0:
        return []
    intervals.sort()
    res = []
    prev = intervals[0]
    for curr in intervals[1:]:
        if curr.start <= prev.end:
            prev.end = max(prev.end, curr.end)
        else:
            res.append(prev)
            prev = curr
    res.append(prev)
    return res


assert condense([I(0, 3), I(1, 2), I(3, 5), I(6, 8), I(7, 9)]) == [I(0, 5), I(6, 9)]


@dataclass(order=True)
class E:
    interval: I
    delta: int


def transform(intervals: list[I], entries: list[E]) -> list[I]:
    res = []
    m, n = len(intervals), len(entries)
    i, j = 0, 0
    while i < m and j < n:
        interval, entry = intervals[i], entries[j]
        if interval.start < entry.interval.start:
            if interval.end <= entry.interval.start:
                res.append(interval)
                i += 1
                continue
            res.append(I(interval.start, entry.interval.start))
            interval.start = entry.interval.start
        delta = entry.delta
        if interval.end <= entry.interval.end:
            interval.start += delta
            interval.end += delta
            res.append(interval)
            i += 1
            continue
        if interval.start < entry.interval.end:
            res.append(I(interval.start + delta, entry.interval.end + delta))
            interval.start = entry.interval.end
        j += 1
    res.extend(intervals[i:])
    return res


def solve(reader: io.TextIOBase) -> int:
    intervals = []
    line = reader.readline()
    nums = [int(word) for word in line.split()[1:]]
    for i in range(0, len(nums), 2):
        start, length = nums[i], nums[i + 1]
        intervals.append(I(start, start + length))
    reader.readline()

    transformers = []
    line = reader.readline().strip()
    while line != "":
        transformer = []
        line = reader.readline().strip()
        while line != "":
            [dest, source, length] = [int(word) for word in line.split()]
            transformer.append(E(I(source, source + length), dest - source))
            line = reader.readline().strip()
        transformer.sort()
        transformers.append(transformer)
        line = reader.readline().strip()

    intervals = condense(intervals)
    for transformer in transformers:
        intervals = condense(transform(intervals, transformer))

    return intervals[0].start


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
