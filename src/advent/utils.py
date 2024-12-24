from __future__ import annotations

import importlib.resources
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Self, override

if TYPE_CHECKING:
    from collections.abc import Collection, Hashable, Iterable, Iterator, Mapping
    from importlib.resources.abc import Traversable
    from typing import Self


def data_dir() -> Traversable:
    return importlib.resources.files(__package__) / "data"


class SupportsChunking(Protocol):
    def __getitem__(self, index: slice, /) -> Self: ...

    def __len__(self) -> int: ...


def chunks[T: SupportsChunking](seq: T, n: int) -> Iterator[T]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


type Coord2 = tuple[int, int]
type Coord3 = tuple[int, int, int]


def manhattan(here: Iterable[int], there: Iterable[int]) -> int:
    return sum(abs(h - t) for h, t in zip(here, there, strict=True))


@dataclass
class Vec2:
    x: int
    y: int

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vec2) -> Self:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2) -> Self:
        self.x -= other.x
        self.y -= other.y
        return self

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2):
            return False

        return self.x == other.x and self.y == other.y

    @override
    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Vec3:
    x: int
    y: int
    z: int

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Vec3) -> Self:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Vec3) -> Self:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, n: int) -> Vec3:
        return Vec3(self.x * n, self.y * n, self.z * n)

    def __rmul__(self, n: int) -> Vec3:
        return Vec3(n * self.x, n * self.y, n * self.z)

    def __imul__(self, n: int) -> Self:
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __floordiv__(self, n: int) -> Vec3:
        return Vec3(self.x // n, self.y // n, self.z // n)

    def __ifloordiv__(self, n: int) -> Self:
        self.x //= n
        self.y //= n
        self.z //= n
        return self

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - other.y * self.z,
            self.z * other.x - other.z * self.x,
            self.x * other.y - other.x * self.y,
        )

    def dot(self, other: Vec3) -> int:
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass
class UnionFind[T: Hashable]:
    parents: dict[T, T]
    ranks: dict[T, int]

    @staticmethod
    def from_elements(things: Iterable[T]) -> UnionFind[T]:
        parents = {thing: thing for thing in things}
        ranks = dict.fromkeys(things, 0)
        return UnionFind(parents, ranks)

    def find(self, k: T) -> T:
        root = k
        while root != (parent := self.parents[root]):
            root = parent

        while root != (parent := self.parents[k]):
            self.parents[k] = root
            k = parent

        return root

    def union(self, a: T, b: T) -> bool:
        x = self.find(a)
        y = self.find(b)

        if x == y:
            return False

        xrank, yrank = self.ranks[x], self.ranks[y]
        if xrank < yrank:
            self.parents[x] = y
        else:
            self.parents[y] = x

            if xrank == yrank:
                self.ranks[x] = xrank + 1

        return True


def topological_sort[T](
    dependencies: Mapping[T, list[T]], unordered: Collection[T]
) -> list[T]:
    order = []

    in_degrees = dict.fromkeys(unordered, 0)
    for before in unordered:
        for after in dependencies[before]:
            if after in in_degrees:
                in_degrees[after] += 1

    queue = deque(n for n in unordered if in_degrees[n] == 0)
    while queue:
        before = queue.popleft()
        order.append(before)
        for after in dependencies[before]:
            if after not in in_degrees:
                continue

            in_degrees[after] -= 1
            if in_degrees[after] == 0:
                queue.append(after)

    return order
