from __future__ import annotations

from dataclasses import dataclass

from advent.utils import data_dir


@dataclass
class BlockRange:
    file_id: int | None
    length: int


def parse_data(data: str) -> list[BlockRange]:
    block_ranges = []
    file_id = 0
    empty = False
    for char in data:
        length = int(char)
        if empty:
            block_range = BlockRange(None, length)
        else:
            block_range = BlockRange(file_id, length)
            file_id += 1
        block_ranges.append(block_range)
        empty = not empty

    return block_ranges


def checksum(block_ranges: list[BlockRange]) -> int:
    checksum = 0

    position = 0
    for block_range in block_ranges:
        if block_range.file_id is not None:
            checksum += (
                block_range.file_id
                * ((2 * position + block_range.length - 1) * block_range.length)
                // 2
            )
        position += block_range.length

    return checksum


def solve_part_one(block_ranges: list[BlockRange]) -> int:
    index = 0
    while index < len(block_ranges):
        file_ = block_ranges[-1]
        if file_.file_id is None:
            block_ranges.pop()
            continue

        gap = block_ranges[index]
        if gap.file_id is not None:
            index += 1
            continue

        moved = min(gap.length, file_.length)
        if moved < gap.length:
            block_ranges.insert(index + 1, BlockRange(None, gap.length - moved))
        file_.length -= moved

        if file_.length == 0:
            block_ranges.pop()

        gap.file_id = file_.file_id
        gap.length = moved

        index += 1

    return checksum(block_ranges)


def find_gap(block_ranges: list[BlockRange], max_index: int, size: int) -> int | None:
    index = 0
    for index, gap in enumerate(block_ranges):
        if index >= max_index:
            break

        if gap.file_id is None and gap.length >= size:
            return index

    return None


def solve_part_two(block_ranges: list[BlockRange]) -> int:
    index = len(block_ranges) - 1
    file_id = len(block_ranges) // 2
    while file_id >= 0:
        while block_ranges[index].file_id != file_id:
            index -= 1

        file_ = block_ranges[index]

        gap_index = find_gap(block_ranges, index, file_.length)
        if gap_index is None:
            file_id -= 1
            continue

        gap = block_ranges[gap_index]
        new_gap_size = gap.length - file_.length

        if new_gap_size > 0:
            block_ranges.insert(gap_index + 1, BlockRange(None, new_gap_size))

        gap.file_id = file_.file_id
        gap.length = file_.length
        file_.file_id = None

        file_id -= 1

    return checksum(block_ranges)


def solve() -> None:
    puzzle = data_dir() / "day09.txt"
    data = puzzle.read_text(encoding="utf-8").strip()

    block_ranges = parse_data(data)
    part_one = solve_part_one(block_ranges)
    print(f"Part one: {part_one}")

    block_ranges = parse_data(data)
    part_two = solve_part_two(block_ranges)
    print(f"Part two: {part_two}")
