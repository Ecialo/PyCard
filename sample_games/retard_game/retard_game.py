# -*- coding: utf-8 -*-
import core.game as game
import core.player as player
import core.resource as resource

import core.action.common_action_tables.game_action_table as game_action_table
from core.action.common_action_tables import system_action_table
import core.action.common_actions.draw_cards as draw_cards
from core.action import common_system_actions

import core.card.card as card
import core.card.card_table as card_table
import core.card.deck as deck

import core.flow.flow as flow
import core.flow.turn as turn
import core.flow.condition as cond

import core.predef as predef
from client.game_ui.bind_widget import bind_widget
from client.game_ui.game_widget import GameWidget
from client.game_ui.player_widget import PlayerWidget
from client.game_ui.hand_widget import HandWidget
from client.game_ui.card_widget import CardWidget
from client.game_ui.deck_widget import DeckWidget

__author__ = 'ecialo'


class RetardActionTable(game_action_table.GameActionTable):
    actions = [
        draw_cards.DrawCards,
    ]


class RetardSystemActionTable(system_action_table.SystemActionTable):
    actions = [
        common_system_actions.append_cards.AppendCards,
        common_system_actions.remove_cards.RemoveCards,
        common_system_actions.next_stage.NextStage,
    ]


@bind_widget(HandWidget)
class RetardHandResource(resource.HandResource):
    pass


@bind_widget(PlayerWidget)
class RetardPlayer(player.Player):

    available_resources = [
        RetardHandResource
    ]

@bind_widget(CardWidget)
class RetardBlackCard(card.Card):

    name = "black_card"

@bind_widget(CardWidget)
class RetardWhiteCard(card.Card):

    name = "white_card"


class RetardBack(card.Card):

    name = predef.CARD_BACK


class RetardCardTable(card_table.CardTable):

    cards = [
        RetardBlackCard,
        RetardWhiteCard,
    ]

@bind_widget(DeckWidget)
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
        # print game_._components
        deck_ = game_[(predef.DECK, self._deck)]
        return deck_.is_empty()


class RetardFlow(flow.TurnCycle):
    turn = RetardTurn
    condition = RetardCondition("retard_deck_0")

# player1 = RetardPlayer('Eustace')
# player2 = RetardPlayer('Spooky')
# retard_deck = RetardDeck()
# retard_card_table = RetardCardTable()
# retard_action_table = RetardActionTable()

# retard_components = [
#     retard_action_table,
#     retard_card_table,
#     retard_deck,
#     # player1,
#     # player2,
# ]
#
# player1_draw_card = draw_cards.DrawCards(
#     author=player1,
#     source=retard_deck,
#     target=player1.resources["hand"]
# )
# player2_draw_card = draw_cards.DrawCards(
#     author=player2,
#     source=retard_deck,
#     target=player2.resources["hand"]
# )


@bind_widget(GameWidget)
class RetardGame(game.Game):

    name = "retard_game"

    def __init__(self, players, mode=predef.SERVER):
        players = [player if isinstance(player, RetardPlayer) else RetardPlayer(**player) for player in players]
        retard_deck = RetardDeck()
        retard_card_table = RetardCardTable()
        retard_action_table = RetardActionTable()
        retard_system_action_table = RetardSystemActionTable()
        retard_components = [
            retard_action_table,
            retard_card_table,
            retard_system_action_table,
            retard_deck,
            # player1,
            # player2,
        ]

        super(RetardGame, self).__init__(
            components=retard_components + players,
            flow=RetardFlow,
            mode=mode
        )
