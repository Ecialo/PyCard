# -*- coding: utf-8 -*-
from .. import action
__author__ = 'ecialo'


class PlaceOnDesk(action.Action):

    def __init__(self, **kwargs):
        self.desk = None
        self.card = None
        super(PlaceOnDesk, self).__init__(**kwargs)

    def apply(self):
        self.desk.place_on(self.card)
