# -*- coding: utf-8 -*-
from flow import EndOfCurrentFlow
__author__ = 'Ecialo'

# TODO Rewrite all


def make_factory(**default_kwargs):

    def run_or_init_with_kwargs(func_or_class):

        def new_func_or_class(*args, **kwargs):
            default_kwargs.update(kwargs)
            return func_or_class(*args, **default_kwargs)

        return new_func_or_class()

    return run_or_init_with_kwargs


class Turn(object):
    """
    Ожидает определённое действие конкретного игрока
    """
    def __init__(self, target):
        self._target = target
        self.is_runned = False
        self._action = None

    def receive_action(self, action):
        print "rec"
        self._action = action

    def run(self):
        print "runned"
        if not self.is_runned and self._action:
            # print "HOO-HOO"
            self.is_runned = True
            return self._action
        elif self.is_runned:
            self._action = None
            self.is_runned = False
            raise EndOfCurrentFlow()

