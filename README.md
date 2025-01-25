# "dt" by @cloudsmith-io

DT: Debug Toolkit? Deep Thinking? Desperately Trying? Definitely Temporary? Dubious Technology? Maybe.

This is a mini-framework for solving coding puzzles. It runs on GitHub Codespaces with little effort.

## Getting Started

Your objective is to solve puzzles by editing the following files:

- `dt/01.py` - Day 1
- `dt/02.py` - Day 2

If you're solving [AoC puzzles](https://adventofcode.com/), you'll need to go there, get the input for your puzzle, and then put it into one of the following places:

- `dt/input/01.txt` - Day 1 Input
- `dt/input/02.txt` - Day 2 Input

If you're playing multiplayer (everyone with their solution) but sharing code, then you can put them in places like this:

- `dt/input/01.txt` - Day 1 Input (Team Lead)
- `dt/input/01a.txt` - Day 1 Input (Team Member A)
- `dt/input/01b.txt` - Day 1 Input (Team Member B)

Then, when running the CLI (see later on how), just pass `-i a` to use the `01a.txt` input above (or `-i b` to use `01b.txt`, etc.)

## Python!?!

Alas, DT is only built to support the [Python programming language only](https://docs.python.org/3/) (sorry, NextJS-ish folks! <3)

Here are some resources to help you on your merry way:

- [Downloadable Python Cheat Sheet](https://github.com/ehmatthes/pcc_3e/releases/download/v1.0.0/beginners_python_cheat_sheet_pcc_all.pdf)
- [Online (More In-Depth) Cheat Sheet](https://www.pythoncheatsheet.org/cheatsheet/basics)
- [Solving Puzzles Like AoC](https://realpython.com/python-advent-of-code/)

There's also a full example of solving a puzzle down below.

You can always ask those most excellent colleagues around you, too (and the DMs!)

P.S. NextJS folks: If it's too painful, install nvm into the devcontainer. :)

### Basic String Operations

Some helpful pointers on string operations:

```python
# String indexing (first character is position 0)
text = "hello"
first_char = text[0]  # 'h'
last_char = text[-1]  # 'o'

# String slicing (get parts of string)
part = text[1:4]  # 'ell'

# String counting
count = text.count('l')  # 2

# String comparison
text1 = "cat"
text2 = "dog"
are_same = text1 == text2  # False

# Split string into parts
text = "a,b,c"
parts = text.split(',')  # ['a', 'b', 'c']

# Join parts into string
joined = '-'.join(['x', 'y', 'z'])  # 'x-y-z'
```

### List/Number Operations

Some helpful pointers on list/number operations:

```python
# List comparisons
numbers = [1, 2, 3, 4]
for i in range(1, len(numbers)):
    if numbers[i] > numbers[i-1]:
        print(f"{numbers[i]} is bigger than {numbers[i-1]}")

# Sliding window (look at groups of numbers)
window_size = 3
for i in range(len(numbers) - window_size + 1):
    window = numbers[i:i + window_size]
    print(f"Window: {window}")
```

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

### It Doesn't Work :(

If any of the above doesn't work, it's probably because it is the first time
you have opened the GitHub Codespaces or VSCode. Just open a new terminal, or
reload the GitHub Codespaces (or VSCode).

## Executing Tests

If you'd like to execute your tests, you can pass `--test` to the CLI or execute `pytest`.

Just run the following in the VSCode Terminal (`CMD/CTRL+SHIFT+'`):

```
pytest
```

## Example: Solving AoC 2022 - Day 1

OK, so we'll solve Part 1 of [Day 1 of AoC 2022](https://adventofcode.com/2022/day/1) here, to show you what the process looks like.

### The Problem

Imagine you're helping Santa's elves organize their groups of snacks by total calories. Each elf carries several snacks, and each snack has a number of calories. The elves wrote down their snacks like this:

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

OK, so we need to:

- Read the groups of elf snacks (their calories).
- Calculate a total for each of the groups (one per elf).
- Find out which is the greatest total.
- Use that total as the answer.

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
    for elf_snacks in elf_groups:
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

That's pretty much it.

You can run it yourself by copying and pasting the above to a file like
`solution.py`, and running it like:

```
python solution.py
```

It _should_ say:

"The elf carrying the most calories has 24000 calories!"

But, of course, it only solves the example, and only solves part 1. But
hopefully, it gives you an idea of what solving a puzzle looks and feels like.

## Help!?!

Just ask the DMs for more help if you're stuck with environmental issues.

If you need help with puzzles, then you need to use a WTD signal + token.

## Have Fun

... And may the quack be with you.
