# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from . import card_widget
from . import hand_widget
from .bind_widget import bind_widget

from sample_games.retard_game.retard_game import RetardBlackCard
from sample_games.retard_game.retard_game import RetardCardTable
from core.card.hand import Hand
__author__ = 'ecialo'


@bind_widget(hand_widget.HandWidget)
class NewCoolHand(Hand):

    table = RetardCardTable()

    def __init__(self):
        super(NewCoolHand, self).__init__()
        self.get_cards([RetardBlackCard.name for _ in xrange(5)])


@bind_widget(card_widget.CardWidget)
class NewCoolBlackCard(RetardBlackCard):
    pass


class RootWidget(FloatLayout):
    pass


class TestApp(App):
    def build(self):
        root = RootWidget()
        # card = NewCoolBlackCard().make_widget(pos=(100, 100))
        hand = NewCoolHand().make_widget()
        # card.pos = (100, 100)
        # root.add_widget(card)
        root.add_widget(hand)
        return root

if __name__ == '__main__':
    TestApp().run()