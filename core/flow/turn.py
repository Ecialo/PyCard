# -*- coding: utf-8 -*-
from flow import EndOfCurrentFlow
__author__ = 'Ecialo'


class Turn(object):
    """
    Ожидает определённое действие конкретного игрока
    """
    def __init__(self, target):
        self._target = target
        self.is_runned = False
        self._action = None

    def receive_action(self, action):
        # print "rec"
        self._action = action

    @staticmethod
    def next_stage():
        raise EndOfCurrentFlow()

    def current_flow(self):
        return self

    def run(self):
        if not self.is_runned and self._action:
            # print "HOO-HOO"
            self.is_runned = True
            return self._action
        elif self.is_runned:
            self._action = None
            self.is_runned = False
            raise EndOfCurrentFlow()

