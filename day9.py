""" OASIS number sequences. """

from utils import read_input_file
from icecream import ic
from itertools import pairwise


# filename = 'test.txt'
filename = 'day9.txt'


class Sequence:
    """ Represents a sequence of OASIS data. """
    def __init__(self, line):
        self.sequence = list(map(int, line.split()))

    def calculate_diff_sequence(self):
        """ Subtract the number [1, 2, 3, 4] turns into [1, 1, 1] """
        return Sequence(' '.join([str(y - x) for x, y in pairwise(self.sequence)]))

    def is_zeros(self) -> bool:
        """ Check if all the number in the sequence is 0 or not. """
        for number in self.sequence:
            if number != 0:
                return False
        return True

    def predict(self, number: int):
        """ Predict the next number after the sequence by adding the number to the last number. """
        self.sequence.append(number + self.sequence[-1])

    def extrapolate(self, number: int):
        """ Extrapolates the preceding number of the sequence subtracting the number from the first number. """
        self.sequence.insert(0, self.sequence[0] - number)

    def get_last(self) -> int:
        """ Gets the last number in the sequence. """
        return self.sequence[-1]

    def get_first(self) -> int:
        """ Gets the first number in the sequence. """
        return self.sequence[0]

    def __str__(self):
        return str(self.sequence)


class Engine:
    """ A prediction engine """
    def predict(self, sequence: Sequence) -> Sequence:
        """ Predict the next number after the sequence. """
        next_sequence = sequence.calculate_diff_sequence()
        if sequence.is_zeros():
            return next_sequence
        else:
            self.predict(next_sequence)
        sequence.predict(next_sequence.get_last())
        return sequence

    def extrapolate(self, sequence: Sequence) -> Sequence:
        """ Extrapolates the first number in the sequence. """
        next_sequence = sequence.calculate_diff_sequence()
        if sequence.is_zeros():
            return next_sequence
        else:
            self.extrapolate(next_sequence)
        sequence.extrapolate(next_sequence.get_first())
        return sequence


def part1():
    """ Part 1 """
    lines = read_input_file(file_name=filename)
    sequences = [Sequence(line) for line in lines]
    engine = Engine()
    predictions = []
    for sequence in sequences:
        predictions.append(engine.predict(sequence).get_last())
    ic(sum(predictions))


def part2():
    """ Part 2 """
    lines = read_input_file(file_name=filename)
    sequences = [Sequence(line) for line in lines]
    engine = Engine()
    extrapolations = []
    for sequence in sequences:
        extrapolated_sequence = engine.extrapolate(sequence)
        extrapolations.append(extrapolated_sequence.get_first())
    ic(sum(extrapolations))


if __name__ == '__main__':
    part1()
    part2()
