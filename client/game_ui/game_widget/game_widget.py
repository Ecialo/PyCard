# -*- coding: utf-8 -*-
import kivy
import kivy.uix.floatlayout as flayout
from kivy.uix import tabbedpanel
import kivy.properties as prop
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from core import predef

__author__ = 'ecialo'
#Builder.load_file('./client/game_ui/game_widget/game_widget.kv')

class GameWidget(Screen):

    game = prop.ObjectProperty()

    def __init__(self, game, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.game = game

        player_widgets = [player.make_widget(game_widget=self) for player in self.game.get_category(predef.PLAYER).itervalues()]
        player_zone = self.ids.player_zone

        for widget in player_widgets:
            tab = tabbedpanel.TabbedPanelItem(text=widget.player.name)
            tab.add_widget(widget=widget)
            player_zone.add_widget(tab)

        deck_zone = self.ids.deck_zone
        deck_widgets = [deck.make_widget(game_widget=self) for deck in self.game.get_category(predef.DECK).itervalues()]
        for w in deck_widgets:
            deck_zone.add_widget(w)

