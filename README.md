# "dt" by @cloudsmith-io

DT: Debug Toolkit? Deep Thinking? Desperately Trying? Definitely Temporary? Dubious Technology? Maybe.

This is a mini-framework for solving coding puzzles. It runs on GitHub Codespaces, with little effort.

## Getting Started

Your objective, is to solve puzzles by editing the following files:

- `dt/01.py` - Day 1
- `dt/02.py` - Day 2

If you're solving [AoC puzzles](https://adventofcode.com/), you'll need to go there, and get the input for your puzzle, and then put it into one of the following places:

- `dt/input/01.txt` - Day 1 Input
- `dt/input/02.txt` - Day 2 Input

If you're playing multiplayer (everyone with their own solution), but sharing code, then you can put them in places like this:

- `dt/input/01.txt` - Day 1 Input (Team Lead)
- `dt/input/01a.txt` - Day 1 Input (Team Member A)
- `dt/input/01b.txt` - Day 1 Input (Team Member B)

Then, when running the CLI (see later on how), just pass `-i 01b.txt` to use the `01b.txt` input above.

## Python!?!

Alas, DT is only built to support the [Python programming language only](https://docs.python.org/3/) (sorry, NextJS-ish folks! <3)

Here's some resources to help you out, in addition to some awesome colleagues around you. :)

Downloadable Python Cheat Sheet:
[[!Python Cheat Sheet](https://media.datacamp.com/legacy/image/upload/v1673614099/Python_Cheat_Sheet_for_Beginners_f939d6b1bb.png)](https://media.datacamp.com/legacy/image/upload/v1694526244/Marketing/Blog/Python_Basics_Cheat_Sheet-updated.pdf)

Other Resources:

- [Online (More In-Depth) Cheat Sheet](https://www.pythoncheatsheet.org/cheatsheet/basics)
- [Solving Puzzles Like AoC](https://realpython.com/python-advent-of-code/)

P.S. NextJS folks: If it's too painful, just install nvm into the devcontainer. :)

## Executing the CLI

The CLI will:

- Run your solution for all days or the days you specify (comma-separated list).
- Provide the answers you generated, either example or real, for each day.
- Provide CPU and timing information for each day.
- Provide Source Lines of Code (SLOC) and the number of characters for each day.
- Tell you whether it was a "golden" solution, i.e., it took less than one second.
- Tell you whether _all_ together are "golden"; i.e., _all_ took less than one second.

Just run the following in the VSCode Terminal (`CMD/CTRL+SHIFT+'`):

```
python -m dt
```

You can get help and other options by passing in `-h`:

```
python -m dt -h
```

To run a specific day, just pass a number:

```
python -m dt 1
```

To force it to run with your example data instead of an input:

```
python -m dt 1 -e
```

## Executing Tests

If you'd like to execute your tests, you can pass `--test` to the CLI or execute `pytest`.

Just run the following in the VSCode Terminal (`CMD/CTRL+SHIFT+'`):

```
pytest
```

## Example: Solving AoC 2022 - Day 1

OK, so we'll solve Part 1 of [Day 1 of AoC 2022](https://adventofcode.com/2022/day/1) here, to show you what the process looks like.

### The Problem

Imagine you're helping Santa's elves organize their snacks. Each elf carries several snacks, and each snack has a number of calories. The elves wrote down their snacks like this:

```
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

Each elf's snacks are separated by blank lines. We need to find which elf is carrying the most calories total.

### The Solution

Here's how we can solve this in Python, with each step explained:

```
EXAMPLE = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def solve() -> int:
    """Count the calories."""
    # First, we'll read the elves' snack list; we're not really reading
    # from a file here (that would use `open()`), just using the EXAMPLE
    text = EXAMPLE

    # Split the text into groups (one group per elf).
    # The elves are separated by double newlines.
    elf_groups = text.split("\n\n")

    # For each elf, we'll add up their snacks, using a list variable.
    elf_totals = []

    # Iterate through each snack in the list
    for elf_snack in elf_snacks:
        # Split each elf's snacks into separate numbers
        calories = elf_snacks.split("\n")

        # Convert the strings to numbers and add them up
        total = sum(int(calorie) for calorie in calories if calorie)

        # Remember this elf's total
        elf_totals.append(total)

        # Find the elf carrying the most calories
        most_calories = max(elf_totals)

    return most_calories


# Use the function
result = solve()
print(f"The elf carrying the most calories has {result} calories!")
```

That's pretty much it. You can run it yourself by copying and pasting
the above to a file like `solution.py`, and running it like:

```
python solution.py
```

But, of course, it only solves the example, and only solves part 1. But
hopefully it gives you an idea of what this looks and feels like. :)

## Help!?!

Just ask the DMs for more help, if you're stuck with environment issues.

If you need help on puzzles, then you need to use a WTD signal + token.

## Have Fun

... And may the quack be with you.
