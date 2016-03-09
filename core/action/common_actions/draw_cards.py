# -*- coding: utf-8 -*-
from ..action import Action
__author__ = 'ecialo'


class DrawCards(Action):
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

    def apply(self):
        cards = []
        for _ in xrange(self.number):
            card = self.source.draw_card()
            cards.append(card)
        self._cards = cards
        self.target.get_cards(*cards)
        return {'cards': cards}

    def make_invisible_response(self):
        pass

    def make_visible_response(self):
        pass
