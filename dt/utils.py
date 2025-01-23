"""
DT - Utilities.

You don't need to edit anything in this file (unless you want to!)
"""

from __future__ import annotations

import pathlib


def read_input(day: str, suffix: str | None) -> str:
    """Read input for a day in."""
    path = pathlib.Path(__file__).parent.resolve()
    suffix = suffix or ""
    filename = f"{day}{suffix}.txt"
    with open(path / f"input/{filename}") as f:
        return f.read().strip()
