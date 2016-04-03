# -*- coding: utf-8 -*-
__author__ = 'ecialo'

import kivy
import kivy.uix.floatlayout as flayout
import kivy.uix.anchorlayout as alayout
import kivy.uix.relativelayout as rlayout
import kivy.uix.stacklayout as slayout
import kivy.uix.widget as widget
import kivy.uix.label as label
import kivy.uix.button as button
import kivy.properties as prop

from kivy.lang import Builder


class HandWidget(slayout.StackLayout):

    hand = prop.ObjectProperty()
    cards = prop.ListProperty()

    def __init__(self, hand, **kwargs):
        super(HandWidget, self).__init__(**kwargs)
        self.hand = hand
        self.register_event_type('on_get_cards')

    def on_get_cards(self, *cards):
        self.cards.extend(cards)


Builder.load_file('./hand_widget/hand_widget.kv')