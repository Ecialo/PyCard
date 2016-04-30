# -*- coding: utf-8 -*-
import kivy
import kivy.uix.floatlayout as flayout
from kivy.uix import tabbedpanel
import kivy.properties as prop
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from core.predef import game_component_types

__author__ = 'ecialo'
Builder.load_file('./client/game_ui/game_widget/game_widget.kv')

class GameWidget(Screen):

    app = prop.ObjectProperty()
    game = prop.ObjectProperty()

    player_name = prop.StringProperty()
    player_widgets = prop.DictProperty()
    deck_widget = prop.ObjectProperty()

    pending_actions = []

    def __init__(self, game, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.game = game
        self.player_name = self.app.player_name

        self.player_widgets = {player.name: player.make_widget(game_widget=self) \
            for player in self.game.get_category(game_component_types.PLAYER).itervalues()}
        player_zone = self.ids.player_zone

        idx = None
        for i, widget in enumerate(self.player_widgets.itervalues()):
            tab = tabbedpanel.TabbedPanelItem(text=widget.player.name)
            tab.add_widget(widget=widget)
            player_zone.add_widget(tab)
            if widget.player.name == self.player_name:
                idx = i

        tl = player_zone.tab_list
        tl[0], tl[idx] = tl[idx], tl[0]
        player_zone.switch_to(tl[0]) # почему это не работает.

        deck_zone = self.ids.deck_zone
        self.deck_widget = self.game.get_category(game_component_types.DECK).values()[0].make_widget(game_widget=self)
        deck_zone.add_widget(self.deck_widget)

    def is_our_turn(self):
        #print("Current player: {0}".format(self.game.current_flow._author))
        return self.player_name == self.game.current_flow._author

    def is_our_tab_active(self):
        #print("Active tab: {0}".format(self.ids.player_zone.current_tab.text))
        return self.player_name == self.ids.player_zone.current_tab.text

    def queue_action(self, action):
        self.pending_actions.append(action)
        print(self.pending_actions)

    def send_actions(self, *actions):
        for action in actions:
            msg = action.make_message()
            self.app.send_action(msg)

    def push_game_forward(self, *actions):
        for action in actions:
            pass

    def notify(self, text):
        self.app.notify(text)

