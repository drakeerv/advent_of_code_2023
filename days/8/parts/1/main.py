"""
One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

import re

total = 0
lines: list[str] = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line and lines[-1] == "":
        break

    lines.append(line)

lookup_table: dict[str, tuple[str, str]] = {}
current_node = None
goal_node = None
for line in lines[2:]:
    match = re.match(r"([a-zA-Z]{3}) = \(([a-zA-Z]{3}), ([a-zA-Z]{3})\)", line)
    if match:
        lookup_table[match.group(1)] = (match.group(2), match.group(3))
        if match.group(1) == "AAA":
            current_node = match.group(1)
        elif match.group(1) == "ZZZ":
            goal_node = match.group(1)

done = False
is_rights = [char == "R" for char in lines[0]]
while True:
    for is_right in is_rights:

        current_node = lookup_table[current_node][is_right]
        total += 1

        if current_node == goal_node:
            done = True
            break


    if done:
        break

print(total)
