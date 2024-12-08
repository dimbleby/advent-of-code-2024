from __future__ import annotations

from itertools import starmap

from advent.utils import data_dir


def unconcat(left: int, right: int) -> int | None:
    tmp = right
    tens = 1
    while tmp > 0:
        tens *= 10
        tmp //= 10

    quotient, remainder = divmod(left, tens)
    return quotient if remainder == right else None


# Work backwards from target, aiming for zero.  Much less branching in this direction,
# compared to starting from zero and hoping to hit the target.
def satisfy(target: int, operands: list[int], *, part_two: bool = False) -> int:
    stack = [(target, len(operands))]
    while stack:
        value, unused = stack.pop()

        if unused == 0:
            if value == 0:
                return target
            continue

        unused -= 1
        operand = operands[unused]

        if value < operand:
            continue

        stack.append((value - operand, unused))

        quotient, remainder = divmod(value, operand)
        if remainder == 0:
            stack.append((quotient, unused))

        if part_two:
            shortened = unconcat(value, operand)
            if shortened is not None:
                stack.append((shortened, unused))

    return 0


def solve() -> None:
    puzzle = data_dir() / "day07.txt"
    data = puzzle.read_text(encoding="utf-8")

    equations = []
    for line in data.splitlines():
        parts = line.split(":")
        target = int(parts[0])
        operands = [int(n) for n in parts[1].split()]
        equations.append((target, operands))

    part_one = sum(starmap(satisfy, equations))
    print(f"Part one: {part_one}")

    part_two = sum(satisfy(*equation, part_two=True) for equation in equations)
    print(f"Part two: {part_two}")
