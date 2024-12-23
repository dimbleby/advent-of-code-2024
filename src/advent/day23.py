from __future__ import annotations

import itertools
from collections import defaultdict
from typing import TYPE_CHECKING

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator

type Node = str


def bron_kerbosch(graph: dict[Node, set[Node]]) -> Iterator[set[Node]]:
    stack = [(set[Node](), set(graph), set[Node]())]
    while stack:
        r, p, x = stack.pop()
        if not p and not x:
            yield r
            continue

        pivot = next(iter(p | x))
        for v in p - graph[pivot]:
            stack.append((r | {v}, p & graph[v], x & graph[v]))
            p.remove(v)
            x.add(v)


def solve() -> None:
    puzzle = data_dir() / "day23.txt"
    data = puzzle.read_text()

    graph = defaultdict(set)
    for line in data.splitlines():
        n1, n2 = line.split("-")
        graph[n1].add(n2)
        graph[n2].add(n1)

    triangles = set()
    for node, neighbours in graph.items():
        if not node.startswith("t"):
            continue

        for n1, n2 in itertools.combinations(neighbours, 2):
            if n2 in graph[n1]:
                triangle = "-".join(sorted([node, n1, n2]))
                triangles.add(triangle)

    part_one = len(triangles)
    print(f"Part one: {part_one}")

    max_cliques = bron_kerbosch(graph)
    biggest_clique = max(max_cliques, key=len)
    part_two = ",".join(sorted(biggest_clique))
    print(f"Part two: {part_two}")
