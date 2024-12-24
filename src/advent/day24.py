from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass

from advent.utils import data_dir, topological_sort


@dataclass(frozen=True)
class Gate:
    in1: str
    in2: str
    operation: str
    out: str

    def evaluate(self, in1: int, in2: int) -> int:
        if self.operation == "AND":
            return in1 & in2

        if self.operation == "OR":
            return in1 | in2

        if self.operation == "XOR":
            return in1 ^ in2

        message = f"Unexpected operation {self.operation}"
        raise AssertionError(message)


def solve() -> None:
    puzzle = data_dir() / "day24.txt"
    data = puzzle.read_text()
    parts = [
        list(part)
        for key, part in itertools.groupby(data.splitlines(), key=bool)
        if key
    ]

    values = {}
    for line in parts[0]:
        name, value = line.split(": ")
        values[name] = int(value)

    gates = {}
    for line in parts[1]:
        left, out = line.split(" -> ")
        in1, operation, in2 = left.split()
        gate = Gate(in1, in2, operation, out)
        gates[out] = gate

    dependencies = defaultdict(list)
    for gate in gates.values():
        dependencies[gate.in1].append(gate.out)
        dependencies[gate.in2].append(gate.out)

    ordered = topological_sort(dependencies, gates)
    for wire in ordered:
        gate = gates[wire]
        values[wire] = gate.evaluate(values[gate.in1], values[gate.in2])

    part_one = 0
    for z in reversed(range(46)):
        wire = f"z{z:02}"
        part_one *= 2
        part_one += values[wire]

    print(f"Part one: {part_one}")

    # Part two by manual inspection of the input and correcting the circuit.
    # Swapped: dbp <-> fdv, ckj <-> z15, kdf <-> z23, rpp <-> z39
