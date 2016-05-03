# -*- coding: utf-8 -*-
import core.predef as predef
from kivy.app import App
from kivy.uix.button import Button
from sample_games.retard_game import retard_game
from random import choice

__author__ = 'ecialo'


class TestApp(App):

    def build(self):
        self.player_name = 'Spooky'
        retard_game_ = retard_game.RetardGame(
            [
                {'name': 'Eustas'},
                {'name': 'Spooky'}
            ],
            mode=predef.CLIENT
        )
        players = retard_game_.get_category(predef.PLAYER).itervalues()
        hands = [player.associated_components[0] for player in players]

        retard_game_widget = retard_game_.make_widget(app=self)
        # retard_game_widget.add_widget(
        #     Button(
        #         text=hands[0].fullname,
        #         size_hint=(0.1, 0.1),
        #         pos=(50, 250),
        #         on_press=lambda self_: hands[0].get_cards(choice(["black_card", "white_card"]))
        #     )
        # )
        # retard_game_widget.add_widget(
        #     Button(
        #         text=hands[1].fullname,
        #         size_hint=(0.1, 0.1),
        #         pos=(250, 250),
        #         on_press=lambda self_: hands[1].get_cards(choice(["black_card", "white_card"]))
        #     )
        # )

        return retard_game_widget

    def send_action(self, action):
        pass

if __name__ == '__main__':
    TestApp().run()
