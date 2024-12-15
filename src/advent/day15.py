from __future__ import annotations

import itertools
from dataclasses import dataclass

from advent.utils import data_dir

MOVES = {"^": -1j, "v": 1j, ">": 1, "<": -1}


@dataclass
class Warehouse:
    cells: dict[complex, str]
    robot: complex

    @staticmethod
    def from_text(lines: list[str]) -> Warehouse:
        cells = {
            complex(x, y): char
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
        }
        robot = next(cell for cell, value in cells.items() if value == "@")

        return Warehouse(cells, robot)

    @staticmethod
    def wider_from_text(lines: list[str]) -> Warehouse:
        cells = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                here = complex(2 * x, y)
                if char == "O":
                    cells[here] = "["
                    cells[here + 1] = "]"
                elif char == "@":
                    robot = here
                    cells[here] = char
                    cells[here + 1] = "."
                else:
                    cells[here] = cells[here + 1] = char

        return Warehouse(cells, robot)

    def score(self) -> int:
        return sum(
            int(cell.real + cell.imag * 100)
            for cell, value in self.cells.items()
            if value in "O["
        )

    def make_move(self, move: str) -> None:
        step = MOVES[move]
        to_move = set()

        stack = [self.robot]
        while stack:
            cell = stack.pop()
            if cell in to_move:
                continue
            to_move.add(cell)

            neighbour = cell + step
            neighbour_value = self.cells[neighbour]
            if neighbour_value == "#":
                return

            if neighbour_value != ".":
                stack.append(neighbour)

            value = self.cells[cell]
            if value == "[":
                stack.append(cell + 1)
            if value == "]":
                stack.append(cell - 1)

        for cell in sorted(
            to_move,
            key=lambda c: (c.real, c.imag),
            reverse=step.real + step.imag > 0,
        ):
            self.cells[cell + step] = self.cells[cell]
            self.cells[cell] = "."

        self.robot += step


def solve() -> None:
    puzzle = data_dir() / "day15.txt"
    data = puzzle.read_text()

    parts = [
        list(part)
        for key, part in itertools.groupby(data.splitlines(), key=bool)
        if key
    ]
    moves = "".join(parts[1])

    warehouse = Warehouse.from_text(parts[0])
    for move in moves:
        warehouse.make_move(move)

    part_one = warehouse.score()
    print(f"Part one: {part_one}")

    warehouse = Warehouse.wider_from_text(parts[0])
    for move in moves:
        warehouse.make_move(move)

    part_two = warehouse.score()
    print(f"Part two: {part_two}")
