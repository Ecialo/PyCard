# -*- coding: utf-8 -*-
import core.game as game
import core.player as player

import core.card.card as card
import core.card.card_table as card_table
import core.card.deck as deck

import core.flow.flow as flow
import core.flow.turn as turn
import core.flow.condition as cond

import testing.test_reactor as test
__author__ = 'ecialo'


class RetardPlayer(player.Player):
    pass


class RetardBlackCard(card.Card):

    name = "black_card"


class RetardWhiteCard(card.Card):

    name = "white_card"


class RetardCardTable(card_table.CardTable):
    pass


class RetardDeck(deck.Deck):
    pass


class RetardTurn(turn.Turn):
    pass


class RetardCondition(cond.Condition):
    pass

player1 = RetardPlayer('Eustace')
player2 = RetardPlayer('Spooky')

if __name__ == '__main__':
    pass
