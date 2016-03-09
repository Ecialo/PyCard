# -*- coding: utf-8 -*-
from .. import action
__author__ = 'ecialo'


class RemoveCards(action.Action):

    def __init__(self, author, **kwargs):
        self.target = None
        self.cards = None
        super(RemoveCards, self).__init__(author, **kwargs)

    def apply(self):
        for card in self.cards:
            self.target.remove_card(card)