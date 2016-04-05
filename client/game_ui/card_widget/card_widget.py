# -*- coding: utf-8 -*-
import kivy
import kivy.uix.floatlayout as flayout
import kivy.uix.anchorlayout as alayout
import kivy.uix.relativelayout as rlayout
import kivy.uix.scatterlayout as slayout
import kivy.uix.widget as widget
import kivy.uix.label as label
import kivy.uix.button as button
import kivy.properties as prop
import kivy.uix.behaviors as beh

from kivy.lang import Builder

__author__ = 'ecialo'


class CardWidget(beh.DragBehavior, flayout.FloatLayout):

    card = prop.ObjectProperty()

    def __init__(self, card, **kwargs):
        super(CardWidget, self).__init__(**kwargs)
        self.card = card
        # print "\n\n\n\n", self.card, "\n\n\n\n"


Builder.load_file('./card_widget/card_widget.kv')