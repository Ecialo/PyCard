# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from . import card_widget
from . import hand_widget
from .bind_widget import bind_widget

from sample_games.retard_game.retard_game import RetardBlackCard
# from sample_games.retard_game.retard_game import RetardCardTable

from core.card.hand import Hand
from core.card.card_table import CardTable
__author__ = 'ecialo'


@bind_widget(card_widget.CardWidget)
class NewCoolBlackCard(RetardBlackCard):
    pass


class CoolCardTable(CardTable):

    cards = [
        NewCoolBlackCard,
    ]


@bind_widget(hand_widget.HandWidget)
class NewCoolHand(Hand):

    table = CoolCardTable()

    def __init__(self):
        super(NewCoolHand, self).__init__()
        # self.get_cards([RetardBlackCard.name for _ in xrange(5)])


class RootWidget(FloatLayout):
    pass


class TestApp(App):
    def build(self):
        root = RootWidget()
        # card = NewCoolBlackCard().make_widget(pos=(100, 100))
        hand = NewCoolHand()
        widget_ = hand.make_widget()
        # card.pos = (100, 100)
        # root.add_widget(card)
        root.add_widget(widget_)

        button = Button(pos=(200, 200), text="add card")
        button.bind(on_press=lambda x: hand.get_cards(NewCoolBlackCard.name))
        root.add_widget(button)
        return root

if __name__ == '__main__':
    TestApp().run()