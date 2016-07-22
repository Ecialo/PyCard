# -*- coding: utf-8 -*-

import kivy.uix.floatlayout as flayout
import kivy.properties as prop
import kivy.uix.behaviors as beh
from core.utility import kivy_doc_hack

from kivy.lang import Builder

from core.predef import ui_namespace

__author__ = 'ecialo'

kivy_doc_hack(Builder, 'card_widget.kv', __file__)

class CardWidget(beh.DragBehavior, flayout.FloatLayout):

    card = prop.ObjectProperty()
    hand = prop.ObjectProperty()

    touch_pos = None
    origin = None

    game_widget = prop.ObjectProperty()
    player_widget = prop.ObjectProperty()


    touch_pos = None
    origin = None

    game_widget = prop.ObjectProperty()


    def __init__(self, card, **kwargs):
        super(CardWidget, self).__init__(**kwargs)
        self.card = card

    def on_touch_down(self, touch, *args):
        if self.origin == ui_namespace.card_types.FROM_ANOTHER_HAND:
            return False

        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.size_hint_y = None
            self.touch_pos = touch.pos

            if self.parent is not None:
                self.parent.remove_widget(self)
                self.game_widget.add_widget(self)

            return True

        return super(CardWidget, self).on_touch_down(touch, *args)


    def on_touch_move(self, touch, *args):
        if touch.grab_current == self:
            if self.touch_pos is None:
                self.touch_pos = touch.pos

            for i in xrange(2):
                self.center[i] += (touch.pos[i] - self.touch_pos[i])
            self.touch_pos = touch.pos
        return super(CardWidget, self).on_touch_move(touch, *args)


    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:

            player_widget = self.game_widget.player_widgets[self.game_widget.player_name]
            hand_widget = player_widget.widgets['hand']

            # карта вкладывается, если она либо лежит над рукой, либо её куда-то несли из руки, но не донесли
            if hand_widget.collide_point(*touch.pos) or self.origin == ui_namespace.card_types.FROM_OUR_HAND:
                self.parent.remove_widget(self)
                hand_widget.try_to_get_card(self, touch.pos)

                touch.ungrab(self)
                return True


            # представим, что тут написана логика для выкладывания карты на стол
            if False:
                return True


            # во всех остальных случаях карту надо удалить из игры
            # на самом деле, удаляется только виджет, а карта лежит где лежала

            self.parent.remove_widget(self)

        return super(CardWidget, self).on_touch_up(touch, *args)

