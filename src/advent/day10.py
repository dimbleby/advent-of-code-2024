from __future__ import annotations

from advent.utils import data_dir


def solve() -> None:
    puzzle = data_dir() / "day10.txt"
    data = puzzle.read_text(encoding="utf-8")

    grid = [[int(n) for n in line] for line in data.splitlines()]
    rows = len(grid)
    cols = len(grid[0])

    zeros = [
        (row, col) for row in range(rows) for col in range(cols) if grid[row][col] == 0
    ]

    score = 0
    rating = 0

    for start in zeros:
        nines = set()
        stack = [start]
        while stack:
            row, col = stack.pop()
            value = grid[row][col]
            if value == 9:
                nines.add((row, col))
                rating += 1
                continue

            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_row, new_col = row + dr, col + dc
                if not (0 <= new_row < rows and 0 <= new_col < cols):
                    continue

                new_value = grid[new_row][new_col]

                if new_value == value + 1:
                    stack.append((new_row, new_col))

        score += len(nines)

    print(f"Part one: {score}")

    print(f"Part two: {rating}")
