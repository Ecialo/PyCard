# -*- coding: utf-8 -*-
from ..action import Action
__author__ = 'ecialo'


class NextStage(Action):

    name = "next_stage"

    def apply(self):
        self.game.next_stage()

    def make_visible_response(self):
        return self

    def make_invisible_response(self):
        return self
