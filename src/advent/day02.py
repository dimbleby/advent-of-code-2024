from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator


def safe(report: list[int]) -> bool:
    diffs = [y - x for x, y in itertools.pairwise(report)]
    increasing = all(1 <= diff <= 3 for diff in diffs)
    decreasing = all(-3 <= diff <= -1 for diff in diffs)
    return increasing or decreasing


def variations(report: list[int]) -> Iterator[list[int]]:
    yield report
    for i in range(len(report)):
        variation = report.copy()
        del variation[i]
        yield variation


def safe2(report: list[int]) -> bool:
    return any(safe(variation) for variation in variations(report))


def solve() -> None:
    puzzle = data_dir() / "day02.txt"
    data = puzzle.read_text()

    reports = [[int(n) for n in line.split()] for line in data.splitlines()]

    part_one = sum(safe(report) for report in reports)
    print(f"Part one: {part_one}")

    part_two = sum(safe2(report) for report in reports)
    print(f"Part two: {part_two}")
