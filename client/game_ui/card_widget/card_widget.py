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
    
    touch_pos = None

    def __init__(self, card, **kwargs):
        super(CardWidget, self).__init__(**kwargs)
        self.card = card
        # print "\n\n\n\n", self.card, "\n\n\n\n"
    
    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.size_hint_y = None
            self.touch_pos = touch.pos
 
            if self.parent != self.game:
                self.hand.remove_widget(self)
                self.game.add_widget(self)
            return True

        return super(CardWidget, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        if touch.grab_current == self:
            for i in xrange(2):
                self.center[i] += (touch.pos[i] - self.touch_pos[i])
            self.touch_pos = touch.pos
        return super(CardWidget, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            player_hand_zone = self.hand.parent # scroll_view
            if player_hand_zone.collide_point(*touch.pos):
                self.game.remove_widget(self)

                for i,c in enumerate(self.hand.children):
                    if c.collide_point(*touch.pos):
                        self.hand.add_widget(self, i)
                        break
                else:
                    self.hand.add_widget(self)

                self.size_hint_y = 1
                touch.ungrab(self)
                return True

        return super(CardWidget, self).on_touch_up(touch, *args)


Builder.load_file('./card_widget/card_widget.kv')
