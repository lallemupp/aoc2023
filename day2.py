""" Day 2 Cube Game """
import math
import re

from icecream import ic

from utils import read_input_file

red_ex = r'\d+ red|$'
green_ex = r'\d+ green|$'
blue_ex = r'\d+ blue|$'

max_list = [12, 13, 14]


def get_pulled_ball_array(game: str):
    """ Parses the input line and returns it as an array in form of [r, g, b] """
    red = re.findall(red_ex, game)[0].split(' ')[0] or 0
    green = re.findall(green_ex, game)[0].split(' ')[0] or 0
    blue = re.findall(blue_ex, game)[0].split(' ')[0] or 0
    return [int(red), int(green), int(blue)]


class Round:
    """ Holds information about a round. """
    def __init__(self, game_array):
        self.r = game_array[0]
        self.g = game_array[1]
        self.b = game_array[2]

    def is_valid(self, max_array: list[int]) -> bool:
        """ Checks if the round is valid. """
        return self.r <= max_array[0] and self.g <= max_array[1] and self.b <= max_array[2]

    def __str__(self):
        return f'{self.r} red, {self.g} green, {self.b} blue'

    def as_list(self) -> list[int]:
        """ Returns the rounds as a list in form [r, g, b] """
        return [self.r, self.g, self.b]


class Game:
    """ Holds information about a game. """
    def __init__(self, line: str):
        self.pulls = []
        self.id = int(line.split(':')[0].split(' ')[1])
        for pulled_balls in line.split(':')[1].split(';'):
            self.pulls.append(Round(get_pulled_ball_array(pulled_balls)))

    def is_valid(self, maxes) -> bool:
        """ Checks if the rounds in the game are valid or not. """
        return not len([game for game in self.pulls if not game.is_valid(maxes)]) > 0

    def power(self) -> int:
        """ Returns the power of the game. The power is the maximum number of cubes for each color multiplied. """
        ic.disable()
        maxes = [0, 0, 0]
        for pull in self.pulls:
            pull_list = pull.as_list()
            for index, color in enumerate(pull_list):
                ic(maxes, index)
                maxes[index] = pull_list[index] if maxes[index] < pull_list[index] else maxes[index]
        power = math.prod(maxes)
        ic(self.id, maxes, power)
        return power

    def __str__(self):
        return self.id


if __name__ == '__main__':
    lines = read_input_file(file_name='day2.txt')
    games = [Game(line) for line in lines]
    valid_games = [game.id for game in games if game.is_valid(max_list)]
    invalid_games = [game.id for game in games if not game.is_valid(max_list)]
    print(sum(valid_games))
    print(sum([game.power() for game in games]))
