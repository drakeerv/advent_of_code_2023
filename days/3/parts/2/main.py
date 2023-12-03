"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

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

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
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

# Delete all symbols except *
lines = [re.sub(r"[@./=\-$&+#%]", " ", line) for line in lines]
values = [[[] for _ in range(len(lines[0]))] for _ in range(len(lines))]

def find_symbols(y: int, xmin: int, xmax: int, number: int) -> None:
    global values

    """
    Look for a symbol in the engine schematic around the given coordinates.
    ####
    #XX#
    ####
    """

    # Check the line above
    if y > 0:
        finds = re.finditer(r"\*", lines[y - 1][xmin:xmax])
        for find in finds:
            if values[find.start() + xmin][y - 1] == []:
                values[find.start() + xmin][y - 1] = [number]
            else:
                values[find.start() + xmin][y - 1].append(number)

    # Check the line below
    if y < len(lines) - 1:
        finds = re.finditer(r"\*", lines[y + 1][xmin:xmax])
        for find in finds:
            if values[find.start() + xmin][y + 1] == []:
                values[find.start() + xmin][y + 1] = [number]
            else:
                values[find.start() + xmin][y + 1].append(number)

    # Check the line itself
    if lines[y][xmin] == "*":
        if values[xmin][y] == []:
            values[xmin][y] = [number]
        else:
            values[xmin][y].append(number)

    if lines[y][xmax - 1] == "*":
        if values[xmax - 1][y] == []:
            values[xmax - 1][y] = [number]
        else:
            values[xmax - 1][y].append(number)
    

# Iterate over all lines
for y, line in enumerate(lines):
    numbers = re.finditer(r"\d+", line)

    for number in numbers:
        xmin = max(0, number.start() - 1)
        xmax = min(len(line) - 1, number.end() + 1)

        find_symbols(y, xmin, xmax, int(number.group()))

# flatten values and remove all values that are not adjacent to exactly two part numbers
values = [value for sublist in values for value in sublist if len(value) == 2]

# calculate the gear ratio of every gear and add them all up
for value in values:
    total += value[0] * value[1]

print(total)