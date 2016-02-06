# -*- coding: utf-8 -*-
__author__ = 'ecialo'
import test_reactor

test_reactor.test("olo2324lo")
#
# from core.game import Game
# from core.flow.turn import Turn
# from core.flow.flow import Flow
# from core.flow.flow import TurnCycle
# from core.player import Player
# from core.flow.condition import CyclesExceedCondition
# from core.card.card import Card
# from core.card.card_table import CardTable
# from core.card.deck import Deck
# from core.resource import HandResource
# from core.generic_componets.flows import SelectFirstPlayerAtRandom
# from core.generic_componets.resources import FirstPlayerToken
# from core.predef import FIRST_PLAYER_TOKEN
# # from core.flow.flow import Flow
# __author__ = 'Ecialo'
#
#
# class PassFlow(TurnCycle):
#
#     turn = Turn
#     condition = CyclesExceedCondition(3)
#
#
# class TestFlow(Flow):
#
#     flow = [SelectFirstPlayerAtRandom, TurnCycle]
#
#
# class TestGame(Game):
#
#     def __init__(self, components):
#         super(TestGame, self).__init__(components, TestFlow)
#
#
# class TestCard(Card):
#
#     name = "card"
#
#
# class TestCardTable(CardTable):
#
#     cards = [TestCard]
#
#
# class TestDeck(Deck):
#
#     name = "test_deck"
#     content = [
#         ("card", 30)
#     ]
#
#
# class TestPlayer(Player):
#
#     available_resources = [
#         HandResource,
#         FirstPlayerToken,
#     ]

if __name__ == '__main__':
    test_reactor.run()