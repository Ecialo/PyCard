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
    game = prop.ObjectProperty()
    hand = prop.ObjectProperty()

    def __init__(self, card, **kwargs):
        super(CardWidget, self).__init__(**kwargs)
        self.card = card
        # print "\n\n\n\n", self.card, "\n\n\n\n"
    
    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            touch.grab(self)            
            self.size_hint_y = None

            self.hand.remove_widget(self)
            self.game.add_widget(self)
            self.center = touch.pos
            return True

        return super(CardWidget, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        if touch.grab_current == self:
            self.center = touch.pos

        return super(CardWidget, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            self.game.remove_widget(self)
            self.hand.add_widget(self)

            self.size_hint_y = 1
            touch.ungrab(self)
            return True

        return super(CardWidget, self).on_touch_up(touch, *args)


Builder.load_file('./card_widget/card_widget.kv')
