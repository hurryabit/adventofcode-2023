import io
import math

DAY = 2
EXAMPLE_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
EXAMPLE_OUTPUT = 2286


def analyse_game(game: str) -> int:
    maxs = dict(red=0, green=0, blue=0)
    [_, rounds] = game.split(":", maxsplit=1)
    for round in rounds.split(";"):
        for info in round.split(","):
            [count, color] = info.strip().split(maxsplit=1)
            maxs[color] = max(maxs[color], int(count))

    return math.prod(maxs.values())


def solve(reader: io.TextIOBase) -> int:
    return sum(analyse_game(line) for line in reader)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY:02}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
