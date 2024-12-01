""" The boat race """
import math

from utils import read_input_file
from icecream import ic
from re import findall

filename = 'day6.txt'


class Race:
    """ Class that holds data about a race. """

    def __init__(self, duration: int, length: int):
        self.duration = duration
        self.length = length

    def ways_of_winning(self):
        """ Finds the number of ways to win. """
        first = self.find_first_winning(range(1, self.duration))
        last = self.find_first_winning(range(self.duration, 1, -1))
        ic(first, last)
        return len(range(first, last + 1))

    def find_first_winning(self, a_range: range) -> int:
        """ iterates over the range and find the first time that wins"""
        for time in a_range:
            time_to_travel = self.duration - time
            distance_traveled = time_to_travel * time
            if distance_traveled > self.length:
                return time

    def __str__(self):
        return f'{{duration: {self.duration}, length: {self.length}}})'


def execute():
    """ Sums up the number of ways of winning """
    lines = read_input_file(file_name=filename)
    times, distances = [findall(r'\d+', line) for line in lines]
    the_list = list(zip(times, distances))
    races = [Race(int(duration), int(length)) for (duration, length) in the_list]
    ways_of_winning_prod = math.prod([race.ways_of_winning() for race in races])
    ic(ways_of_winning_prod)
    new_time = int(''.join([str(time) for time in times]))
    new_distance = int(''.join([str(distance) for distance in distances]))
    ic(new_time, new_distance)
    new_race = Race(new_time, new_distance)
    ic(new_race.ways_of_winning())


if __name__ == '__main__':
    execute()
