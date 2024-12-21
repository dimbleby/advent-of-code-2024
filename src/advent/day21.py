from __future__ import annotations

import itertools
from functools import cache
from typing import TYPE_CHECKING

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator

NUMBERS = {char: divmod(n, 3) for n, char in enumerate("789456123 0A")}
DIRECTIONS = {char: divmod(n, 3) for n, char in enumerate(" ^A<v>")}


def get_paths(start: str, end: str, *, door: bool) -> Iterator[str]:
    keypad = NUMBERS if door else DIRECTIONS
    gap = keypad[" "]

    r1, c1 = keypad[start]
    r2, c2 = keypad[end]

    drow = r2 - r1
    dcol = c2 - c1

    north_south = "v" * drow + "^" * -drow
    east_west = ">" * dcol + "<" * -dcol

    if c1 != gap[1] or r2 != gap[0]:
        yield north_south + east_west

    if r1 != gap[0] or c2 != gap[1]:
        yield east_west + north_south


@cache
def get_length(code: str, depth: int, *, door: bool = False) -> int:
    if depth == 0:
        return len(code)

    length = 0
    for here, there in itertools.pairwise("A" + code):
        paths = get_paths(here, there, door=door)
        length += min(get_length(path + "A", depth - 1) for path in paths)

    return length


def solve_code(code: str, depth: int = 3) -> int:
    length = get_length(code, depth, door=True)
    numeric = int(code[:-1])

    return length * numeric


def solve() -> None:
    puzzle = data_dir() / "day21.txt"
    data = puzzle.read_text()
    codes = data.splitlines()

    part_one = sum(solve_code(code) for code in codes)
    print(f"Part one: {part_one}")

    part_two = sum(solve_code(code, depth=26) for code in codes)
    print(f"Part two: {part_two}")
