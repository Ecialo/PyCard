# -*- coding: utf-8 -*-
from core.action import action
from core.action.common_system_actions import *
__author__ = 'ecialo'


class PlayAsAttack(action.Action):

    def __init__(self, author, **kwargs):
        self.hand = None
        self.card = None
        self.desk = None

        self._card = None

        super(PlayAsAttack, self).__init__(author, **kwargs)

    def apply(self):
        card = self.card
        self.hand.remove_card(card.name)
        self._card = self.game.make_card(card.name)
        self.desk.place_on(self._card)

    def check(self):
        pass

    def make_visible_response(self):
        pass

    def make_invisible_response(self):
        pass


class PlayAsDefend(action.Action):

    def __init__(self, author, **kwargs):
        self.card = None
        self.desk = None
        super(PlayAsDefend, self).__init__(author, **kwargs)

    def apply(self):
        pass

    def make_visible_response(self):
        pass

    def make_invisible_response(self):
        pass


class Grab(action.Action):

    def __init__(self, author, **kwargs):
        self.hand = None
        self.desk = None
        super(Grab, self).__init__(author, **kwargs)

    def apply(self):
        pass

    def make_visible_response(self):
        pass

    def make_invisible_response(self):
        pass
