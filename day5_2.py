import os
import time
from itertools import takewhile

from icecream import ic
from utils import read_input_file
from multiprocessing import Pool

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Seeds:
    def __init__(self):
        self.seeds = []

    def add_line(self, seeds: str):
        self.seeds = [int(seed) for seed in seeds.split()]

    def __iter__(self):
        return self.seeds

    def __str__(self):
        return ' '.join([str(number) for number in self.seeds])


class RangeSeeds:
    def __init__(self):
        self.seeds = []

    def add_line(self, line):
        for start, length in zip(line.split()[0::2], line.split()[1::2]):
            self.seeds.append((start, length))

    def number_of_seeds(self) -> int:
        return sum([int(seeds[0]) + int(seeds[1]) for seeds in self.seeds])

    def contains(self, item):
        for a_range in self.seeds:
            start, length = map(int, a_range)
            if item in range(start, start + length):
                return True
        return False


class StupidData:
    def __init__(self,
                 seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature,
                 temperature_to_humidity, humidity_to_location):
        self.seeds = seeds
        self.seed_to_soil = seed_to_soil
        self.soil_to_fertilizer = soil_to_fertilizer
        self.fertilizer_to_water = fertilizer_to_water
        self.water_to_light = water_to_light
        self.light_to_temperature = light_to_temperature
        self.temperature_to_humidity = temperature_to_humidity
        self.humidity_to_location = humidity_to_location

    def find_lowest_location(self, a_range):
        min_location = 10E12
        # end = a_range[-1]
        processed = 0
        last_printed = -1
        logger.info('Processing range %s', a_range)
        length = len(a_range)
        for location in a_range:
            percent_done = int((processed / length) * 100)
            rest = int(percent_done % 5)
            if percent_done > 0 and rest == 0 and percent_done != last_printed:
                logger.info('process %d: %d', os.getpid(), percent_done)
                last_printed = percent_done
            humidity = self.humidity_to_location.value_for(location)
            temperature = self.temperature_to_humidity.key_for(humidity)
            light = self.light_to_temperature.key_for(temperature)
            water = self.water_to_light.key_for(light)
            fertilizer = self.fertilizer_to_water.key_for(water)
            soil = self.soil_to_fertilizer.key_for(fertilizer)
            seed = self.seed_to_soil.key_for(soil)
            if self.seeds.contains(seed):
                # logger.debug(f'{seed} -> {soil} -> {fertilizer} -> {water} -> {light} -> {temperature} -> {humidity} -> {location}')
                min_location = min((location, min_location))
                logger.debug(f'{location} -> {humidity} -> {temperature} -> {light} -> {water} -> {fertilizer} -> {soil} -> {seed}')
            processed += 1
        return min_location

class StupidMapBase:
    def __init__(self, name: str):
        self.name = name
        self.ranges: list[StupidRange] = []

    def add_lines(self, lines: list[str]):
        for line in lines:
            ic(line)
            numbers = [int(number) for number in line.split()]
            self.ranges.append(StupidRange(numbers))

    def value_for(self, key: int) -> int:
        key_in_range, a_range = self.key_in_range(key)
        if key_in_range:
            value = a_range.value_for_key(key)
        else:
            value = key
        return value

    def key_in_range(self, key: int) -> (bool, any):
        for a_range in self.ranges:
            if a_range.key_in_range(key):
                return True, a_range
        return False, None

    def key_for(self, value: int) -> int:
        value_in_range, a_range = self.value_in_range(value)
        if value_in_range:
            return a_range.key_for_value(value)
        else:
            return value

    def value_in_range(self, value: int) -> (bool, any):
        for a_range in self.ranges:
            if a_range.value_in_destination(value):
                return True, a_range
        return False, None

    def get_max_range_value(self) -> int:
        max_value = 0
        for a_range in self.ranges:
            range_end = a_range.get_destination_range()[-1]
            max_value = max((max_value, range_end))
        return max_value

    def __str__(self):
        return ','.join([str(a_range) for a_range in self.ranges])


class StupidRange:
    def __init__(self, numbers: list[int]):
        self.destination_start = int(numbers[0])
        self.source_start = int(numbers[1])
        self.length = int(numbers[2])

    def key_in_range(self, key: int) -> bool:
        return key in range(self.source_start, self.source_start + self.length)

    def value_in_destination(self, value) -> bool:
        return value in range(self.destination_start, self.destination_start + self.length)

    def value_for_key(self, key: int) -> int:
        if self.key_in_range(key):
            return self.destination_start + (key - self.source_start)

    def get_source_range(self) -> range:
        return range(self.source_start, self.source_start + self.length)

    def key_for_value(self, value) -> int:
        if self.value_in_destination(value):
            try:
                destination_range = self.get_destination_range()
                return self.source_start + destination_range.index(value)
            except ValueError as e:
                print('Could not find', value, 'in range', destination_range)
                raise e
        else:
            return value

    def get_destination_range(self) -> range:
        return range(self.destination_start, self.destination_start + self.length)

    def __str__(self):
        return (f'source: [{self.source_start} .. {self.source_start + self.length}] '
                f'destination [{self.destination_start} .. {self.destination_start + self.length}]')


def parse_input_lines(lines):
    seeds: RangeSeeds = RangeSeeds()
    range_seeds: RangeSeeds = RangeSeeds()
    seed_to_soil = StupidMapBase('seed-to-soil map')
    soil_to_fertilizer = StupidMapBase('soil-to-fertilizer map')
    fertilizer_to_water = StupidMapBase('fertilizer-to-water map')
    water_to_light = StupidMapBase('water-to-light map')
    light_to_temperature = StupidMapBase('light-to-temperature map')
    temperature_to_humidity = StupidMapBase('temperature-to-humidity map')
    humidity_to_location = StupidMapBase('humidity-to-location map')
    line_iter = iter(lines)
    line = next(line_iter, 'EOF')
    while line != 'EOF':
        if line and line[0].isalpha():
            map_name = line.split(':')[0]
            if map_name == 'seeds':
                ic('seeds')
                seeds.add_line(line.split(':')[1])
                range_seeds.add_line(line.split(':')[1])
            if map_name == seed_to_soil.name:
                ic('seeds_to_soil')
                parse_to_map(line_iter, seed_to_soil)
            if map_name == soil_to_fertilizer.name:
                ic('soil_to_fertilizer')
                parse_to_map(line_iter, soil_to_fertilizer)
            if map_name == fertilizer_to_water.name:
                ic('fertilizer_to_water')
                parse_to_map(line_iter, fertilizer_to_water)
            if map_name == water_to_light.name:
                ic('water_to_light')
                parse_to_map(line_iter, water_to_light)
            if map_name == light_to_temperature.name:
                ic('light_to_temperature')
                parse_to_map(line_iter, light_to_temperature)
            if map_name == temperature_to_humidity.name:
                ic('temperature_to_humidity')
                parse_to_map(line_iter, temperature_to_humidity)
            if map_name == humidity_to_location.name:
                ic('humidity_to_location')
                parse_to_map(line_iter, humidity_to_location)
        line = next(line_iter, 'EOF')
    return seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location


def parse_to_map(line_iter, seed_to_soil):
    lines_to_parse = []
    for line in takewhile(lambda text: text, line_iter):
        lines_to_parse += [line]
    seed_to_soil.add_lines(lines_to_parse)


def execute():
    start_time = time.time()
    lines = read_input_file(file_name='day5.txt', remove_blank_lines=False)
    (seeds,
     seed_to_soil,
     soil_to_fertilizer,
     fertilizer_to_water,
     water_to_light,
     light_to_temperature,
     temperature_to_humidity,
     humidity_to_location) = parse_input_lines(lines)
    data = StupidData(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)
    ic('starting')
    step = int(humidity_to_location.get_max_range_value() / 10)
    ranges = []
    end = step
    for start in range(0, humidity_to_location.get_max_range_value(), step):
        ranges.append(range(start, end))
        end += step
    with Pool(10) as p:
        min_locations = p.map(data.find_lowest_location, ranges)
        print(sorted(min_locations))
    stop_time = time.time()
    logger.info('done in %d seconds', int(stop_time - start_time))


if __name__ == '__main__':
    execute()

# 44014033 to high
# 28580590



# 1717986916
# 446166190
# 1288490187,
# 1717986916,
# 2576980374,
# 28580590
# 1288490187