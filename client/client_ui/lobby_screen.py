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

    def print_message(self, msg):
        """
        Выводит текст в чат.
        """

        self.ids.chatlog.text += msg + "\n"
        self.scroll_if_necessary()
        self.ids.input_field.focus = True

    def scroll_if_necessary(self):
        """
        Прокручивает чат, если в нижней части скрыто более 2 строк текста.
        Судя по наблюдениям за интерфейсом, каждая строка имеет высоту 1.5 * font_h.
        """

        hidden_h = self.ids.chatlog.height - self.ids.chatlog_view.height
        font_h = self.ids.chatlog.font_size
        near_the_bottom = (self.ids.chatlog_view.scroll_y * hidden_h < 3.0 * font_h)
        if near_the_bottom:
            self.ids.chatlog_view.scroll_y = 0


    def send_chat_message(self):
        """
        Отправляет сообщение в чат.
        """

        text = self.ids.input_field.text
        self.ids.input_field.text = ""
        if text:
            self.app.send_chat_message(text)


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
