"""
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""

import functools
import threading
import re
import math

lines: list[str] = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if line:
        lines.append(line)

seeds_numbers = [
    tuple(map(int, match.split(" "))) for match in re.findall(r"(\d+ \d+)+", lines[0])
]


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


@functools.cache
def get_soil(seed_number: int) -> int:
    """Get the soil number for a seed number."""
    return map_number(seed_number, seed_to_soil_map)


@functools.cache
def get_fertilizer(soil_number: int) -> int:
    """Get the fertilizer number for a soil number."""
    return map_number(soil_number, seed_to_fertilizer_map)


@functools.cache
def get_water(fertilizer_number: int) -> int:
    """Get the water number for a fertilizer number."""
    return map_number(fertilizer_number, fertilizer_to_water_map)


@functools.cache
def get_light(water_number: int) -> int:
    """Get the light number for a water number."""
    return map_number(water_number, water_to_light_map)


@functools.cache
def get_temperature(light_number: int) -> int:
    """Get the temperature number for a light number."""
    return map_number(light_number, light_to_temperature_map)


@functools.cache
def get_humidity(temperature_number: int) -> int:
    """Get the humidity number for a temperature number."""
    return map_number(temperature_number, temperature_to_humidity_map)


@functools.cache
def get_location(humidity_number: int) -> int:
    """Get the location number for a humidity number."""
    return map_number(humidity_number, humidity_to_location_map)


def get_location_from_seed(seed_number: int) -> int:
    """Get the location number for a seed number."""

    soil = map_number(seed_number, seed_to_soil_map)
    fertilizer = map_number(soil, seed_to_fertilizer_map)
    water = map_number(fertilizer, fertilizer_to_water_map)
    light = map_number(water, water_to_light_map)
    temperature = map_number(light, light_to_temperature_map)
    humidity = map_number(temperature, temperature_to_humidity_map)
    return map_number(humidity, humidity_to_location_map)


min_seed_number = math.inf


def find_min_location_thread(seed_number: int, seed_count: int) -> None:
    """Find the min location number for a seed number."""
    global min_seed_number

    min_seed_number = min(
        min_seed_number,
        *map(get_location_from_seed, range(seed_number, seed_number + seed_count)),
    )


threads = []
for seed_number, seed_count in seeds_numbers:
    thread = threading.Thread(
        target=find_min_location_thread, args=(seed_number, seed_count), daemon=True
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(min_seed_number)
