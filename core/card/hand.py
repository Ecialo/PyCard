# -*- coding: utf-8 -*-
from collections import Iterable
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class Hand(utility.Component):
    """
    Управляет картами
    """

    categories = [predef.HAND]
    hooks = ['get_cards']

    def __init__(self):
        super(Hand, self).__init__()
        self._cards = []
        self._num_of_cards = 0
        self._selected_cards = []

    def cards(self):
        return self._cards[::]

    def select_cards(self, *cards):
        pass

    def get_cards(self, *cards):
        self._cards += cards
        self._num_of_cards += len(cards)

    def make_action(self, action):
        pass

    def remove_card(self, card):
        if card:
            self._cards.remove(card)
        self._num_of_cards += 1

    def __eq__(self, other):
        if isinstance(other, Hand):
            self == other._cards
        elif isinstance(other, Iterable):
            return sorted(self._cards) == sorted(other)
        else:
            return self is other

    def __repr__(self):
        return "Hand: " + str(self._cards)
