# -*- coding: utf-8 -*-
__author__ = 'ecialo'

from ..action import Action


class DrawCards(Action):

    default_args = {
        'number': 1
    }

    def __init__(self, **kwargs):
        self.source = None
        self.target = None
        self.number = None
        super(DrawCards, self).__init__(**kwargs)

    def apply(self):
        pass