import io
import os

EXAMPLE_INPUT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
EXAMPLE_OUTPUT = 21


def dot_case(s: str, t: tuple[int, ...]) -> int:
    return possibilities(s[1:], t)


def hash_case(s: str, t: tuple[int, ...]) -> int:
    if len(t) == 0:
        return 0
    k = t[0]
    if len(s) < k or any(c not in "#?" for c in s[:k]):
        return 0
    s = s[k:]
    if len(s) > 0:
        if s[0] not in ".?":
            return 0
        s = s[1:]
    return possibilities(s, t[1:])


def possibilities(s: str, t: tuple[int, ...]) -> int:
    if len(s) == 0:
        return 1 if len(t) == 0 else 0

    match s[0]:
        case ".":
            return dot_case(s, t)
        case "#":
            return hash_case(s, t)
        case "?":
            return dot_case(s, t) + hash_case(s, t)
        case _:
            raise ValueError(f"Invalid character: {s[0]}")


def solve(reader: io.TextIOBase) -> int:
    result = 0
    for line in reader:
        [s, t0] = line.split()
        t = tuple(map(int, t0.split(",")))
        result += possibilities(s, t)
    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
