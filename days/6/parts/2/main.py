"""
As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200

...now instead means this:

Time:      71530
Distance:  940200

Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?
"""

import math
import re

lines: list[str] = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    lines.append(line)

# get the first line using regex
total_time = int("".join(re.findall(r"\d+", lines[0])))
best_distance = int("".join(re.findall(r"\d+", lines[1])))

min_time = math.ceil(
    (-total_time + math.sqrt((total_time * total_time) - (4 * best_distance))) / -2
)
length = (total_time - min_time) - min_time + 1

print(length)
