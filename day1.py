""" Day 1 Trebuche """
from utils import read_input_file
from re import finditer

word_to_int_dict = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def word_to_int(word: str) -> int:
    """ Converts a number word to the corresponding int. """
    return word_to_int_dict[word]


def find_numbers(string: str) -> [(int, int)]:
    """ Finds all the number words in the string. """
    numbers = filter_out_digit(string)
    numbers += find_number_words(string)
    numbers = sorted(numbers, key=lambda number: number[1])
    return [number[0] for number in numbers]


def find_number_words(string: str) -> [(int, int)]:
    """ Finds all numbers and numbers words in the string and returns them in the order they occur."""
    numbers = []
    for word, number in word_to_int_dict.items():
        indexes = [index.start() for index in finditer(word, string)]
        numbers += [(number, index) for index in indexes]
    return numbers


def filter_out_digit(string):
    """ Filters out and returns all the digits in the string. """
    return [(int(char), index) for index, char in enumerate(string) if char.isdigit()]


if __name__ == '__main__':
    lines = read_input_file(file_name='day1.txt')
    numbers_on_line = map(find_numbers, lines)
    first_and_last = [int(f'{line[0]}{line[-1]}') for line in numbers_on_line]
    print(first_and_last)
    print(sum(first_and_last))
