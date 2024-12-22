from __future__ import annotations

from collections import defaultdict

from advent.utils import data_dir


def evolve(secret: int) -> int:
    secret ^= secret << 6
    secret &= 0xFFFFFF
    secret ^= secret >> 5
    secret &= 0xFFFFFF
    secret ^= secret << 11
    secret &= 0xFFFFFF

    return secret


def solve() -> None:
    puzzle = data_dir() / "day22.txt"
    data = puzzle.read_text()
    secrets = [int(line) for line in data.splitlines()]

    bananas: dict[int, int] = defaultdict(int)
    part_one = 0

    for secret in secrets:
        seen = set()
        changes = 0

        current_secret = secret
        current_price = current_secret % 10

        for spot in range(2000):
            new_secret = evolve(current_secret)
            new_price = new_secret % 10

            diff = new_price - current_price
            changes &= 0xFFFFFF
            changes <<= 8
            changes ^= diff + 9
            if spot >= 3 and changes not in seen:
                seen.add(changes)
                bananas[changes] += new_price

            current_secret = new_secret
            current_price = new_price

        part_one += current_secret

    print(f"Part one: {part_one}")

    part_two = max(bananas.values())
    print(f"Part two: {part_two}")
