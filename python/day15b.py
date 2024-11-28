import os
from collections.abc import Callable

EXAMPLE_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
EXAMPLE_OUTPUT = 145


def hash(input: str) -> int:
    res = 0
    for char in input:
        res = 17 * (res + ord(char)) % 256
    return res


assert hash("HASH") == 52


def find[T](l: list[T], p: Callable[[T], bool]) -> int | None:
    return next((i for i, x in enumerate(l) if p(x)), None)


def solve(input: str) -> int:
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]
    for step in input.rstrip().split(","):
        if step[-1] == "-":
            label = step[:-1]
            box = boxes[hash(label)]
            index = next((i for i, (l, _) in enumerate(box) if l == label), None)
            if index is not None:
                box.pop(index)
        else:
            assert step[-2] == "="
            label = step[:-2]
            focus = int(step[-1])
            box = boxes[hash(label)]
            index = next((i for i, (l, _) in enumerate(box) if l == label), None)
            if index is None:
                box.append((label, focus))
            else:
                box[index] = (label, focus)

    result = 0
    for i, box in enumerate(boxes):
        for j, (_, focus) in enumerate(box):
            result += (i + 1) * (j + 1) * focus

    return result


assert solve(EXAMPLE_INPUT) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file.read())
        print(solution)


if __name__ == "__main__":
    main()
