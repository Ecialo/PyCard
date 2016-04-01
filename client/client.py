# -*- coding: utf-8 -*-
""" Test client """

from uuid import getnode as get_mac
import io, sys
import json

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.support import install_twisted_reactor
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

install_twisted_reactor()

from twisted.internet import reactor, protocol
from twisted.logger import Logger, jsonFileLogObserver

import core.predef as predef


log = Logger(observer=jsonFileLogObserver(io.open("client.json", "a")),
                 namespace="client")

__author__ = 'Anton Korobkov'


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        log.info('Message recieved {message}', message=data)
        self.factory.app.parse_message(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        log.debug('Connection {connection} lost because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.print_message("Connection lost!")

    def clientConnectionFailed(self, conn, reason):
        log.debug('Failed to connect to {connection} because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.print_message("Connection failed!")


Builder.load_file('./client.kv')

# пустые экраны, разметка для которых содержится в client.kv
class LobbyScreen(Screen):
    pass
class GameScreen(Screen):
    pass


class TwistedClientApp(App):
    connection = None
    player_name, macaddr = None, get_mac()

    users = []

    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LobbyScreen(name='lobby'))
        sm.add_widget(GameScreen(name='game'))

        self.lobby_scr = sm.get_screen('lobby')
        self.game_scr = sm.get_screen('game')

        self.lobby_scr.ids.ready_checkbox.bind(state=self.on_ready_clicked)

        return sm

    def on_start(self):
        """
        Вызывается автоматически после создания интерфейса.
        """
        self.stdout_hook = StdoutHook(self.lobby_scr.ids.chatlog)
        Factory.ConnectionWidget().open()

    def connect_to_server(self, host, port):
        if self.player_name and host and port:
            reactor.connectTCP(host, port, EchoFactory(self))
            log.info('Connecting to server {server} on port {port}',
                server=host, port=port)
        
        else:
            self.print_message("One or more fields are empty.") # TODO: make a proper error message
            Factory.ConnectionWidget().open()

    def on_connection(self, connection):
        """
        Вызывается автоматически при успешном подключении к серверу.
        """

        self.print_message("Connected succesfully!")
        self.connection = connection
        self.send_chat_register()

        self.users.append(self.player_name)

    def print_message(self, msg):
        """
        Выводит текст в чат.
        """

        self.lobby_scr.ids.chatlog.text += msg + "\n"
        self.scroll_if_necessary()
        self.lobby_scr.ids.input_field.focus = True

    def scroll_if_necessary(self):
        """
        Прокручивает чат, если в нижней части скрыто более 2 строк текста.
        Судя по наблюдениям за интерфейсом, каждая строка имеет высоту 1.5 * font_h.
        """

        hidden_h = self.lobby_scr.ids.chatlog.height - self.lobby_scr.ids.chatlog_view.height
        font_h = self.lobby_scr.ids.chatlog.font_size
        near_the_bottom = (self.lobby_scr.ids.chatlog_view.scroll_y * hidden_h < 3.0 * font_h)
        if near_the_bottom:
            self.lobby_scr.ids.chatlog_view.scroll_y = 0


    # Обработка сообщений сервера

    def parse_message(self, msg):
        """
        В зависимости от типа сообщения, пришедшего от сервера, вызывает один из обработчиков.
        """

        ev = json.loads(msg)
        ev_type, params = ev[predef.MESSAGE_TYPE_KEY], ev[predef.MESSAGE_PARAMS_KEY]

        if ev_type == predef.CHAT_JOIN:
            self.handle_chat_join(params)

        elif ev_type == predef.CHAT_PART:
            self.handle_chat_part(params)

        elif ev_type == predef.CHAT_MESSAGE:
            self.handle_chat_message(params)

        elif ev_type == predef.LOBBY_ALL_READY:
        	self.handle_lobby_all_ready(params)
        	
        else:
            pass # TODO: add handlers for all events

    def handle_chat_join(self, params):
        """
        Обработчик для появления на сервере нового игрока.
        """

        name = params[predef.CHAT_NAME_KEY]
        self.print_message("%s has joined" % name)

        self.users.append(name)

    def handle_chat_part(self, params):
        """
        Обработчик для ухода игрока с сервера.
        """

        name = params[predef.CHAT_NAME_KEY]
        self.print_message("%s has left" % name)

        for i, u in enumerate(self.users):
            if u == name:
                self.users.pop(i)
                break

    def handle_chat_message(self, params):
        """
        Обработчик для приходящих сообщений чата.
        """

        author = params[predef.CHAT_AUTHOR_KEY]
        msg_type, text = params[predef.CHAT_MESSAGE_TYPE_KEY], params[predef.CHAT_TEXT_KEY]
        self.print_message("<%s> %s" % (author, text))

    def handle_lobby_all_ready(self, params):
    	"""
    	Обработчик для сообщения «все готовы, пора играть».
    	"""

    	self.root.current = 'game'


    # Генерация сообщений для сервера

    def send_message(self, msg):
        """
        Отправляет сообщение на сервер.
        Сообщение должно иметь формат, указанный в описании протокола, и являться словарём.
        """

        if msg and self.connection:
            self.connection.write(str(json.dumps(msg)))

    def send_chat_register(self):
        """
        Уведомляет сервер о заходе в лобби.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.CHAT_REGISTER,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_NAME_KEY: self.player_name,
                predef.CHAT_MAC_KEY: self.macaddr
            }
        }
        self.send_message(msg)

    def send_chat_message(self):
        """
        Отправляет сообщение в чат.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.CHAT_MESSAGE,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_AUTHOR_KEY: self.player_name,
                predef.CHAT_MESSAGE_TYPE_KEY: predef.CHAT_MESSAGE_BROADCAST, # TODO: implement private messages
                predef.CHAT_TEXT_KEY: self.lobby_scr.ids.input_field.text,
            }
        }
        self.lobby_scr.ids.input_field.text = ""
        self.send_message(msg)

    def send_lobby_ready(self):
        """
        Отправляет сигнал о готовности к началу игры.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.LOBBY_READY,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_MAC_KEY: self.macaddr
            }
        }
        self.send_message(msg)

    def send_lobby_not_ready(self):
        """
        Отправляет сигнал об отмене готовности к началу игры.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.LOBBY_NOT_READY,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_MAC_KEY: self.macaddr
            }
        }
        self.send_message(msg)


    # Обработка событий с виджетов

    def on_ready_clicked(self, checkbox, state):
        if state == 'down':
            self.send_lobby_ready()
        else:
            self.send_lobby_not_ready()


class StdoutHook():
    """
    Дублирует stdout в окно чата.
    """

    def __init__(self, chat):
        self.ex_stdout = sys.stdout # in case there's already a hook installed by someone
        sys.stdout = self
        self.chat = chat

    def write(self, s):
        s = s.strip()
        if s:
            self.ex_stdout.write(s)
            self.chat.text += 'STDOUT> ' + s + '\n'


if __name__ == '__main__':
    TwistedClientApp().run()
