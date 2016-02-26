# -*- coding: utf-8 -*-
from ..action import Action
__author__ = 'ecialo'


class DrawCards(Action):
    """
    Тянем карты из чего-то куда-то.

    @param number: Сколько карт нужно вытянуть
    @type number: int
    @param source:
    @type source: core.card.deck.Deck
    @param target:
    @type target: core.card.hand.Hand
    """

    name = "draw_cards"
    default_args = {
        'number': 1
    }

    def __init__(self, **kwargs):
        self.source = None
        self.target = None
        self.number = None
        super(DrawCards, self).__init__(**kwargs)

    def apply(self):
        cards = []
        for _ in xrange(self.number):
            card = self.source.draw_card()
            cards.append(card)
        self.target.get_cards(*cards)
        return {'cards': cards}
