# -*- coding: utf-8 -*-
from itertools import product
import json
from core.card import card_table
__author__ = 'ecialo'

CARD_SET = './sample_games/durak/assets/cards.json'


class DurakCardTable(card_table.CardTable):

    card_set_file = CARD_SET


if __name__ == '__main__':

    table_of_names = {
        14: "Ace",
        13: "King",
        12: "Queen",
        11: "Jack",
    }

    def make_card_struct(suit_value):
        suit, value = suit_value
        card_struct = {
            'suit': suit,
            'value': value,
            'name': (
                (str(value) if value not in table_of_names else table_of_names[value]) +
                " of " +
                suit
            )
        }
        return card_struct

    suits = [
        'Hearts',
        'Diamonds',
        'Clubs',
        'Spades',
    ]
    value = range(2, 15)

    all_cards = product(suits, value)

    with open(CARD_SET, 'w') as card_file:
        json.dump(map(make_card_struct, all_cards), card_file)