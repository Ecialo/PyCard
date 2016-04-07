# -*- coding: utf-8 -*-
__author__ = 'ecialo'

import kivy
import kivy.uix.floatlayout as flayout
import kivy.uix.anchorlayout as alayout
import kivy.uix.relativelayout as rlayout
import kivy.uix.stacklayout as slayout
import kivy.uix.boxlayout as blayout
import kivy.uix.widget as widget
import kivy.uix.label as label
import kivy.uix.button as button
import kivy.properties as prop

from kivy.lang import Builder


class HandWidget(blayout.BoxLayout):

    hand = prop.ObjectProperty()
    cards = prop.ListProperty()
    
    def __init__(self, hand, **kwargs):
        super(HandWidget, self).__init__(**kwargs)
        #self.ids = kwargs.get('ids')
        self.hand = hand
        
        self.register_event_type('on_get_cards')

    def on_get_cards(self, *cards):
        for card in cards:
            card = self.ids.game.game.view_card(card)
            
            card_widget = card.make_widget(game=self.ids.game, hand=self.ids.card_stack)
            self.ids.card_stack.add_widget(widget=card_widget)

Builder.load_file('./hand_widget/hand_widget.kv')
