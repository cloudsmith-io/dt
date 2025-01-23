"""
DT - Utilities.

You don't need to edit anything in this file (unless you want to!)
"""
from __future__ import annotations

import pathlib


def read_input(day: str) -> list[str]:
    """Read input for a day in."""
    path = pathlib.Path(__file__).parent.resolve()
    with open(path / f"input/{day}.txt") as f:
        return f.read().strip()

