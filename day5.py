""" Day 5 Seed Planting. """

import logging
import multiprocessing
import os
import datetime
from itertools import takewhile

from icecream import ic

from utils import read_input_file

# format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(threadName)s] '
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

    def __str__(self):
        seed_strings = []
        for seeds in self.seeds:
            start, end = map(int, seeds)
            seed_range = range(start, start + end)
            seed_strings.append(f'{seed_range[0]}: {seed_range[-1]}')
        return ", ".join(seed_strings)


class StupidRange:
    def __init__(self, numbers: list[int]):
        self.destination_start = int(numbers[0])
        self.source_start = int(numbers[1])
        self.length = int(numbers[2])

    def key_in_range(self, key: int) -> bool:
        return key in range(self.source_start, self.source_start + self.length)

    def value_for_key(self, key: int) -> int:
        if self.key_in_range(key):
            return self.destination_start + (key - self.source_start)

    def get_source_range(self) -> range:
        return range(self.source_start, self.source_start + self.length)

    def get_destination_range(self) -> range:
        return range(self.destination_start, self.destination_start + self.length)

    def __str__(self):
        return (f'destination [{self.destination_start} .. {self.destination_start + self.length}] '
                f'source: [{self.source_start} .. {self.source_start + self.length}]')


class StupidData:
    def __init__(self,
                 seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature,
                 temperature_to_humidity, humidity_to_location):
        self.seed_to_soil = seed_to_soil
        self.soil_to_fertilizer = soil_to_fertilizer
        self.fertilizer_to_water = fertilizer_to_water
        self.water_to_light = water_to_light
        self.light_to_temperature = light_to_temperature
        self.temperature_to_humidity = temperature_to_humidity
        self.humidity_to_location = humidity_to_location

    def seedy_runner(self, seed_range, proc_number, mins) -> int:
        logger.info('Process %s, proc number %s', os.getpid(), proc_number)
        min_location = 1E12
        processed = 0
        start, length = map(int, seed_range)
        end = start + length
        last_printed = -1
        seed_range = range(start, end)
        logger.info(f'starting with numbers from {seed_range[0]} to {seed_range[-1]}')
        for seed in seed_range:
            logger.debug('seed %s', seed)
            percent_done = int((processed / length) * 100)
            rest = int(percent_done % 5)
            if percent_done > 0 and rest == 0 and percent_done != last_printed:
                logger.info('process %d: %d', proc_number, percent_done)
                last_printed = percent_done
            soil = self.seed_to_soil.value_for(seed)
            fertilizer = self.soil_to_fertilizer.value_for(soil)
            water = self.fertilizer_to_water.value_for(fertilizer)
            light = self.water_to_light.value_for(water)
            temperature = self.light_to_temperature.value_for(light)
            humidity = self.temperature_to_humidity.value_for(temperature)
            location = self.humidity_to_location.value_for(humidity)
            if location < min_location:
                min_location = min((min_location, location))
                logger.debug(
                    f'seed: {seed} -> soil: {soil} -> fertilizer: {fertilizer} -> water: {water} -> light: {light} -> temperature: {temperature} -> humidity: {humidity} -> location: {location}')
                min_location = min((location, min_location))
            processed += 1
        mins[proc_number] = min_location
        print(mins)


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
        for range in self.ranges:
            if range.key_in_range(key):
                return True, range
        return False, None

    def __str__(self):
        return ','.join([str(a_range) for a_range in self.ranges])


def printer(thread_number, message):
    logger.debug('thread: %d %s', thread_number, message)


def execute():
    lines = read_input_file(file_name='day5.txt', remove_blank_lines=False)
    (seeds,
     range_seeds,
     seed_to_soil,
     soil_to_fertilizer,
     fertilizer_to_water,
     water_to_light,
     light_to_temperature,
     temperature_to_humidity,
     humidity_to_location) = parse_input_lines(lines)
    # ic(str(seeds))
    # ic(str(seed_to_soil))
    # ic(str(soil_to_fertilizer))
    # ic(str(fertilizer_to_water))
    # ic(str(water_to_light))
    # ic(str(light_to_temperature))
    # ic(str(temperature_to_humidity))
    # ic(str(humidity_to_location))
    # locations = []
    # for seed in seeds.seeds:
    #     ic(seed)
    #     soil = seed_to_soil.value_for(seed)
    #     fertilizer = soil_to_fertilizer.value_for(soil)
    #     water = fertilizer_to_water.value_for(fertilizer)
    #     light = water_to_light.value_for(water)
    #     temperature = light_to_temperature.value_for(light)
    #     humidity = temperature_to_humidity.value_for(temperature)
    #     location = humidity_to_location.value_for(humidity)
    #     locations.append(location)
    # ic(min(locations))
    logger.info('range seeds: %s', range_seeds)
    ic.disable()
    start_time = datetime.datetime.now()
    data = StupidData(seed_to_soil,
                      soil_to_fertilizer,
                      fertilizer_to_water,
                      water_to_light,
                      light_to_temperature,
                      temperature_to_humidity,
                      humidity_to_location)

    # with Pool(10) as p:
    #     mins = p.map(data.seedy_runner, range_seeds.seeds)
    #     logger.info('min location: %d', min(mins))
    manager: multiprocessing.Manager = multiprocessing.Manager()
    mins = manager.dict()
    procs = []
    for i, seeds in enumerate(range_seeds.seeds):
        proc = multiprocessing.Process(target=data.seedy_runner, args=(seeds, i, mins))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
    logger.info('it all took: %s', (datetime.datetime.now() - start_time))
    print(min(mins.values()))


def parse_input_lines(lines):
    seeds: Seeds = Seeds()
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
    return (seeds,
            range_seeds,
            seed_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location)


def seedy_runner(thread_number, seed_range: tuple, seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
                 water_to_light,
                 light_to_temperature, temperature_to_humidity, humidity_to_location, callback) -> int:
    callback(thread_number, 'starting')
    min_location = 1E12
    processed = 0
    start, length = map(int, seed_range)
    end = start + length
    last_printed = -1
    seed_range = range(start, end)
    callback(thread_number, f'starting with numbers from {seed_range[0]} to {seed_range[-1]}')
    for seed in seed_range:
        percent_done = int((processed / length) * 100)
        rest = int(percent_done % 5)
        if percent_done > 0 and rest == 0 and percent_done != last_printed:
            callback(thread_number, f'{percent_done}%')
            last_printed = percent_done
        soil = ic(seed_to_soil.value_for(seed))
        fertilizer = ic(soil_to_fertilizer.value_for(soil))
        water = ic(fertilizer_to_water.value_for(fertilizer))
        light = ic(water_to_light.value_for(water))
        temperature = ic(light_to_temperature.value_for(light))
        humidity = ic(temperature_to_humidity.value_for(temperature))
        location = ic(humidity_to_location.value_for(humidity))
        min_location = min((min_location, location))
        processed += 1
    return int(min_location)


def parse_to_map(line_iter, seed_to_soil):
    lines_to_parse = []
    for line in takewhile(lambda text: text, line_iter):
        lines_to_parse += [line]
    seed_to_soil.add_lines(lines_to_parse)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    execute()
# 28580590 to high
# 28580590
# 28580589 KORREKT!