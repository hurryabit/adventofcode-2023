from __future__ import annotations
import io
import os
import re
from dataclasses import dataclass
import math

EXAMPLE_INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
EXAMPLE_OUTPUT = 167409079868000

RULE_RE = re.compile(r"([xmas])([<>])(\d+):([a-z]+|[AR])")
WORKFLOW_RE = re.compile(r"([a-z]+){((?:[^,]+)(?:,[^,]+)*),([^,]+)}")


type Box = dict[str, range]


@dataclass
class Rule:
    prop: str
    cmp: str
    val: int
    tgt: str

    @classmethod
    def parse(cls, input: str) -> Rule:
        m = RULE_RE.fullmatch(input)
        assert m is not None
        return Rule(m[1], m[2], int(m[3]), m[4])

    def exec(self, box: Box) -> tuple[Box | None, Box | None]:
        rng = box[self.prop]
        match self.cmp:
            case "<":
                matches = range(rng.start, self.val)
                kontinue = range(self.val, rng.stop)
            case ">":
                matches = range(self.val + 1, rng.stop)
                kontinue = range(rng.start, self.val + 1)
            case _:
                raise Exception(f"bad cmp: {self.cmp}")
        matches = None if len(matches) == 0 else box | {self.prop: matches}
        kontinue = None if len(kontinue) == 0 else box | {self.prop: kontinue}
        return (matches, kontinue)


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    deftgt: str

    @classmethod
    def parse(cls, input: str) -> Workflow:
        m = WORKFLOW_RE.fullmatch(input)
        assert m is not None
        rules = [Rule.parse(rule) for rule in m[2].split(",")]
        return Workflow(m[1], rules, m[3])

    def exec(self, box: Box) -> list[tuple[Box, str]]:
        result: list[tuple[Box, str]] = []
        for rule in self.rules:
            (matches, kontinue) = rule.exec(box)
            if matches is not None:
                result.append((matches, rule.tgt))
            if kontinue is None:
                break
            box = kontinue
        else:
            result.append((box, self.deftgt))
        return result


@dataclass
class Series:
    wfs: dict[str, Workflow]

    def exec(self, box: Box) -> int:
        result = 0
        queue = [(box, "in")]
        while queue:
            (box, tgt) = queue.pop()
            match tgt:
                case "R":
                    pass
                case "A":
                    result += math.prod(len(rng) for rng in box.values())
                case _:
                    queue.extend(self.wfs[tgt].exec(box))
        return result


def solve(reader: io.TextIOBase) -> int:
    wfs = dict[str, Workflow]()
    for line in reader:
        line = line.rstrip()
        if len(line) == 0:
            break
        wf = Workflow.parse(line)
        wfs[wf.name] = wf
    series = Series(wfs)
    box = {prop: range(1, 4001) for prop in "xmas"}
    return series.exec(box)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
