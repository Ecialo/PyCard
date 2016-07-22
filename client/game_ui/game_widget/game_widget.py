# -*- coding: utf-8 -*-

from kivy.uix import tabbedpanel
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import kivy.properties as prop

from core.predef import game_component_types
from core.utility import kivy_doc_hack

__author__ = 'ecialo'
kivy_doc_hack(Builder, 'game_widget.kv', __file__)

class GameWidget(Screen):

    app = prop.ObjectProperty()
    game = prop.ObjectProperty()

    player_name = prop.StringProperty()
    current_turn_author = prop.StringProperty()
    player_widgets = prop.DictProperty()
    deck_widget = prop.ObjectProperty()

    pending_actions = []
    player_tab_title = '* You *'

    def __init__(self, game, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.game = game
        self.player_name = self.app.player_name

        self.player_widgets = {player.name: player.make_widget(game_widget=self) \
            for player in self.game.get_category(game_component_types.PLAYER).itervalues()}

        self.add_player_widget(self.player_widgets[self.player_name])
        for widget in self.player_widgets.itervalues():
            if widget.player.name != self.player_name:
                self.add_player_widget(widget)

        deck_zone = self.ids.deck_zone
        self.deck_widget = self.game.get_category(game_component_types.DECK).values()[0].make_widget(game_widget=self)
        deck_zone.add_widget(self.deck_widget)

        self.update_current_turn_author()

    def update_current_turn_author(self):
        self.current_turn_author = self.game.current_flow._author

    def is_our_turn(self):
        #print("Current player: {0}".format(self.game.current_flow._author))
        return self.player_name == self.current_turn_author

    def is_our_tab_active(self):
        #print("Active tab: {0}".format(self.ids.player_zone.current_tab.text))
        return self.ids.player_zone.current_tab.text == self.player_tab_title

    def add_player_widget(self, widget):
        caption = self.player_tab_title if widget.player.name == self.player_name else widget.player.name
        tab = tabbedpanel.TabbedPanelItem(text=caption)
        tab.add_widget(widget=widget)
        self.ids.player_zone.add_widget(tab)

    def queue_action(self, action):
        self.pending_actions.append(action)
        print(self.pending_actions)

    def send_actions(self, *actions):
        for action in actions:
            msg = action.make_message()
            self.app.send_action(msg)

    def push_game_forward(self, action):
        self.game.receive_message(action)
        self.update_current_turn_author()

    def notify(self, text):
        self.app.notify(text)
