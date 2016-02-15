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

    def __init__(self):
        super(Deck, self).__init__()
        self._deck = []
        for card_name, amount in self.content:
            self._deck += [card_name] * amount

    def draw_card(self):
        return self._deck.pop()

    def shuffle(self):
        rnd.shuffle(self._deck)

    def is_empty(self):
        return bool(self._deck)
