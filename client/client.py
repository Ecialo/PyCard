# -*- coding: utf-8 -*-
""" Test client """

from os import getpid
import io, sys
import json

from kivy.app import App
from kivy.lang import Builder
from kivy.support import install_twisted_reactor
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout

from notifications.notifications import NotificationsManager
from client_ui.connection_screen import ConnectionScreen
from client_ui.lobby_screen import LobbyScreen

install_twisted_reactor()

from twisted.internet import reactor, protocol
from twisted.logger import Logger, jsonFileLogObserver

import core.predef as predef

from game_ui.game_widget import game_widget as gw
from sample_games.retard_game import retard_game


log = Logger(observer=jsonFileLogObserver(io.open("client_{pid}.json".format(pid=getpid()), "a")),
                 namespace="client")

__author__ = 'Anton Korobkov'


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        log.info('Message from server: {message}', message=data)
        self.factory.app.parse_message(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        log.debug('Connection {connection} lost because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.sm.get_screen('lobby').print_message("Connection lost!")

    def clientConnectionFailed(self, conn, reason):
        log.debug('Failed to connect to {connection} because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.notify("Connection failed!")
        self.app.sm.current = 'connection'


class TwistedClientApp(App):
    connection = None
    player_name = None

    users = []
    ready = False
    msg_handlers = {}


    def set_message_handlers(self):
        self.msg_handlers = {
            predef.CHAT_JOIN:                   self.handle_chat_join,
            predef.CHAT_PART:                   self.handle_chat_part,
            predef.CHAT_MESSAGE:                self.handle_chat_message,
            predef.LOBBY_START_GAME:            self.handle_lobby_start_game,
            predef.LOBBY_NAME_ALREADY_EXISTS:   self.handle_lobby_name_already_exists
        }

    def build(self):
        self.set_message_handlers()

        root = FloatLayout()

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ConnectionScreen(app=self, name='connection'))
        sm.add_widget(LobbyScreen(app=self, name='lobby'))

        self.lobby_scr = sm.get_screen('lobby')


        root.add_widget(sm)

        nm = NotificationsManager()
        root.add_widget(nm)

        self.sm = sm
        self.nm = nm
        return root

    def on_start(self):
        """
        Вызывается автоматически после создания интерфейса.
        """

        self.stdout_hook = StdoutHook(self.sm.get_screen('lobby').ids.chatlog)

    def connect_to_server(self, host, port):
        self.sm.current = 'lobby'
        reactor.connectTCP(host, port, EchoFactory(self))
        log.info('Connecting to server {server} on port {port}',
            server=host, port=port)

    def on_connection(self, connection):
        """
        Вызывается автоматически при успешном подключении к серверу.
        """

        self.sm.get_screen('lobby').print_message("Connected succesfully!")
        log.info("Connected!")
        self.connection = connection
        self.send_chat_register()


    # Обработка сообщений сервера

    def parse_message(self, msg):
        """
        В зависимости от типа сообщения, пришедшего от сервера, вызывает один из обработчиков.
        """

        ev = json.loads(msg)
        ev_type, params = ev[predef.MESSAGE_TYPE_KEY], ev[predef.MESSAGE_PARAMS_KEY]

        if ev_type in self.msg_handlers:
            log.info("Calling handler for message of type {h}", h=ev_type)
            self.msg_handlers[ev_type](params)

        elif ev_type in [predef.ACTION_JUST, predef.ACTION_SEQUENCE, predef.ACTION_PIPE]:
            log.info("Trying to move game forward")
            self.handle_game_action(msg)

        else:
            log.debug("Unknown event type: {evt}", evt=ev_type)

    def handle_chat_join(self, params):
        """
        Обработчик для появления на сервере нового игрока.
        """

        users = params[predef.CHAT_NAMES_KEY]
        log.info("Online changed: {users}", users=users)
        self.users = users

    def handle_chat_part(self, params):
        """
        Обработчик для ухода игрока с сервера.
        """

        name = params[predef.CHAT_NAME_KEY]
        log.info("Someone has left: {user}", user=name)
        self.sm.get_screen('lobby').print_message("%s has left" % name)

        for i, u in enumerate(self.users):
            if u == name:
                self.users.pop(i)
                break

    def handle_chat_message(self, params):
        """
        Обработчик для приходящих сообщений чата.
        """

        name = params[predef.CHAT_NAME_KEY]
        msg_type, text = params[predef.CHAT_MESSAGE_TYPE_KEY], params[predef.CHAT_TEXT_KEY]
        log.info("Received message {m} from user {u}, type {t}", m=msg_type, u=name, t=msg_type)
        self.sm.get_screen('lobby').print_message("<{name}> {msg}".format(name=name, msg=text))

    def handle_lobby_start_game(self, params):
        """
        Обработчик для сообщения «все готовы, пора играть».
        """

        rg = retard_game.RetardGame(
                [{'name': user} for user in self.users],
                mode=predef.CLIENT)

        log.info("Starting game, players are: {pl}", pl=self.users)
        rgw = rg.make_widget(name='game', app=self)
        self.sm.add_widget(rgw)
        self.game_scr = self.sm.get_screen('game')

        self.sm.current = 'game'

    def handle_lobby_name_already_exists(self, params):
        """
        Когда игрок с таким именем уже есть на сервере.
        """

        log.debug("Name {n} already exists on server", n=self.player_name)
        self.connection.loseConnection()

        self.notify('Name {n} is already taken, please pick another one.'.format(n=self.player_name))
        self.sm.current = 'connection'

    def handle_game_action(self, action_msg):
        """
        Обработка игровых событий (простая передача их по цепочке).
        """

        self.game_scr.game.receive_message(action_msg)


    # Генерация сообщений для сервера

    def send_raw_message(self, raw_msg):
        log.info("Sending message: {m}", m=raw_msg)
        if raw_msg and self.connection:
            self.connection.write(raw_msg)

    def send_action(self, action_msg):
        self.send_raw_message(action_msg)

    def send_message(self, msg):
        """
        Отправляет сообщение на сервер.
        Сообщение должно иметь формат, указанный в описании протокола, и являться словарём.
        """

        dump = json.dumps(msg)
        self.send_raw_message(dump)

    def send_chat_register(self):
        """
        Уведомляет сервер о заходе в лобби.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.CHAT_REGISTER,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_NAME_KEY: self.player_name,
            }
        }

        self.send_message(msg)

    def send_chat_message(self, text):
        """
        Отправляет сообщение в чат.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.CHAT_MESSAGE,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_NAME_KEY: self.player_name,
                predef.CHAT_MESSAGE_TYPE_KEY: predef.CHAT_MESSAGE_BROADCAST, # TODO: implement private messages
                predef.CHAT_TEXT_KEY: text,
            }
        }

        self.send_message(msg)

    def send_lobby_ready(self):
        """
        Отправляет сигнал о готовности к началу игры.
        """

        msg = {
            predef.MESSAGE_TYPE_KEY: predef.LOBBY_READY,
            predef.MESSAGE_PARAMS_KEY: {
                predef.CHAT_NAME_KEY: self.player_name
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
                predef.CHAT_NAME_KEY: self.player_name
            }
        }

        self.send_message(msg)



    # Обработка событий с виджетов

    def notify(self, text):
        """
        Показывает уведомление вверху экрана.
        """

        self.nm.notify(text)


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
