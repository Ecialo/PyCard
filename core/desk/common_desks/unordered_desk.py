# -*- coding: utf-8 -*-
from .. import desk
__author__ = 'ecialo'


class UnorderedDesk(desk.Desk):
    """
    Карты на этой доске не учитывают взаиморасположение.
    """

    def __init__(self):
        super(UnorderedDesk, self).__init__()
        self._cards = []

    def place_on(self, card, *args, **kwargs):
        self._cards.append(card)
        super(UnorderedDesk, self).place_on(card)

    def take_off(self, card):
        self._cards.remove(card)
        # super(UnorderedDesk, self).take_off(card)

    @property
    def cards(self):
        return self._cards[::]
