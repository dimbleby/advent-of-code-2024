from __future__ import annotations

from advent.utils import data_dir


def solve() -> None:
    puzzle = data_dir() / "day04.txt"
    data = puzzle.read_text(encoding="utf-8")

    rows = data.splitlines()
    columns = ["".join(row) for row in zip(*data.splitlines(), strict=True)]

    num_rows = len(rows)
    num_cols = len(columns)

    positives: list[str] = []
    for total in range(num_rows + num_cols - 1):
        min_row = max(0, total + 1 - num_cols)
        max_row = min(total + 1, num_rows)
        line = "".join(rows[i][total - i] for i in range(min_row, max_row))
        positives.append(line)

    negatives: list[str] = []
    for diff in range(-num_rows + 1, num_cols):
        min_row = max(0, -diff)
        max_row = min(num_cols - diff, num_rows)
        line = "".join(rows[i][i + diff] for i in range(min_row, max_row))
        negatives.append(line)

    count = 0
    for line in (*rows, *columns, *positives, *negatives):
        count += line.count("XMAS")
        count += line.count("SAMX")

    print(f"Part one: {count}")

    count = 0
    for row in range(num_rows - 2):
        for col in range(num_cols - 2):
            if rows[row + 1][col + 1] != "A":
                continue

            d1 = {rows[row][col], rows[row + 2][col + 2]}
            if d1 != {"M", "S"}:
                continue

            d2 = {rows[row + 2][col], rows[row][col + 2]}
            if d2 != {"M", "S"}:
                continue

            count += 1

    print(f"Part two: {count}")
