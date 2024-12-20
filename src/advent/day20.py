from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from advent.utils import data_dir


@dataclass(frozen=True)
class Maze:
    tiles: dict[complex, str]

    @staticmethod
    def from_string(text: str) -> Maze:
        tiles = {
            complex(col, row): char
            for row, line in enumerate(text.splitlines())
            for col, char in enumerate(line)
        }

        return Maze(tiles)

    def solve(self) -> dict[complex, int]:
        end = next(tile for tile, value in self.tiles.items() if value == "E")

        distances = {end: 0}
        queue = deque([(0, end)])

        while queue:
            distance, position = queue.popleft()

            for step in (1, -1, 1j, -1j):
                new_position = position + step
                if self.tiles[new_position] == "#":
                    continue

                if new_position in distances:
                    continue

                new_distance = distance + 1
                distances[new_position] = new_distance
                queue.append((new_distance, new_position))

        return distances


def count_cheats(distances: dict[complex, int], max_cheat: int = 2) -> int:
    cheats = 0
    for p1, d1 in distances.items():
        for dcol in range(-max_cheat, max_cheat + 1):
            max_drow = max_cheat - abs(dcol)
            for drow in range(-max_drow, max_drow + 1):
                p2 = p1 + complex(dcol, drow)
                d2 = distances.get(p2)
                if d2 is None:
                    continue

                saving = d1 - (d2 + abs(dcol) + abs(drow))
                if saving >= 100:
                    cheats += 1

    return cheats


def solve() -> None:
    puzzle = data_dir() / "day20.txt"
    data = puzzle.read_text()
    maze = Maze.from_string(data)

    distances = maze.solve()

    part_one = count_cheats(distances)
    print(f"Part one: {part_one}")

    part_two = count_cheats(distances, max_cheat=20)
    print(f"Part two: {part_two}")
