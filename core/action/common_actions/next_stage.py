# -*- coding: utf-8 -*-
from ..action import Action
__author__ = 'ecialo'


class NextStage(Action):

    name = "next_stage"

    def apply(self):
        self.game.next_stage()