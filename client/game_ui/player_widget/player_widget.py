# -*- coding: utf-8 -*-
import kivy
import kivy.uix.floatlayout as flayout
import kivy.properties as prop

from kivy.lang import Builder

__author__ = 'ecialo'

Builder.load_file('./player_widget/player_widget.kv')


class PlayerWidget(flayout.FloatLayout):

    player = prop.ObjectProperty()

    def __init__(self, player):
        super(PlayerWidget, self).__init__()
        self.player = player