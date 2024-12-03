from __future__ import annotations

import re

from advent.utils import data_dir


def solve() -> None:
    puzzle = data_dir() / "day03.txt"
    data = puzzle.read_text(encoding="utf-8")

    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    total = 0
    for match in pattern.finditer(data):
        total += int(match.group(1)) * int(match.group(2))

    print(f"Part one: {total}")

    total = 0
    pieces = re.split(r"don't\(\)", "do()" + data)
    for piece in pieces:
        start = piece.find("do()")
        if start == -1:
            continue

        for match in pattern.finditer(piece[start:]):
            total += int(match.group(1)) * int(match.group(2))

    print(f"Part two: {total}")
