"""
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?
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

# find the area by shooting a ray from the start point
area = 0

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if (x, y) in pipes:
            continue

        crosses = 0
        x2, y2 = x, y

        while x2 < len(line) and y2 < len(lines):
            c2 = lines[y2][x2]
            if (x2, y2) in pipes and c2 != "L" and c2 != "7":
                crosses += 1
            x2 += 1
            y2 += 1

        if crosses % 2 == 1:
            area += 1
            
print(area)