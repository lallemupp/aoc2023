""" Day 3 Engine """
import math

from icecream import ic

from utils import read_input_file, submatrix


class Engine:
    """ Class representing the engin. """
    def __init__(self):
        self.parts = []
        self.gear_parts = []
        self.index_to_part = {}
        self.part_number = 0

    def add_line(self, line_number: int, line: str):
        """ Parses and adds the line to the parts and gear parts. """
        ic(line_number)
        self.parts.append([char for char in line])
        gear_part = ''
        gear_line = []
        for char in line:
            if char.isdigit():
                gear_part += char
            else:
                if gear_part:
                    gear_line += [gear_part] * len(gear_part)
                    gear_part = ''
                gear_line.append(char)
        if gear_part:
            gear_line += [gear_part] * len(gear_part)
        self.gear_parts.append(gear_line)


    def find_parts(self):
        """ Finds all the parts and the corresponding number. """
        found_parts = []
        for row_number, row in enumerate(self.parts):
            part = ''
            for char_index, char in enumerate(row):
                if not char.isdigit() and part:
                    if self.valid_part_number(part, char_index, row_number):
                        found_parts.append(int(part))
                    part = ''
                elif char.isdigit():
                    part += char
            if part:
                if self.valid_part_number(part, len(row), row_number):
                    found_parts.append(int(part))
        return found_parts

    def find_gears(self):
        """ Finds all gears and there corresponding product. """
        gear_ratios = []
        for row_number, row in enumerate(self.gear_parts):
            for char_number, char in enumerate(row):
                if char == '*':
                    sub_matrix = submatrix(self.gear_parts, 1, char_number, char_number, row_number)
                    valid, product = process_gear_matrix(sub_matrix)
                    if valid:
                        gear_ratios.append(product)
        return gear_ratios

    def valid_part_number(self, part: str, char_index: int, row_number: int) -> bool:
        """ Checks if the part has a valid part number. """
        start = char_index - len(part)
        end = char_index - 1
        sub_matrix = submatrix(self.parts, 1, start, end, row_number)
        response = contains_part(sub_matrix)
        return response


def contains_part(matrix):
    """ Checks if the matrix contains non digit character that is not ."""
    for row in matrix:
        for char in row:
            if not char.isdigit() and char != '.':
                return True
    return False


def parse_engine():
    """ Parses the input and generates an engine. """
    engine = Engine()
    for line_number, line in enumerate(read_input_file(file_name='day3.txt')):
        engine.add_line(line_number, line)
    return engine


def process_gear_matrix(matrix):
    """ Processes the gear matrix and returns the product of all numbers and if it is valid."""
    all_numbers = []
    for line in matrix:
        number = {int(char) for char in line if char.isdigit()}
        all_numbers += list(number)
    return len(all_numbers) == 2, math.prod(all_numbers)


if __name__ == '__main__':
    engine = parse_engine()
    parts = engine.find_parts()
    ic(sum(parts))
    ratios = engine.find_gears()
    ic(sum(ratios))
