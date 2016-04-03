# -*- coding: utf-8 -*-
import core.predef as predef
from kivy.app import App
from sample_games.retard_game.retard_game import RetardGame
__author__ = 'ecialo'


class TestApp(App):

    def build(self):
        retard_game = RetardGame(
            [{'name': 'Eustas'}, {'name': 'Spooky'}],
            mode=predef.CLIENT
        )
        return retard_game.make_widget()

if __name__ == '__main__':
    TestApp().run()