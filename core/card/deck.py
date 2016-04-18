# -*- coding: utf-8 -*-
import random as rnd
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class Deck(utility.Component):
    """
    Колода содержит индексы карт из таблицы карт данной игры
    """
    content = []        # TODO добавить возможность передавать как имена так и классы
    categories = [predef.DECK]

    hooks = ['remove_card']

    def __init__(self):
        super(Deck, self).__init__()
        self._deck = []
        for card_name, amount in self.content:
            self._deck += [card_name] * amount
        self._num_of_cards = len(self._deck)

    @property
    def number_of_cards(self):
        return self._num_of_cards

    def draw_card(self):
        self._num_of_cards -= 1
        return self._deck.pop()

    def remove_card(self, card):
        if card:
            self._deck.remove(card)
        self._num_of_cards -= 1

    def shuffle(self):
        rnd.shuffle(self._deck)

    def is_empty(self):
        return not bool(self._deck)
