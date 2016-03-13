# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from .card_widget import card_widget
from .bind_widget import bind_widget
from sample_games.retard_game.retard_game import RetardBlackCard
__author__ = 'ecialo'


@bind_widget(card_widget.CardWidget)
class NewCoolBlackCard(RetardBlackCard):
    pass


class RootWidget(FloatLayout):
    pass


class TestApp(App):
    def build(self):
        root = RootWidget()
        card = NewCoolBlackCard().make_widget(pos=(100, 100))
        # card.pos = (100, 100)
        root.add_widget(card)
        return root

if __name__ == '__main__':
    TestApp().run()