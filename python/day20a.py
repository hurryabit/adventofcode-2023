from __future__ import annotations
import io
import math
import os
from collections import deque
from dataclasses import dataclass

EXAMPLE_INPUT1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
EXAMPLE_OUTPUT1 = 32000000
EXAMPLE_INPUT2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
EXAMPLE_OUTPUT2 = 11687500


@dataclass
class Pulse:
    src: str
    dst: str
    high: bool


class Network:
    modules: dict[str, Module]
    queue: deque[Pulse]
    count: dict[bool, int]

    def __init__(self, modules: list[Module]) -> None:
        self.modules = {mod.name: mod for mod in modules}
        for src_mod in self.modules.values():
            for dst in src_mod.dsts:
                dst_mod = self.modules.get(dst, None)
                if dst_mod is not None:
                    dst_mod.add_src(src_mod.name)
        self.queue = deque()
        self.count = {False: 0, True: 0}

    def send(self, pulse: Pulse) -> None:
        self.queue.append(pulse)
        while self.queue:
            pulse = self.queue.popleft()
            # print(f"{pulse.src} -{"high" if pulse.high else "low"}-> {pulse.dst}")
            self.count[pulse.high] += 1
            mod = self.modules.get(pulse.dst, None)
            if mod is None:
                continue
            out = mod.output(pulse)
            if out is not None:
                self.queue.extend(
                    Pulse(src=mod.name, dst=dst, high=out) for dst in mod.dsts
                )


class Module:
    name: str
    dsts: list[str]

    def __init__(self, name: str, dsts: list[str]) -> None:
        self.name = name
        self.dsts = dsts

    def output(self, pulse: Pulse) -> bool | None:
        return pulse.high

    def add_src(self, src: str) -> None:
        pass


class FlipFlop(Module):
    def __init__(self, name: str, dsts: list[str]) -> None:
        super().__init__(name, dsts)
        self.on = False

    def output(self, pulse: Pulse) -> bool | None:
        if pulse.high:
            return None
        self.on = not self.on
        return self.on


class Conjunction(Module):
    def __init__(self, name: str, dsts: list[str]) -> None:
        super().__init__(name, dsts)
        self.srcs: dict[str, bool] = {}

    def output(self, pulse: Pulse) -> bool | None:
        self.srcs[pulse.src] = pulse.high
        return not all(self.srcs.values())

    def add_src(self, src: str):
        self.srcs[src] = False


def solve(reader: io.TextIOBase) -> int:
    modules: list[Module] = []
    for line in reader:
        [name, _, *dsts] = line.rstrip().split()
        match name[0]:
            case "%":
                name = name[1:]
                cls = FlipFlop
            case "&":
                name = name[1:]
                cls = Conjunction
            case _:
                cls = Module
        modules.append(cls(name, [dst.rstrip(",") for dst in dsts]))

    network = Network(modules)
    for _ in range(1000):
        network.send(Pulse("button", "broadcaster", False))
    return math.prod(network.count.values())


assert solve(io.StringIO(EXAMPLE_INPUT1)) == EXAMPLE_OUTPUT1
assert solve(io.StringIO(EXAMPLE_INPUT2)) == EXAMPLE_OUTPUT2


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
