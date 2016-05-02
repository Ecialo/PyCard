# -*- coding: utf-8 -*-
import core.action.common_action_tables.game_action_table as game_action_table
import core.action.common_actions.draw_cards as draw_cards
import core.card.card as card
import core.card.card_table as card_table
import core.card.deck as deck
import core.flow.condition as cond
import core.flow.flow as flow
import core.flow.common_flows.score_calculation_flow as score
# import core.flow.turn as turn
from core.game import GameOver
import core.flow.common_turns.personal_turn as personal_turn
import core.flow.condition as cond

import core.flow.turn as turn
import core.game as game
import core.player as player
import core.predef as predef
import core.resource as resource
from client.tools.bind_widget import bind_widget
from core.action import common_system_actions
from core.action.common_action_tables import system_action_table

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


@bind_widget("HandWidget")
class RetardHandResource(resource.HandResource):
    pass


@bind_widget("PlayerWidget")
class RetardPlayer(player.Player):

    available_resources = [
        RetardHandResource
    ]


@bind_widget("CardWidget")
class RetardBlackCard(card.Card):

    name = "black_card"


@bind_widget("CardWidget")
class RetardWhiteCard(card.Card):

    name = "white_card"


@bind_widget("CardWidget")
class RetardBack(card.Card):

    name = predef.CARD_BACK


class RetardCardTable(card_table.CardTable):

    cards = [
        RetardBlackCard,
        RetardWhiteCard,
        RetardBack,
    ]


@bind_widget("DeckWidget")
class RetardDeck(deck.Deck):

    name = "retard_deck"

    content = [
        (RetardBlackCard.name, 5),
        (RetardWhiteCard.name, 5),
    ]


class RetardTurn(personal_turn.PersonalTurn):
    pass


class RetardScoreCalculation(score.ScoreCalculationFlow):
    pass


class RetardWinCondition(cond.WinCondition):

    def __call__(self, flow_game):
        flow_, game_ = flow_game
        if flow_ is None:
            players = game_.get_category(predef.PLAYER).values()
            players_black_cards = [player_.resources["hand"].cards().count("white_card") for player_ in players]
            players_names = [player_.name for player_ in players]
            leaders = enumerate(sorted(zip(players_black_cards, players_names), reverse=True))
            # print "b_cards", list(players_names)
            players_stats = {pos_struct[1][1]: (pos_struct[0], {'score': pos_struct[1][0]}) for pos_struct in leaders}
            raise GameOver(players_stats)


class RetardCondition(cond.Condition):

    def __init__(self, deck_):
        self._deck = deck_

    def __call__(self, (flow_, game_)):
        # print game_._components
        deck_ = game_[(predef.DECK, self._deck)]
        # print "\n\n\n", deck_.is_empty()
        return deck_.is_empty()


class RetardTurns(flow.TurnCycle):
    turn = RetardTurn
    condition = RetardCondition("retard_deck_0")


class RetardFlow(flow.Flow):
    flow = [RetardTurns]
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


@bind_widget("GameWidget")
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
            mode=mode,
            win_condition=RetardWinCondition()
        )

    def make_dummy_card(self):
        return RetardBack()

