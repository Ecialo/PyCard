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

from core import predef

__author__ = 'ecialo'


class CardWidget(beh.DragBehavior, flayout.FloatLayout):

    card = prop.ObjectProperty()
    hand = prop.ObjectProperty()

    touch_pos = None
    origin = None

    game_widget = prop.ObjectProperty()
    player_widget = prop.ObjectProperty()


    def __init__(self, card, **kwargs):
        super(CardWidget, self).__init__(**kwargs)
        self.card = card

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.size_hint_y = None
            self.touch_pos = touch.pos
     
            self.hackity_hack = self.parent.parent.parent
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

            # попытка вложить карту в руку: на самом деле нам нужна не рука, а scroll view, в котором она лежит
            # карта вкладывается, если она либо лежит над рукой, либо её куда-то несли из руки, но не донесли

            if self.player_widget is not None:
                #hw = self.player_widget.widgets['hand'] # это не работает

                hw = self.hackity_hack
                if hw.collide_point(*touch.pos) or self.origin == predef.CARD_FROM_HAND:
                    self.parent.remove_widget(self)
                    hw.ui_add_card_widget(self, touch.pos)

                    self.origin = predef.CARD_FROM_HAND
                    self.size_hint_y = 1
                    touch.ungrab(self)

                    # если карта из руки, то, собственно, ничего не нужно делать
                    # если карта из дека, нужно её оттуда убрать
                    # TODO: убрать карту из дека

                    return True


            # представим, что тут написана логика для выкладывания карты на стол
            if False:
                return True


            # во всех остальных случаях карту надо удалить из игры
            # на самом деле, удаляется только виджет, а карта лежит где лежала

            self.parent.remove_widget(self)
           
        return super(CardWidget, self).on_touch_up(touch, *args)


Builder.load_file('./card_widget/card_widget.kv')

