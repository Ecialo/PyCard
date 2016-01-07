#! /usr/bin/python
# -*- coding: utf-8 -*-
from ..flow import turn
__author__ = 'Ecialo'


class DrawCards(turn.Turn):
    """
    Вытянуть cards_amount карт из колоды deck в руку target
    """

    def __init__(self, target, deck, cards_amount=1):
        super(DrawCards, self).__init__(target)
        self._amount = cards_amount
        self._deck = deck
