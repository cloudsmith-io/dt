"""
DT - Day 02.

You need to edit this file to solve the puzzle. :)
"""
from __future__ import annotations

from . import utils


EXAMPLE = """
DELETE_THIS_AND_PASTE_EXAMPLE_HERE
""".strip()  # this gets rid of leading/trailing spaces


# If you put data in input/02.txt, then solve() here will
# automatically be given it in `data` as an argument.
def solve(data: str | None = None) -> tuple[int, int]:
    """Solve the problem (change this docstring to describe what you're solving)."""
    # See dt/utils.py to see what reading a file looks like:
    data = data or EXAMPLE
    p1, p2 = 0, 0
    return p1, p2  # return answer for part 1, and part 2


def test_solve() -> None:
    assert solve() == (0, 0)
