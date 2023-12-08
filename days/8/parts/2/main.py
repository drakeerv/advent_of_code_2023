"""
After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?
"""

import re
import math
import functools

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

intermediary_table: dict[str, tuple[int, str, str]] = {}
for index, line in enumerate(lines[2:]):
    match = re.match(r"([a-zA-Z0-9]{3}) = \(([a-zA-Z0-9]{3}), ([a-zA-Z0-9]{3})\)", line)
    if match:
        intermediary_table[match.group(1)] = (int(index), str(match.group(2)), str(match.group(3)))

lookup_table: list[tuple[int, int]] = []
goal_nodes = set()
current_nodes = set()
for node, (index, left, right) in intermediary_table.items():
    lookup_table.append((intermediary_table[left][0], intermediary_table[right][0]))

    if node.endswith("A"):
        current_nodes.add(index)
    elif node.endswith("Z"):
        goal_nodes.add(index)

is_rights = [char == "R" for char in lines[0]]
totals = []
while True:
    for is_right in is_rights:
        current_nodes = {lookup_table[int(node)][int(is_right)] for node in current_nodes}
        total += 1

        totals += [total for _ in current_nodes.intersection(goal_nodes)]
        current_nodes = current_nodes.difference(goal_nodes)

        if not current_nodes:
            break

    if not current_nodes:
        break

def lcm(a, b):
    """Least common multiple of two integers."""
    return a * b // math.gcd(a, b)

print(functools.reduce(lcm, totals))
