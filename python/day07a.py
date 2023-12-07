from collections import Counter
import io
import os

EXAMPLE_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
EXAMPLE_OUTPUT = 6440

CARD_VALUES = dict(zip("23456789TJQKA", range(2, 15)))

HAND_VALUES = {
    (1, 1, 1, 1, 1): 1,
    (2, 1, 1, 1): 2,
    (2, 2, 1): 3,
    (3, 1, 1): 4,
    (3, 2): 5,
    (4, 1): 6,
    (5,): 7,
}


def hand_value(hand: str) -> tuple[int, ...]:
    sig = tuple(sorted(Counter(hand).values(), reverse=True))
    return (HAND_VALUES[sig],) + tuple(CARD_VALUES[card] for card in hand)


def solve(reader: io.TextIOBase) -> int:
    hands = [line.split() for line in reader]
    hands.sort(key=lambda hand_bet: hand_value(hand_bet[0]))
    return sum((i + 1) * int(bet) for (i, (_, bet)) in enumerate(hands))


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
