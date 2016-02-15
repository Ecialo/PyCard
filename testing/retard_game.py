# -*- coding: utf-8 -*-
import core.game as game
import core.player as player
import core.resource as resource

import core.action.action_table as action_table
import core.action.common_actions.draw_cards as draw_cards

import core.card.card as card
import core.card.card_table as card_table
import core.card.deck as deck

import core.flow.flow as flow
import core.flow.turn as turn
import core.flow.condition as cond

import core.predef as predef

import testing.test_reactor as test
__author__ = 'ecialo'


class RetardActionTable(action_table.ActionTable):
    actions = [
        draw_cards.DrawCards,
    ]


class RetardPlayer(player.Player):

    available_resources = [
        resource.HandResource
    ]


class RetardBlackCard(card.Card):

    name = "black_card"


class RetardWhiteCard(card.Card):

    name = "white_card"


class RetardCardTable(card_table.CardTable):

    cards = [
        RetardBlackCard,
        RetardWhiteCard,
    ]


class RetardDeck(deck.Deck):

    name = "retard_deck"

    content = [
        (RetardBlackCard.name, 5),
        (RetardWhiteCard.name, 5),
    ]


class RetardTurn(turn.Turn):
    pass


class RetardCondition(cond.Condition):

    def __init__(self, deck_):
        self._deck = deck_

    def __call__(self, (flow_, game_)):
        deck_ = game_[(predef.DECK, self._deck)]
        return deck_.is_empty()


class RetardFlow(flow.TurnCycle):

    turn = RetardTurn

player1 = RetardPlayer('Eustace')
player2 = RetardPlayer('Spooky')

retard_components = [
    RetardActionTable(),
    RetardCardTable(),
    RetardDeck(),
    player1,
    player2,
]


class RetardGame(game.Game):
    def __init__(self):
        super(RetardGame, self).__init__(
            components=retard_components,
            flow=RetardFlow
        )

if __name__ == '__main__':
    pass
