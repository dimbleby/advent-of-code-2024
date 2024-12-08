from __future__ import annotations

import itertools
from collections import defaultdict
from typing import TYPE_CHECKING

from advent.utils import Vec2, data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator


def in_bounds(bounds: tuple[int, int], vec: Vec2) -> bool:
    rows, cols = bounds

    return 0 <= vec.x < rows and 0 <= vec.y < cols


def get_antinodes(
    bounds: tuple[int, int], a1: Vec2, a2: Vec2, *, part_two: bool = False
) -> Iterator[Vec2]:
    step = a2 - a1

    antinode = a2 if part_two else a2 + step
    while in_bounds(bounds, antinode):
        yield antinode

        if not part_two:
            break

        antinode = antinode + step

    antinode = a1 if part_two else a1 - step
    while in_bounds(bounds, antinode):
        yield antinode

        if not part_two:
            break

        antinode = antinode - step


def solve() -> None:
    puzzle = data_dir() / "day08.txt"
    data = puzzle.read_text(encoding="utf-8")

    antennae = defaultdict(list)
    for i, row in enumerate(data.splitlines()):
        for j, char in enumerate(row):
            if char == ".":
                continue
            antennae[char].append(Vec2(i, j))

    bounds = (i + 1, j + 1)

    antinodes: set[Vec2] = set()
    for locations in antennae.values():
        for a1, a2 in itertools.combinations(locations, 2):
            antinodes.update(get_antinodes(bounds, a1, a2))

    print(f"Part one: {len(antinodes)}")

    antinodes = set()
    for locations in antennae.values():
        for a1, a2 in itertools.combinations(locations, 2):
            antinodes.update(get_antinodes(bounds, a1, a2, part_two=True))

    print(f"Part two: {len(antinodes)}")
