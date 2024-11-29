from __future__ import annotations
import io
import math
import os
from collections import deque
from dataclasses import dataclass


@dataclass
class Pulse:
    src: str
    dst: str
    high: bool


class Network:
    modules: dict[str, Module]
    queue: deque[Pulse]
    count: int
    firsts: dict[str, int]

    def __init__(self, modules: list[Module]) -> None:
        self.modules = {mod.name: mod for mod in modules}
        for src_mod in self.modules.values():
            for dst in src_mod.dsts:
                dst_mod = self.modules.get(dst, None)
                if dst_mod is not None:
                    dst_mod.add_src(src_mod.name)
        self.queue = deque()
        self.count = 0
        self.firsts = {}

    def send(self, pulse: Pulse) -> bool:
        self.count += 1
        self.queue.append(pulse)
        while self.queue:
            pulse = self.queue.popleft()
            if pulse.dst == "kh" and pulse.high:
                if pulse.src not in self.firsts:
                    self.firsts[pulse.src] = self.count
                    if len(self.firsts) == len(self.modules["kh"].srcs):  # type: ignore
                        return True
            # print(f"{pulse.src} -{"high" if pulse.high else "low"}-> {pulse.dst}")
            mod = self.modules.get(pulse.dst, None)
            if mod is None:
                continue
            out = mod.output(pulse)
            if out is not None:
                self.queue.extend(
                    Pulse(src=mod.name, dst=dst, high=out) for dst in mod.dsts
                )
        return False


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

    def label(self) -> str:
        return self.name


class FlipFlop(Module):
    def __init__(self, name: str, dsts: list[str]) -> None:
        super().__init__(name, dsts)
        self.on = False

    def output(self, pulse: Pulse) -> bool | None:
        if pulse.high:
            return None
        self.on = not self.on
        return self.on

    def label(self) -> str:
        return "%" + self.name


class Conjunction(Module):
    def __init__(self, name: str, dsts: list[str]) -> None:
        super().__init__(name, dsts)
        self.srcs: dict[str, bool] = {}

    def output(self, pulse: Pulse) -> bool | None:
        self.srcs[pulse.src] = pulse.high
        return not all(self.srcs.values())

    def add_src(self, src: str):
        self.srcs[src] = False

    def label(self) -> str:
        return "&" + self.name


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
    while not network.send(Pulse("button", "broadcaster", False)):
        pass
    return math.lcm(*network.firsts.values())


def main():
    prefix = os.path.splitext(os.path.basename(__file__))[0][:-1]
    with open(f"input/{prefix}.txt") as file:
        solution = solve(file)
        print(solution)


if __name__ == "__main__":
    main()
