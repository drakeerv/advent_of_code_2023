"""
There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged records.

In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1

However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1

Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.

In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.

The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.

The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#

In this example, the number of possible arrangements for each row is:

    ???.### 1,1,3 - 1 arrangement
    .??..??...?##. 1,1,3 - 4 arrangements
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
    ????.#...#... 4,1,1 - 1 arrangement
    ????.######..#####. 1,6,5 - 4 arrangements
    ?###???????? 3,2,1 - 10 arrangements

Adding all of the possible arrangement counts together produces a total of 21 arrangements.

For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?
"""

total = 0

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    record1, record2 = line.split(" ")
    record2 = list(map(int, record2.split(",")))

    def find_possible(length: int) -> list:
        """Find all possible positions of a string of length length in record1"""
        possible = []

        for index in range(len(record1)):
            prev_index = index - 1
            if prev_index >= 0:
                if record1[prev_index] == "#":
                    continue

            count = 0
            for i in range(length):
                next_index = index + i
                if next_index >= len(record1):
                    break

                next_char = record1[next_index]
                if next_char in "#?":
                    count += 1

            if count == length:
                next_index = index + length
                if next_index < len(record1):
                    if record1[next_index] == "#":
                        continue
                possible.append(index)

        return possible

    possible_positions = list(map(find_possible, record2))
    new_possible_positions = [possible_positions[0]]

    for positions in range(1, len(possible_positions)):
        # get the max of the previous
        prev_min = min(new_possible_positions[-1])

        # now we can get rid of all the values equal to or lower than prev_min
        new_possible_positions.append(
            list(filter(lambda x: x > prev_min, possible_positions[positions]))
        )

    possible_positions = new_possible_positions
    new_possible_positions = [possible_positions[-1]]

    # now we can work backwards
    for positions in range(len(possible_positions) - 2, -1, -1):
        # get the max of the previous
        prev_max = max(new_possible_positions[-1])

        # now we can get rid of all the values equal to or lower than prev_min
        new_possible_positions.append(
            list(filter(lambda x: x < prev_max, possible_positions[positions]))
        )

    possible_positions = new_possible_positions[::-1]

    # now we can get the total by trying all the possible positions and seeing if they are at least a space away from each other
    def recursive(index: int = 0, prev_position: int | None = None) -> int:
        count = 0

        if index == len(possible_positions):
            return 1

        for position in possible_positions[index]:
            if prev_position is not None:
                if position - prev_position <= 1:
                    continue

            count += recursive(index + 1, position)

        return count

    total += recursive()

print(total)
