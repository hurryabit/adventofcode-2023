from __future__ import annotations
import io
import os
import re
from dataclasses import dataclass

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
EXAMPLE_OUTPUT = 19114

RULE_RE = re.compile(r"([xmas])([<>])(\d+):([a-z]+|[AR])")
WORKFLOW_RE = re.compile(r"([a-z]+){((?:[^,]+)(?:,[^,]+)*),([^,]+)}")


type Part = dict[str, int]


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

    def exec(self, part: Part) -> str | None:
        part_val = part[self.prop]
        if (self.cmp == "<" and part_val < self.val) or (
            self.cmp == ">" and part_val > self.val
        ):
            return self.tgt
        else:
            return None


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

    def exec(self, part: Part) -> str:
        for rule in self.rules:
            tgt = rule.exec(part)
            if tgt is not None:
                return tgt
        return self.deftgt


@dataclass
class Series:
    wfs: dict[str, Workflow]

    def exec(self, part: Part) -> bool:
        tgt = "in"
        while tgt not in {"A", "R"}:
            tgt = self.wfs[tgt].exec(part)
        return tgt == "A"


def solve(reader: io.TextIOBase) -> int:
    wfs = dict[str, Workflow]()
    for line in reader:
        line = line.rstrip()
        if len(line) == 0:
            break
        wf = Workflow.parse(line)
        wfs[wf.name] = wf
    series = Series(wfs)

    result = 0
    for line in reader:
        line = line.rstrip()
        part: Part = {}
        for assign in line[1:-1].split(","):
            [prop, val] = assign.split("=")
            part[prop] = int(val)
        if series.exec(part):
            result += sum(part.values())
    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
