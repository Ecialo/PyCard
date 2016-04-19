# -*- coding: utf-8 -*-
from .. import test_reactor
from sample_games.retard_game import retard_game
__author__ = 'ecialo'


class TestRetardGame(test_reactor.TestGame):
    game = retard_game.RetardGame
    path_to_scenarios = "./testing/game_scenarios/retard_game"

if __name__ == '__main__':
    game = retard_game.RetardGame
    test_reactor.test(game)
