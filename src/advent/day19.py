from __future__ import annotations

from functools import cache

from advent.utils import data_dir


def count_ways(patterns: list[str], design: str) -> int:
    @cache
    def inner(design: str) -> int:
        if not design:
            return 1

        return sum(
            inner(design[len(pattern) :])
            for pattern in patterns
            if design.startswith(pattern)
        )

    return inner(design)


def solve() -> None:
    puzzle = data_dir() / "day19.txt"
    data = puzzle.read_text()
    lines = data.splitlines()
    patterns = lines[0].split(", ")
    designs = lines[2:]

    counts = [count_ways(patterns, design) for design in designs]

    part_one = sum(1 for count in counts if count != 0)
    print(f"Part one: {part_one}")

    part_two = sum(counts)
    print(f"Part two: {part_two}")
