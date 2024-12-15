from __future__ import annotations

from collections import Counter, defaultdict

from advent.utils import UnionFind, data_dir

NORTH = -1
SOUTH = 1
EAST = 1j
WEST = -1j


def solve() -> None:
    puzzle = data_dir() / "day12.txt"
    data = puzzle.read_text()

    grid = {
        complex(r, c): char
        for r, line in enumerate(data.splitlines())
        for c, char in enumerate(line)
    }

    uf = UnionFind.from_elements(grid)
    for plot, value in grid.items():
        for direction in [NORTH, EAST]:
            neighbour = plot + direction
            new_value = grid.get(neighbour)
            if value == new_value:
                uf.union(plot, neighbour)

    regions = defaultdict(set)
    for plot in grid:
        regions[uf.find(plot)].add(plot)

    fences = defaultdict(set)
    for region, plots in regions.items():
        for plot in plots:
            for direction in [NORTH, EAST, SOUTH, WEST]:
                neighbour = plot + direction
                if neighbour not in plots:
                    fences[region].add((plot, direction))

    part_one = sum(
        len(plots) * len(fences[region]) for region, plots in regions.items()
    )

    print(f"Part one: {part_one}")

    corners: Counter[complex] = Counter()
    for region, edges in fences.items():
        for plot, direction in edges:
            step = direction * 1j
            neighbour = plot + step
            if (neighbour, direction) not in edges:
                corners[region] += 1

    part_two = sum(len(plots) * corners[region] for region, plots in regions.items())
    print(f"Part two: {part_two}")
