# -*- coding: utf-8 -*-
from .. import action
from ... import predef
from ..common_system_actions import *
__author__ = 'ecialo'


class DrawCards(action.Action):
    """
    Тянем карты из чего-то куда-то.

    :param number: Сколько карт нужно вытянуть
    :type number: int
    :param source:
    :type source: core.card.deck.Deck
    :param target:
    :type target: core.card.hand.Hand
    """

    name = "draw_cards"
    default_args = {
        'number': 1
    }

    def __init__(self, author, **kwargs):
        self.source = None
        self.target = None
        self.number = None
        self._cards = None
        super(DrawCards, self).__init__(author, **kwargs)

    def check(self):
        return self.source.number_of_cards > 0

    def apply(self):
        cards = []
        for _ in xrange(self.number):
            card = self.source.draw_card()
            cards.append(card)
        self._cards = cards
        self.target.get_cards(*cards)
        return {'cards': cards}

    def make_invisible_response(self):
        cards = [None for _ in xrange(self.number)]
        cards_backs = [predef.CARD_BACK for _ in xrange(self.number)]
        remove = remove_cards.RemoveCards(
            predef.SYSTEM,
            target=self.source,
            cards=cards
            )
        append = append_cards.AppendCards(
            predef.SYSTEM,
            target=self.target,
            cards=cards_backs
        )
        return remove & append

    def make_visible_response(self):
        cards = self._cards
        remove = remove_cards.RemoveCards(
            predef.SYSTEM,
            target=self.source,
            cards=cards
            )
        append = append_cards.AppendCards(
            predef.SYSTEM,
            target=self.target,
            cards=cards
        )
        return remove & append

if __name__ == '__main__':
    draw_cards = DrawCards(
        author="system",
        source="Ololo",
        target="Azaza",
        _cards=["push"]
    )
    print draw_cards.make_visible_response().make_message()
    print draw_cards.make_message()
