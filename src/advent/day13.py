from __future__ import annotations

import itertools
import re

from advent.utils import data_dir


def cost(a: int, b: int, c: int, d: int, x: int, y: int) -> int | None:
    det = a * d - b * c
    assert det != 0

    l1, remainder = divmod(x * d - b * y, det)
    if remainder != 0:
        return None

    l2, remainder = divmod(a * y - x * c, det)
    if remainder != 0:
        return None

    assert l1 >= 0
    assert l2 >= 0

    return 3 * l1 + l2


def solve() -> None:
    puzzle = data_dir() / "day13.txt"
    data = puzzle.read_text(encoding="utf-8").strip()

    puzzles = []
    parts = [
        list(part)
        for key, part in itertools.groupby(data.splitlines(), key=bool)
        if key
    ]
    for part in parts:
        a, c = (int(number) for number in re.findall(r"(\d+)", part[0]))
        b, d = (int(number) for number in re.findall(r"(\d+)", part[1]))
        x, y = (int(number) for number in re.findall(r"(\d+)", part[2]))
        puzzles.append((a, b, c, d, x, y))

    costs = itertools.starmap(cost, puzzles)
    part_one = sum(cost for cost in costs if cost is not None)
    print(f"Part one: {part_one}")

    puzzles = [
        (a, b, c, d, x + 10000000000000, y + 10000000000000)
        for (a, b, c, d, x, y) in puzzles
    ]
    costs = itertools.starmap(cost, puzzles)
    part_two = sum(cost for cost in costs if cost is not None)
    print(f"Part two: {part_two}")
