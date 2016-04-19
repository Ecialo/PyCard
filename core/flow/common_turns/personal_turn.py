# -*- coding: utf-8 -*-
from ..turn import Turn
__author__ = 'ecialo'


class PersonalTurn(Turn):

    def receive_action(self, action):
        # print "\n\n\n", self._author, action.author, "\n\n\n"
        if action.author == self._author:
            self._action = action
