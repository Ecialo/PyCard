# -*- coding: utf-8 -*-
from ..turn import Turn
__author__ = 'ecialo'


class PersonalTurn(Turn):

    def receive_action(self, action):
        if action.author == self._target:
            self._action = action
