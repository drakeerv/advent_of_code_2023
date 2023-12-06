"""
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""

import threading
import re
import math

lines: list[str] = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line and lines[-1] == line:
        break
    lines.append(line)

# parse the seeds
seeds_numbers = [
    tuple(map(int, match.split(" "))) for match in re.findall(r"(\d+ \d+)+", lines[0])
]

# convert it to start and end
seeds_numbers = [
    (start, start + length) for start, length in seeds_numbers
]

# helper function
def is_overlapping(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    """Check if two ranges are overlapping."""
    return range1[0] <= range2[0] <= range1[1] or range2[0] <= range1[0] <= range2[1]

# condense overlapping ranges of seeds
new_seeds_numbers: list[tuple[int, int]] = [seeds_numbers[0]]

for seed_start, seed_end in seeds_numbers[1:]:
    extended_range = False

    for i, (start, end) in enumerate(new_seeds_numbers):
        if is_overlapping((seed_start, seed_end), (start, end)):
            new_seeds_numbers[i] = (min(start, seed_start), max(end, seed_end))
            extended_range = True
            break

    if not extended_range:
        new_seeds_numbers.append((seed_start, seed_end))
        
def parse_section(section_name: str) -> list[tuple[int, int, int]]:
    """Parse a section of the input file."""

    return [
        tuple(map(int, number_str.split(" ")))
        for number_str in re.search(
            rf"{section_name}:\n((?:\d+ \d+ \d+\n)+)", "\n".join(lines)
        )
        .group(1)
        .split("\n")
        if number_str
    ]


seed_to_soil_map = parse_section("seed-to-soil map")
seed_to_fertilizer_map = parse_section("soil-to-fertilizer map")
fertilizer_to_water_map = parse_section("fertilizer-to-water map")
water_to_light_map = parse_section("water-to-light map")
light_to_temperature_map = parse_section("light-to-temperature map")
temperature_to_humidity_map = parse_section("temperature-to-humidity map")
humidity_to_location_map = parse_section("humidity-to-location map")


def map_number(number: int, map_: list[tuple[int, int, int]]) -> int:
    """Map a number using a map."""
    for destination_start, source_start, length in map_:
        if source_start <= number < source_start + length:
            return destination_start + number - source_start

    return number


def get_location_from_seed(seed_number: int) -> int:
    """Get the location number for a seed number."""

    soil = map_number(seed_number, seed_to_soil_map)
    fertilizer = map_number(soil, seed_to_fertilizer_map)
    water = map_number(fertilizer, fertilizer_to_water_map)
    light = map_number(water, water_to_light_map)
    temperature = map_number(light, light_to_temperature_map)
    humidity = map_number(temperature, temperature_to_humidity_map)
    return map_number(humidity, humidity_to_location_map)


min_location_number = math.inf


def find_min_location_thread(start: int, end: int) -> None:
    """Find the min location number for a seed number."""
    global min_location_number

    SKIP_AMOUNT = 100

    # SKIP a certain amount of seeds and see if the distance is smaller or bigger than expected to then redo the search in that area. We then repeat this process until we find the min location number for the seed range.

    current_number = start
    previous_location_number = get_location_from_seed(current_number)

    if previous_location_number < min_location_number:
        min_location_number = previous_location_number
        print(min_location_number)

    for skip_i in range(start, end, SKIP_AMOUNT):
        location_number = get_location_from_seed(skip_i)

        # get the distance between the current location number
        distance = location_number - previous_location_number

        if distance != SKIP_AMOUNT:
            for i in range(current_number, skip_i):
                location_number = get_location_from_seed(i)

                if location_number < min_location_number:
                    min_location_number = location_number
                    print(min_location_number)

        previous_location_number = location_number
        current_number = skip_i


threads: list[threading.Thread] = []
for start, end in seeds_numbers:
    thread = threading.Thread(
        target=find_min_location_thread, args=(
            start, end), daemon=True
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(min_location_number)
