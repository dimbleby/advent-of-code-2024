from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from advent.utils import data_dir

INFINITY = 1_000_000_000


@dataclass(frozen=True)
class Maze:
    tiles: dict[complex, int]

    @staticmethod
    def from_lines(lines: list[str]) -> Maze:
        tiles = defaultdict(lambda: INFINITY)
        for count, line in enumerate(lines, 1):
            x, y = (int(n) for n in line.split(","))
            tiles[complex(x, y)] = count

        return Maze(tiles)

    def solve(self, tick: int) -> int | None:
        start = 0j
        end = complex(70, 70)

        visited = set()
        queue = deque([(0, start)])

        while queue:
            cost, position = queue.popleft()

            if position == end:
                return cost

            for step in (1, -1, 1j, -1j):
                new_position = position + step
                if not 0 <= new_position.real <= 70:
                    continue

                if not 0 <= new_position.imag <= 70:
                    continue

                if self.tiles[new_position] <= tick:
                    continue

                if new_position in visited:
                    continue

                visited.add(new_position)
                queue.append((cost + 1, new_position))

        return None


def solve() -> None:
    puzzle = data_dir() / "day18.txt"
    data = puzzle.read_text()
    lines = data.splitlines()

    maze = Maze.from_lines(lines)
    part_one = maze.solve(1024)
    print(f"Part one: {part_one}")

    good = 0
    bad = len(lines)
    while good + 1 < bad:
        middle = (good + bad) // 2
        blocked = maze.solve(middle) is None
        good, bad = (good, middle) if blocked else (middle, bad)

    print(f"Part two: {lines[bad - 1]}")
