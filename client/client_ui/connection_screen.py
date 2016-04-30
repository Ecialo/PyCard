# -*- coding: utf-8 -*-

import io, sys
import json

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import kivy.properties as prop


Builder.load_file('./client/client_ui/connection_screen.kv')


class ConnectionScreen(Screen):
    app = prop.ObjectProperty()

    def __init__(self, app, **kwargs):
        super(ConnectionScreen, self).__init__(**kwargs)
        self.app = app

    def connect(self, host, port, name):
        if not host or not port or not name:
            l = []
            if not host:
                l.append('host')
            if not port:
                l.append('port')
            if not name:
                l.append('name')

            err = 'The following fields are empty: {fields}'.format(
                fields=', '.join(l))
            self.app.notify(err)
            return

        self.app.player_name = name
        self.app.connect_to_server(host=host, port=int(port))

    def cancel(self):
        self.app.stop()
