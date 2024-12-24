from __future__ import annotations

import itertools
from collections import defaultdict

from advent.utils import data_dir, topological_sort

type Rule = tuple[int, int]


def middle(ns: list[int]) -> int:
    index = len(ns) // 2
    return ns[index]


def valid(rules: list[Rule], update: list[int]) -> bool:
    order = {value: position for position, value in enumerate(update)}

    for before, after in rules:
        p1 = order.get(before)
        if p1 is None:
            continue

        p2 = order.get(after)
        if p2 is None:
            continue

        if p1 > p2:
            return False

    return True


def solve() -> None:
    puzzle = data_dir() / "day05.txt"
    data = puzzle.read_text()
    parts = [
        list(part)
        for key, part in itertools.groupby(data.splitlines(), key=bool)
        if key
    ]

    rules = []
    for line in parts[0]:
        before, after = (int(n) for n in line.split("|"))
        rules.append((before, after))

    updates = [[int(n) for n in line.split(",")] for line in parts[1]]

    part_one = sum(middle(update) for update in updates if valid(rules, update))

    print(f"Part one: {part_one}")

    dependencies = defaultdict(list)
    for before, after in rules:
        dependencies[before].append(after)

    ordered = (
        topological_sort(dependencies, update)
        for update in updates
        if not valid(rules, update)
    )

    part_two = sum(middle(update) for update in ordered)

    print(f"Part two: {part_two}")
