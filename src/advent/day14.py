from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from math import prod

from advent.utils import Vec2, data_dir

ROWS = 103
COLS = 101
MIDROW = ROWS // 2
MIDCOL = COLS // 2


@dataclass
class Robot:
    position: Vec2
    velocity: Vec2

    @staticmethod
    def from_line(line: str) -> Robot:
        numbers = [int(number) for number in re.findall(r"(-?\d+)", line)]
        position = Vec2(numbers[0], numbers[1])
        velocity = Vec2(numbers[2], numbers[3])
        return Robot(position, velocity)

    def step(self, steps: int = 1) -> None:
        x = (self.position.x + steps * self.velocity.x) % COLS
        y = (self.position.y + steps * self.velocity.y) % ROWS
        self.position = Vec2(x, y)

    def quadrant(self) -> int | None:
        if self.position.x < MIDCOL and self.position.y < MIDROW:
            return 1

        if self.position.x < MIDCOL and self.position.y > MIDROW:
            return 2

        if self.position.x > MIDCOL and self.position.y < MIDROW:
            return 3

        if self.position.x > MIDCOL and self.position.y > MIDROW:
            return 4

        return None


def solve() -> None:
    puzzle = data_dir() / "day14.txt"
    data = puzzle.read_text()

    robots = [Robot.from_line(line) for line in data.splitlines()]

    for robot in robots:
        robot.step(100)

    quadrants = (robot.quadrant() for robot in robots)
    quadrant_counts = Counter(q for q in quadrants if q is not None)
    part_one = prod(quadrant_counts.values())
    print(f"Part one: {part_one}")

    robots = [Robot.from_line(line) for line in data.splitlines()]
    for time in range(ROWS * COLS):  # noqa: B007
        for robot in robots:
            robot.step()

        position_counts = Counter(robot.position for robot in robots)
        if max(position_counts.values()) == 1:
            break

    positions = {robot.position for robot in robots}
    for row in range(ROWS):
        chars = ["█" if Vec2(col, row) in positions else "." for col in range(COLS)]
        line = "".join(chars)
        print(line)

    print(f"Part two: {time + 1}")
