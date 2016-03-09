# -*- coding: utf-8 -*-
from .. import test_reactor
from sample_games.retard_game import retard_game
__author__ = 'ecialo'


class SubRetardGame(retard_game.RetardGame):    # TODO выпилить как только будет возможность делать предустановки в сценариях

    def __init__(self):
        super(SubRetardGame, self).__init__([retard_game.player1, retard_game.player2])


class TestRetardGame(test_reactor.TestGame):
    game = SubRetardGame
    path_to_scenarios = "./testing/game_scenarios/retard_game"