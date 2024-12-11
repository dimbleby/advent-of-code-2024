from __future__ import annotations

from functools import cache

from advent.utils import data_dir


@cache
def expand(blinks: int, stone: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return expand(blinks - 1, 1)

    string = str(stone)
    split, remainder = divmod(len(string), 2)
    if remainder == 0:
        left = int(string[:split])
        right = int(string[split:])
        return expand(blinks - 1, left) + expand(blinks - 1, right)

    return expand(blinks - 1, stone * 2024)


def solve() -> None:
    puzzle = data_dir() / "day11.txt"
    data = puzzle.read_text(encoding="utf-8").strip()

    stones = [int(n) for n in data.split()]

    part_one = sum(expand(25, stone) for stone in stones)
    print(f"Part one: {part_one}")

    part_two = sum(expand(75, stone) for stone in stones)
    print(f"Part two: {part_two}")
