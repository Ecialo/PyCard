# -*- coding: utf-8 -*-
__author__ = 'Ecialo'


class Condition(object):

    def __call__(self, target):
        return True


class CyclesExceedCondition(Condition):

    def __init__(
            self,
            max_value
    ):
        self._max_value = max_value

    def __call__(self, target):
        if target.cycles >= self._max_value:
            return True
        else:
            return False
