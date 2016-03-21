# -*- coding: utf-8 -*-
from .. import action
__author__ = 'ecialo'


class MakeCard(action.Action):

    def __init__(self, **kwargs):
        self.card_name = None
        self._id = None
        super(MakeCard, self).__init__(**kwargs)

    def apply(self):
        return {'card': self.game.make_card(self.card_name, self._id)}
