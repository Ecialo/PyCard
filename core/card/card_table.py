# -*- coding: utf-8 -*-
import json
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class CardTable(utility.Table):
    """
    Перечень карт участвующих в игре.
    """

    name = predef.CARD
    card_set_file = None
    cards = []
    _cards = {}

    def init(self):
        if self.card_set_file:
            with open(self.card_set_file) as cards_file:
                for card_struct in json.load(cards_file):
                    self.cards.append(self.make_card(card_struct))
        for card in self.cards:
            self._cards[card.name] = card

    def __getitem__(self, item):
        return self._cards.get(item)

    def make_card(self, card_struct):
        pass