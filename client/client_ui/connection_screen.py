# -*- coding: utf-8 -*-
""" Test client """

import io, sys
import json

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
import kivy.properties as prop

import core.predef as predef


Builder.load_file('./client/client_ui/connection_screen.kv')


class ConnectionScreen(Screen):
    app = prop.ObjectProperty()

    def __init__(self, app, **kwargs):
        super(ConnectionScreen, self).__init__(**kwargs)
        self.app = app

    def connect(self, server, port, name):
        self.app.player_name = name
        self.app.connect_to_server(host=server, port=port)

    def cancel(self):
        self.app.stop()
