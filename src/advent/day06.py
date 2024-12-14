from __future__ import annotations

from dataclasses import dataclass

from advent.utils import data_dir


@dataclass
class Grid:
    cells: dict[complex, str]

    @staticmethod
    def from_lines(lines: list[str]) -> Grid:
        cells = {
            complex(x, y): cell
            for x, row in enumerate(lines)
            for y, cell in enumerate(row)
        }

        return Grid(cells)

    def find_guard(self) -> complex:
        guards = (coord for coord, cell in self.cells.items() if cell == "^")
        return next(guards)

    def visited_points(self, start: complex) -> set[complex] | None:
        position = start
        direction = complex(-1)
        visited = set()

        while True:
            if (position, direction) in visited:
                return None
            visited.add((position, direction))

            new_position = position + direction

            cell = self.cells.get(new_position)
            if cell is None:
                break

            if cell == "#":
                direction = direction * -1j
            else:
                position = new_position

        return {position for (position, direction) in visited}


def solve() -> None:
    puzzle = data_dir() / "day06.txt"
    data = puzzle.read_text()
    lines = data.splitlines()
    grid = Grid.from_lines(lines)
    guard = grid.find_guard()

    visited = grid.visited_points(guard)
    assert visited is not None
    print(f"Part one: {len(visited)}")

    count = 0
    for coord in visited:
        if grid.cells[coord] != ".":
            continue

        grid.cells[coord] = "#"
        if grid.visited_points(guard) is None:
            count += 1
        grid.cells[coord] = "."

    print(f"Part two: {count}")
