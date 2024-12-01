""" Day 4 Scratch Tickets """
import math

import utils

from icecream import ic


class Card:
    def __init__(self, line):
        self.winning_numbers = []
        self.my_numbers = []
        card_data = line.split(':')[1]
        winning_numbers = card_data.split('|')[0]
        my_numbers = card_data.split('|')[1]
        self.parse_winning_numbers(winning_numbers)
        self.parse_my_numbers(my_numbers)

    def parse_winning_numbers(self, line):
        self.winning_numbers = [int(number.strip()) for number in line.split()]

    def parse_my_numbers(self, line: str):

        self.my_numbers = [int(number.strip()) for number in line.split() if number.isdigit()]

    def card_value(self):
        winning_numbers = [winning_number for winning_number in self.my_numbers if winning_number in self.winning_numbers]
        power = len(winning_numbers) - 1
        value = math.floor(math.exp2(power))
        return value

    def number_of_winning_numbers(self):
        winning_numbers = [winning_number for winning_number in self.my_numbers if winning_number in self.winning_numbers]
        return len(winning_numbers)

class Cards():
    def __init__(self, lines):
        self.cards = [Card(line) for line in lines]

    def get_cards_values(self) -> int:
        cards_value = [card.card_value() for card in self.cards]
        return sum(cards_value)

    def cards_value_2(self):
        """ Finds the total number of scratch cards that has been won."""
        cards = [1] * len(self.cards)
        for card_number in range(len(cards)):
            ic(card_number)
            for index in range(cards[card_number]):
                card_winnings = self.cards[card_number].number_of_winning_numbers()
                start_index = min([card_number + 1, len(cards)])
                end_index = min([card_number + card_winnings + 1, len(cards)])
                for card in range(start_index, end_index):
                    cards[card] += 1
        return sum(cards)


def execute():
    lines: list[str] = utils.read_input_file(file_name='day4.txt')
    cards = Cards(lines)
    ic(cards.get_cards_values())
    ic(cards.cards_value_2())


if __name__ == '__main__':
    execute()

