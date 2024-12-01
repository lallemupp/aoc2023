""" Camel Card """

from utils import read_input_file
from icecream import ic

# filename = "test.txt"
filename = "day7.txt"
card_to_value = {
    'A': 'a',
    'K': 'b',
    'Q': 'c',
    'J': 'd',
    'T': 'e',
    '9': 'f',
    '8': 'g',
    '7': 'h',
    '6': 'i',
    '5': 'j',
    '4': 'k',
    '3': 'l',
    '2': 'm',
    '1': 'n'
}

card_to_value_with_joker = {
    'A': 'a',
    'K': 'b',
    'Q': 'c',
    'J': 'o',
    'T': 'e',
    '9': 'f',
    '8': 'g',
    '7': 'h',
    '6': 'i',
    '5': 'j',
    '4': 'k',
    '3': 'l',
    '2': 'm',
    '1': 'n'
}

valid_hands = ['FIVE', 'FOUR', 'FH', 'THREE', 'TP', 'PAIR', 'ONE']


class Hand:
    """ Describes a hand of camel cards. """
    def __init__(self, line):
        self.cards = line.split()[0]
        self.hand = self.find_winning()
        self.weight = int(line.split()[1])

    def find_winning(self, ) -> str:
        """ Finds the winning of the hand. """
        number_of_each_card: dict[str, int] = {}
        for card in self.cards:
            number_of_card = number_of_each_card.get(card)
            number_of_each_card[card] = 1 if not number_of_card else number_of_card + 1
        if Hand.find_hand(5, number_of_each_card):
            return 'FIVE'
        elif Hand.find_hand(4, number_of_each_card):
            return 'FOUR'
        elif Hand.find_hand(3, number_of_each_card):
            if Hand.find_hand(2, number_of_each_card):
                return 'FH'
            else:
                return 'THREE'
        found_for_card = Hand.find_hand(2, number_of_each_card)
        if found_for_card:
            if Hand.find_hand(2, number_of_each_card, do_not_look_for=found_for_card):
                return 'TP'
            else:
                return 'PAIR'
        return 'ONE'

    @staticmethod
    def find_hand(number_to_look_for: int, cards_to_number: dict[str: int], do_not_look_for: any = None) -> any:
        """ Finds if the hand contains the specific number of any card. """
        for card, value in cards_to_number.items():
            if card != do_not_look_for and number_to_look_for == value:
                return card
        return None

    def __str__(self):
        return f'{{cards: {self.cards}, hand: {self.hand}}}'


class JokerHand:
    """ A hand of cards where J are wild. """
    def __init__(self, line: str):
        self.cards = line.split()[0]
        self.card_values = ''.join([card_to_value_with_joker[card] for card in self.cards])
        self.weight = int(line.split()[1])
        self.hand = self.find_hand()

    def find_hand(self) -> str:
        cards_to_number_of_cards: dict[str, int] = {}
        for card in self.cards:
            current_number_of_card = cards_to_number_of_cards.get(card)
            cards_to_number_of_cards[card] = 1 if not current_number_of_card else current_number_of_card + 1
        max_cards = self.find_cards(cards_to_number_of_cards)
        if max_cards[1] == 5:
            return 'FIVE'
        if max_cards[1] == 4:
            return 'FOUR'
        if max_cards[1] == 3:
            second_most_cards = self.find_cards(cards_to_number_of_cards, [max_cards[0], 'J'], add_joker=False)
            if second_most_cards[1] == 2:
                return 'FH'
            else:
                return 'THREE'
        elif max_cards[1] == 2:
            second_most_cards = self.find_cards(cards_to_number_of_cards, [max_cards[0], 'J'], add_joker=False)
            if second_most_cards[1] == 2:
                return 'TP'
            else:
                return 'PAIR'
        return 'ONE'

    def find_cards(
            self,
            cards_to_numbers_of_cards: dict[str: int],
            to_ignore: list[str] = (),
            add_joker: bool = True
    ) -> (str, int):
        filtered_cards = dict(filter(lambda card: card[0] not in to_ignore, cards_to_numbers_of_cards.items()))
        if filtered_cards.get('J', 0) == 5:
            return 'J', 5
        jokers = filtered_cards.get('J') or 0
        try:
            del filtered_cards['J']
        except KeyError:
            pass
        max_item = max(filtered_cards, key=filtered_cards.get)
        number_of_max_item = int(filtered_cards[max_item])
        if add_joker:
            number_of_max_item += jokers
        return max_item, number_of_max_item

    def __str__(self):
        return f'{self.cards} {self.hand}'


def main():
    """ Executes the code! """
    lines = read_input_file(file_name=filename)
    hands = [Hand(line) for line in lines]
    sorted_hands = sorted(
        hands,
        key=lambda hand: (valid_hands.index(hand.hand), ''.join([card_to_value[card] for card in hand.cards])),
        reverse=True
    )
    total_value = 0
    for i, hand in enumerate(sorted_hands):
        index = i + 1
        total_value += hand.weight * index
    ic(total_value)
    joker_hands = [JokerHand(line) for line in lines]
    sorted_joker_hands = sorted(
        joker_hands,
        key=lambda x: (valid_hands.index(x.hand), x.card_values),
        reverse=True
    )
    joker_value = 0
    for i, hand in enumerate(sorted_joker_hands):
        index = i + 1
        joker_value += (index * hand.weight)
    ic(joker_value)


if __name__ == '__main__':
    main()

# 250101670 to low
# 250898830 Correct part 1

# 253094508 To high
# 253002566 To high
# 251468324 To low
# 251823002 FAIL!
# 252511144 FAIL!
# 252127335 SUCCESS!
