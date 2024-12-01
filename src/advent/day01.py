from __future__ import annotations

from collections import Counter

from advent.utils import data_dir


def solve() -> None:
    puzzle = data_dir() / "day01.txt"
    data = puzzle.read_text(encoding="utf-8")

    pairs = ((int(n) for n in line.split()) for line in data.splitlines())
    lefts, rights = (sorted(ns) for ns in zip(*pairs, strict=True))

    part_one = sum(abs(left - right) for left, right in zip(lefts, rights, strict=True))
    print(f"Part one: {part_one}")

    right_counts = Counter(rights)
    part_two = sum(left * right_counts[left] for left in lefts)
    print(f"Part two: {part_two}")
