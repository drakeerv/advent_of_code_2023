"""
As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
"""

total = 0

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    first = None
    last = None
    for char in line:
        if char.isdigit():
            if not first:
                first = char
            last = char

    if first and last:
        total += int(first + last)

print(total)
