# -*- coding: utf-8 -*-
import core.predef as predef
from kivy.app import App
from kivy.uix.button import Button
from sample_games.retard_game import retard_game
__author__ = 'ecialo'


class TestApp(App):

    def build(self):
        retard_game_ = retard_game.RetardGame(
            [
                {'name': 'Eustas'},
                {'name': 'Spooky'}
            ],
            mode=predef.CLIENT
        )
        players = retard_game_.get_category(predef.PLAYER).itervalues()
        hands = [player.associated_components[0] for player in players]
        # print "\n\n\nHands\n", hands
        retard_game_widget = retard_game_.make_widget()
        retard_game_widget.add_widget(
            Button(
                text=hands[0].fullname,
                size_hint=(0.1, 0.1),
                pos=(0, 250),
                on_press=lambda self_: hands[0].get_cards("black_card")
            )
        )
        return retard_game_widget

if __name__ == '__main__':
    TestApp().run()
