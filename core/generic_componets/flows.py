#! /usr/bin/python
# -*- coding: utf-8 -*-
from .. import utility
from .. import predef
from ..flow import (
    flow,
    condition,
)
# import resources
import random as rnd
__author__ = 'Ecialo'


class SelectFirstPlayerAtRandom(flow.Cycle):
    """
    Случайным образом выбирает первого игрока.
    """

    condition = condition.CyclesExceedCondition(1)
    associated_components = []

    def run(self):
        super(SelectFirstPlayerAtRandom, self).run()
        first_player = rnd.choice(self._players)
        first_player_token = first_player.resources[predef.FIRST_PLAYER_TOKEN].fullname
        return utility.make_message('select_first_player', token_path=first_player_token)