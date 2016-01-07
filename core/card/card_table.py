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

if __name__ == '__main__':
    CardTable()
    CardTable()
    raw_input()