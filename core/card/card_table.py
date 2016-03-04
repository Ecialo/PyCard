# -*- coding: utf-8 -*-
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class CardTable(utility.Table):
    """
    Перечень карт участвующих в игре.
    """

    name = predef.CARD
    cards = []
    _cards = {}

    def init(self):
        for card in self.cards:
            self._cards[card.name] = card

    def __getitem__(self, item):
        return self._cards[item]

    def register_card(self, environment, id_=None):
        pass

if __name__ == '__main__':
    CardTable()
    CardTable()
    raw_input()