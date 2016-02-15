# -*- coding: utf-8 -*-
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class Hand(utility.Component):
    """
    Управляет картами
    """

    categories = [predef.HAND]

    def __init__(self):
        super(Hand, self).__init__()
        self._cards = []
        self._selected_cards = []

    def select_cards(self, *cards):
        pass

    def get_cards(self, *cards):
        self._cards += cards

    def make_action(self, action):
        pass
