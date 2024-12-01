#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys


def solve(day: int) -> None:
    try:
        module = importlib.import_module(f"advent.day{day:02}")
        module.solve()
    except ModuleNotFoundError:
        print(f"Day {day} not implemented")


def main() -> None:
    days = range(1, 26) if len(sys.argv) < 2 else (int(sys.argv[1]),)
    for day in days:
        print(f"Day {day}:")
        solve(day)
        print()


if __name__ == "__main__":
    main()
