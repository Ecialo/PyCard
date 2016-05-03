# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import kivy.properties as prop


Builder.load_file('./client/client_ui/lobby_screen.kv')


class LobbyScreen(Screen):
    app = prop.ObjectProperty()

    def __init__(self, app, **kwargs):
        super(LobbyScreen, self).__init__(**kwargs)
        self.app = app
        self.ids.ready_checkbox.bind(state=self.on_ready_clicked)


    # Обработка событий с виджетов

    def on_ready_clicked(self, checkbox, state):
        if state == 'down':
            self.app.send_lobby_ready()
        else:
            self.app.send_lobby_not_ready()

    def notify(self, text):
        """
        Показывает уведомление вверху экрана.
        """

        self.nm.notify(text)
