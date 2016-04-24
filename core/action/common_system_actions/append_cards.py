# -*- coding: utf-8 -*-
from .. import action
__author__ = 'ecialo'


class AppendCards(action.Action):
    name = "append_card"

    def __init__(self, author, **kwargs):
        self.cards = None
        self.target = None
        super(AppendCards, self).__init__(author, **kwargs)

    def apply(self):
        self.target.get_cards(*self.cards)