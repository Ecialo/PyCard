# -*- coding: utf-8 -*-
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class Desk(utility.Component):
    """
    Определяет контекст карт.
    """

    categories = [predef.DESK]

    def place_on(self, card, *args, **kwargs):
        card.change_context(self)

    def take_off(self, card):
        pass
