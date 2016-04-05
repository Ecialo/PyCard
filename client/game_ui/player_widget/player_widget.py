# -*- coding: utf-8 -*-
import kivy
import kivy.uix.floatlayout as flayout
import kivy.properties as prop

from kivy.lang import Builder

__author__ = 'ecialo'

Builder.load_file('./player_widget/player_widget.kv')


class PlayerWidget(flayout.FloatLayout):

    player = prop.ObjectProperty()

    def __init__(self, player, **kwargs):
        super(PlayerWidget, self).__init__(**kwargs)
        self.ids = kwargs.get('ids')
        self.player = player

        associated_widgets = [component.make_widget(ids={'game': self.ids.game, 'player': self}) for component in player.associated_components]
        for widget in associated_widgets:
            # widget.ids.game = self.ids.game
            self.add_widget(widget=widget)
