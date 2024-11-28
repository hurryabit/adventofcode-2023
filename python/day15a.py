import os

EXAMPLE_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
EXAMPLE_OUTPUT = 1320


def hash(input: str) -> int:
    res = 0
    for char in input:
        res = 17 * (res + ord(char)) % 256
    return res


assert hash("HASH") == 52


def solve(input: str) -> int:
    result = 0
    for step in input.rstrip().split(","):
        result += hash(step)
    return result


assert solve(EXAMPLE_INPUT) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file.read())
        print(solution)


if __name__ == "__main__":
    main()
