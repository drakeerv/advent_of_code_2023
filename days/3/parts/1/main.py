"""
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

import re

total = 0
lines: list[str] = []

# Read all lines from stdin
while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    lines.append(line)

# Convert all symbols to * and remove all periods
lines = [re.sub(r"[@*/=\-$&+#%]", "*", line.replace(".", " ")) for line in lines]


def look_for_symbol(y: int, xmin: int, xmax: int) -> bool:
    """
    Look for a symbol in the engine schematic around the given coordinates.
    ####
    #XX#
    ####
    """

    # Check the line above
    if y > 0:
        if lines[y - 1][xmin:xmax].find("*") != -1:
            return True

    # Check the line below
    if y < len(lines) - 1:
        if lines[y + 1][xmin:xmax].find("*") != -1:
            return True

    # Check the line itself
    if lines[y][xmin] == "*" or lines[y][xmax - 1] == "*":
        return True

    return False
    

# Iterate over all lines
for y, line in enumerate(lines):
    numbers = re.finditer(r"\d+", line)

    for number in numbers:
        xmin = max(0, number.start() - 1)
        xmax = min(len(line) - 1, number.end() + 1)

        if look_for_symbol(y, xmin, xmax):
            total += int(number.group())

print(total)
