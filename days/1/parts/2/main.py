"""
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""

total = 0
numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def find_first_num(line: str) -> str | None:
    """
    Find the first number in a string.
    """

    line = line.lower()
    keys = list(numbers.keys())

    substring = ""

    for char in line:
        if char.isdigit():
            return char

        if char.isalpha():
            substring += char

            for key in keys:
                if key in substring:
                    return str(numbers[key])
    return None

def find_last_num(line: str) -> str | None:
    """
    Find the last number in a string.
    """

    line = line.lower()
    keys = list(numbers.keys())

    substring = ""

    for i in range(len(line) - 1, -1, -1):
        char = line[i]

        if char.isdigit():
            return char

        if char.isalpha():
            substring = char + substring

            for key in keys:
                if key in substring:
                    return str(numbers[key])
    return None

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    first = find_first_num(line)
    last = find_last_num(line)

    if first and last:
        total += int(first + last)

print(total)