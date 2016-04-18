# -*- coding: utf-8 -*-

import kivy
import kivy.properties as prop
from kivy.uix.label import Label
from kivy.lang import Builder

from core import predef

Builder.load_file('./client/game_ui/deck_widget/deck_widget.kv')

class DeckWidget(Label):
    deck = prop.ObjectProperty()
    game_widget = prop.ObjectProperty()

    def __init__(self, deck, **kwargs):
        super(DeckWidget, self).__init__(**kwargs)
        self.deck = deck

        self.register_event_type('on_remove_card')

    def on_touch_down(self, touch, *args):
        if self.deck.number_of_cards > 0:
            if self.collide_point(*touch.pos):
                card = self.game_widget.game.make_dummy_card()
                cw = card.make_widget(game_widget=self.game_widget)
                cw.size_hint_y = None
                cw.size = self.size
                cw.center = self.center
                cw.origin = predef.CARD_FROM_DECK
                self.game_widget.add_widget(cw)
                touch.grab(cw)

                return True

        return super(DeckWidget, self).on_touch_down(touch, *args)


    def on_remove_card(self, card):
        pass

