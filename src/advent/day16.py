from __future__ import annotations

import heapq
from collections import defaultdict
from dataclasses import dataclass

from advent.utils import data_dir

INFINITY = 1_000_000_000


@dataclass(frozen=True)
class State:
    position: complex
    direction: complex

    def __lt__(self, other: State) -> bool:
        return False


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

    def solve(self) -> tuple[int, int]:
        start = next(tile for tile, value in self.tiles.items() if value == "S")
        end = next(tile for tile, value in self.tiles.items() if value == "E")

        initial_state = State(start, 1)
        costs = defaultdict(lambda: INFINITY) | {initial_state: 0}
        predecessors: dict[State, list[State]] = {initial_state: []}

        queue = [(0, initial_state)]
        heapq.heapify(queue)

        while queue:
            cost, state = heapq.heappop(queue)
            if cost > costs[state]:
                continue

            for turn in (1, 1j, -1j):
                new_direction = state.direction * turn
                new_position = state.position + new_direction
                if self.tiles[new_position] == "#":
                    continue

                penalty = 0 if turn == 1 else 1000
                new_cost = cost + penalty + 1

                # It is not helpful to go back on ourselves.
                opposite_state = State(new_position, -new_direction)
                if new_cost > costs[opposite_state]:
                    continue

                new_state = State(new_position, new_direction)
                old_cost = costs[new_state]

                if new_cost < old_cost:
                    costs[new_state] = new_cost
                    predecessors[new_state] = [state]
                    heapq.heappush(queue, (new_cost, new_state))

                if new_cost == old_cost:
                    predecessors[new_state].append(state)

        end_states = [State(end, direction) for direction in (1, -1, 1j, -1j)]
        best_cost = min(costs[state] for state in end_states)

        best_tiles = set()
        visited = set()
        stack = [state for state in end_states if costs[state] == best_cost]
        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)

            best_tiles.add(state.position)
            stack.extend(predecessors[state])

        return best_cost, len(best_tiles)


def solve() -> None:
    puzzle = data_dir() / "day16.txt"
    data = puzzle.read_text(encoding="utf-8")
    maze = Maze.from_string(data)
    best_cost, tile_count = maze.solve()
    print(f"Part one: {best_cost}")
    print(f"Part two: {tile_count}")
