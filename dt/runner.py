"""
DT - Run All The Things.

You don't need to edit anything in this file (unless you want to!)
"""

from __future__ import annotations

import argparse
import ast
import dataclasses
import functools
import importlib
import inspect
import operator
import os
import pathlib
import sys
import textwrap
import time
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np
import psutil
import pytest
from rich.console import Console
from rich.table import Table
from rich_argparse import RichHelpFormatter

from . import utils


@dataclass
class PerfCounter:
    """Capture an inner block's execution time in nanoseconds, and cpu time."""

    elapsed: float = 0.0  # nanoseconds
    idle: float = 0.0
    iowait: float = 0.0
    irq: float = 0.0
    steal: float = 0.0
    system: float = 0.0
    user: float = 0.0

    __t1: float = 0.0
    __t2: float = 0.0
    __cpu: Any = field(default_factory=lambda: psutil.cpu_times_percent())
    __mem: float = 0.0

    def __enter__(self) -> PerfCounter:
        self.__t1 = self.__t2 = time.perf_counter_ns()
        self.__cpu = psutil.cpu_times_percent()  # Only for marking start
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.__t2 = time.perf_counter_ns()
        self.__cpu = psutil.cpu_times_percent()  # psutil handles delta
        self.elapsed = self.__t2 - self.__t1
        self.idle = self.__cpu.idle
        self.iowait = self.__cpu.iowait
        self.irq = self.__cpu.irq
        self.steal = self.__cpu.steal
        self.system = self.__cpu.system
        self.user = self.__cpu.user

    def __add__(self, other: PerfCounter) -> PerfCounter:
        return self.__operator__(operator.add, other)

    def __sub__(self, other: PerfCounter) -> PerfCounter:
        return self.__operator__(operator.sub, other)

    def __truediv__(self, other: PerfCounter | int | float) -> PerfCounter:
        return self.__operator__(operator.truediv, other)

    def __floordiv__(self, other: PerfCounter | int | float) -> PerfCounter:
        return self.__operator__(operator.floordiv, other)

    def __operator__(self, op: Callable, other: PerfCounter | int | float) -> PerfCounter:
        return PerfCounter(**{
            key: op(
                getattr(self, key),
                getattr(other, key) if isinstance(other, PerfCounter) else other,
            )
            for key in dataclasses.asdict(self)
            if not key.startswith("_")
        })


def generate_parser() -> argparse.ArgumentParser:
    """Generate the argument parser."""
    parser = argparse.ArgumentParser(
        prog="dt",
        description="Advent of Code: 2025 (@cloudsmith-io)",
        epilog="Ho Ho Ho!",
        formatter_class=RichHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        "puzzles",
        type=str,
        default="all",
        nargs="?",
        help="the puzzles to execute, split by commas (default: all)",
    )
    parser.add_argument(
        "-h", "--help", action="store_true", help="show this help message and exit."
    )
    parser.add_argument(
        "-d",
        "--debug-path",
        default=None,
        nargs="?",
        help="debug the file path (and only execute *that* puzzle)",
    )
    parser.add_argument(
        "-e", "--example", default=False, action="store_true", help="use example inputs."
    )
    parser.add_argument(
        "-p",
        "--profile",
        nargs="?",
        const=10,
        type=int,
        help="execute tests multiple times (default: 10) to get better performance statistics.",
    )
    parser.add_argument(
        "-P",
        "--percentile",
        nargs="?",
        default=5,
        type=int,
        help="for profiling, remove outliers beyond the nth percentile (default: 5).",
    )
    parser.add_argument(
        "-s",
        "--suppress-output",
        default=False,
        action="store_true",
        help="suppress the results output.",
    )
    parser.add_argument(
        "-r",
        "--redact",
        default=False,
        action="store_true",
        help="redact the solution values.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        help="disables output, colours and any interactive elements.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=None,
        help="use an alternative input file (e.g. 'a' -> '01a.txt')",
    )
    parser.add_argument(
        "-t",
        "--test",
        default=False,
        action="store_true",
        help="execute tests (same as running 'pytest')",
    )
    return parser


def ns_to_s(ns: float | int) -> float:
    """Convert nanoseconds to seconds."""
    return round(ns / 1000000000.0, 6)


def yes_no(value: bool) -> str:
    """Convert boolean to a yes/no."""
    return ":star:" if value else "-"


def maybe_redact(value: str, redact: bool) -> str:
    """Maybe redact a value if asked to."""
    return "[dim grey]<redact>[/dim grey]" if redact else value


def purify_source(source: str) -> str:
    """Strip comments and other unneeded parts from source code."""
    return ast.unparse(ast.parse(source))


def run() -> None:  # noqa: C901
    """Execute the runner."""
    parser = generate_parser()
    args = parser.parse_args(sys.argv[1:])
    console = Console(force_interactive=False if args.quiet else None)

    if args.help:
        parser.print_help()
        return

    if args.debug_path:
        args.puzzles = os.path.basename(args.debug_path.rstrip(".py"))

    puzzles = [
        str(int(s)).zfill(2)
        for s in (range(1, 26) if args.puzzles == "all" else args.puzzles.split(","))
    ]

    if args.test:
        # Execute pytest, but only with the puzzles specified
        pytest.main([
            f"dt/{puzzle}.py" for puzzle in puzzles if os.path.exists(f"dt/{puzzle}.py")
        ])
        return

    # Import all modules and read all inputs, upfront
    modules = {}
    inputs = {}
    for puzzle in puzzles:
        try:
            modules[puzzle] = importlib.import_module(f".{puzzle}", __package__)
            inputs[puzzle] = utils.read_input(puzzle, suffix=args.input)
        except ImportError as exc:
            path = pathlib.Path(__file__).parent.resolve()
            filepath = path / f"{puzzle}.py"
            if os.path.exists(filepath):
                console.print(f"[red]Error importing puzzle {puzzle} ({filepath}):[/red]")
                console.print(f"[red][b]{exc}[/b][/red]")
                console.print()
                console.print("Check your code for syntax errors, then try again.")
                return

    if args.suppress_output:
        for puzzle, module in modules.items():
            module.solve(data=inputs[puzzle] if not args.example else None)
        return

    table = Table(
        caption_style="on navy_blue",
        row_styles=["", "bold"],
    )
    table.add_column("puzzle", justify="right", style="bold cyan", no_wrap=True)
    table.add_column("p1", style="magenta")
    table.add_column("p2", style="green")
    table.add_column("cpu", justify="left", style="red")
    table.add_column("sloc", justify="right", style="yellow")
    table.add_column("chars", justify="right", style="yellow")
    table.add_column("t/seconds", justify="right", style="blue")
    table.add_column("t<1", justify="center", style="not dim bold gold3")

    if args.profile:
        percentile = max(1, min(25, args.percentile))  # 75th to 99th percentile
        table.caption = " ".join(
            textwrap.dedent(
                f"""
                [b red][yellow]Note:[/yellow] Profiling averaged
                over {args.profile} run(s)
                /w <{percentile},>{100 - percentile} percentile removed :rocket:
                """
            ).splitlines()
        )

    total_seconds = 0.0
    total_sloc = 0
    total_chars = 0

    def _add_row(
        puzzle: str | None,
        p1: int | None,
        p2: int | None,
        pc: PerfCounter | None,
        sloc: int,
        chars: int,
        seconds: float,
    ) -> None:
        """Add a row to the table."""
        row = [
            puzzle if puzzle else "total",
            maybe_redact(str(p1), args.redact) if p1 is not None else "",
            maybe_redact(str(p2), args.redact) if p2 is not None else "",
            f"user {pc.user:0.2f}%, sys {pc.system:0.2f}%" if pc else "",
        ]

        row.extend([
            str(sloc),
            str(chars),
            f"{seconds:.6f}".ljust(8, "0"),
            yes_no(seconds < 1),
        ])

        table.add_row(*row)

    with console.status("[bold green]Solving ...") as status:
        for puzzle, module in modules.items():
            counters = []
            once = not args.profile
            max_attempts = 1 if once else args.profile
            for _ in range(max_attempts):
                attempt = "" if once else f"(profiling {_ + 1} of {max_attempts})"
                with PerfCounter() as pc:
                    counters.append(pc)
                    status.update(f"[bold green]Solving puzzle {puzzle} {attempt}...")
                    p1, p2 = module.solve(
                        data=inputs[puzzle] if not args.example else None
                    )
            if len(counters) > 2:
                # For "fairness" (subjective), we remove the interquartile range (IQR) of
                # the timings, and then average the rest.
                elapsed = np.array([counter.elapsed for counter in counters])
                lower, upper = np.percentile(elapsed, [percentile, 100 - percentile])
                counters = [
                    counter for counter in counters if lower <= counter.elapsed <= upper
                ]
            pc = functools.reduce(operator.add, counters) / len(counters)
            day_seconds = ns_to_s(pc.elapsed)
            source = purify_source(inspect.getsource(module))
            sloc = source.count("\n") + 1
            chars = len(source)

            _add_row(puzzle, p1, p2, pc, sloc, chars, day_seconds)

            total_seconds += day_seconds
            total_sloc += sloc
            total_chars += chars

    # Add the total row
    _add_row(None, None, None, None, total_sloc, total_chars, total_seconds)

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":  # pragma: no cover
    run()
