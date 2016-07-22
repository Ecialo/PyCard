# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
import kivy.properties as prop

from kivy.lang import Builder

from core.utility import kivy_doc_hack

__author__ = 'ecialo'
kivy_doc_hack(Builder, 'player_widget.kv', __file__)

class PlayerWidget(BoxLayout):

    player = prop.ObjectProperty()

    game_widget = prop.ObjectProperty()
    widgets = prop.DictProperty()

    def __init__(self, player, **kwargs):
        super(PlayerWidget, self).__init__(**kwargs)
        self.player = player
        self.widgets = {}

        associated_widgets = [component.make_widget(game_widget=self.game_widget, player_widget=self) for component in player.associated_components]
        for widget in associated_widgets:
            self.add_widget(widget=widget)
            if widget.name:
                self.widgets[widget.name] = widget
