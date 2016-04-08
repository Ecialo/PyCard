# -*- coding: utf-8 -*-
__author__ = 'ecialo'

import kivy
from kivy.uix.gridlayout import GridLayout
import kivy.properties as prop
from kivy.lang import Builder

class UnorderedDeskWidget(GridLayout):

    cards = prop.ListProperty()

    def __init__(self, **kwargs):
        pass
    
    def on_place_on(self, *cards, **kwargs):
        pass

    def on_take_off(self, *cards, **kwargs):
        pass

