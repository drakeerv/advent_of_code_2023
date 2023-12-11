"""
Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
"""

# We can represent a pipe as such:
# .0.
# 1.2
# .3.

PIPES = {
    "|": (0, 3),
    "-": (1, 2),
    "L": (0, 2),
    "J": (0, 1),
    "7": (3, 1),
    "F": (3, 2),
    "S": (0, 1, 2, 3)
}

lines: list[str] = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    lines.append(line.replace(".", " "))

# find S
start_y = 0
start_x = 0
for line_index, line in enumerate(lines):
    if "S" in line:
        start_line = line_index
        start_column = line.index("S")
        break

# find the loop
def find_adjacent_pipes(x: int, y: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []

    # up
    if y > 0:
        if lines[y - 1][x] != " ":
            result.append((x, y - 1))

    # down
    if y < len(lines) - 1:
        if lines[y + 1][x] != " ":
            result.append((x, y + 1))

    # left
    if x > 0:
        if lines[y][x - 1] != " ":
            result.append((x - 1, y))

    # right
    if x < len(lines[y]) - 1:
        if lines[y][x + 1] != " ":
            result.append((x + 1, y))

    return result

def find_connected_pipes(x: int, y: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []

    adjacent_pipes = find_adjacent_pipes(x, y)
    my_pipe = PIPES[lines[y][x]]

    for pipe in adjacent_pipes:
        other_x, other_y = pipe

        if other_y == y - 1 and other_x == x:
            if 0 in my_pipe and 3 in PIPES[lines[other_y][other_x]]:
                result.append(pipe)
        elif other_y == y + 1 and other_x == x:
            if 3 in my_pipe and 0 in PIPES[lines[other_y][other_x]]:
                result.append(pipe)
        elif other_y == y and other_x == x - 1:
            if 1 in my_pipe and 2 in PIPES[lines[other_y][other_x]]:
                result.append(pipe)
        elif other_y == y and other_x == x + 1:
            if 2 in my_pipe and 1 in PIPES[lines[other_y][other_x]]:
                result.append(pipe)
        

    return result

pipes: list[tuple[int, int]] = [(start_column, start_line), find_connected_pipes(start_column, start_line)[0]]

while len(pipes) == 1 or pipes[-1] != (start_column, start_line):
    x, y = pipes[-1]
    connected_pipes = find_connected_pipes(x, y)

    if len(pipes) > 1:
        connected_pipes.remove(pipes[-2])

    pipes.append(connected_pipes[0])

print(len(pipes) // 2)