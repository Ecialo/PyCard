# -*- coding: utf-8 -*-
"""
PyCard client application
"""

from os import getpid
import io, sys
import json

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol
from twisted.logger import Logger, jsonFileLogObserver

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from notifications.notifications import NotificationsManager
from client_ui.connection_screen import ConnectionScreen
from client_ui.lobby_screen import LobbyScreen

import core.predef as predef
from core.predef import pycard_protocol as pp
from sample_games.retard_game import retard_game


log = Logger(
    observer=jsonFileLogObserver(io.open("client_{pid}.json".format(pid=getpid()), "a")),
    namespace="client"
)

__author__ = 'Anton Korobkov'


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        messages = data.split('\n')
        for m in messages:
            if m:
                log.info('Message from server: {message}', message=m)
                self.factory.app.parse_message(m)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        log.debug('Connection {connection} lost because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.screen_mgr.get_screen('lobby').print_message("Connection lost!")

    def clientConnectionFailed(self, conn, reason):
        log.debug('Failed to connect to {connection} because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.notify("Connection failed!")
        self.app.screen_mgr.current = 'connection'


class TwistedClientApp(App):
    connection = None
    player_name = None

    users = []
    ready = False
    msg_handlers = {}


    def set_message_handlers(self):
        self.msg_handlers = {
            pp.event_types.CHAT_JOIN:                   self.handle_chat_join,
            pp.event_types.CHAT_PART:                   self.handle_chat_part,
            pp.event_types.CHAT_MESSAGE:                self.handle_chat_message,
            pp.event_types.LOBBY_START_GAME:            self.handle_lobby_start_game,
            pp.event_types.LOBBY_NAME_ALREADY_EXISTS:   self.handle_lobby_name_already_exists
        }

    def build(self):
        self.set_message_handlers()

        root = FloatLayout()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ConnectionScreen(app=self, name='connection'))
        sm.add_widget(LobbyScreen(app=self, name='lobby'))
        root.add_widget(sm)

        nm = NotificationsManager()
        root.add_widget(nm)

        self.screen_mgr = sm
        self.notifications_mgr = nm
        return root

    def on_start(self):
        """
        Вызывается автоматически после создания интерфейса.
        """

        self.stdout_hook = StdoutHook(self.screen_mgr.get_screen('lobby').ids.chatlog)

    def connect_to_server(self, host, port):
        self.screen_mgr.current = 'lobby'
        reactor.connectTCP(host, port, EchoFactory(self))
        log.info('Connecting to server {server} on port {port}',
            server=host, port=port)

    def on_connection(self, connection):
        """
        Вызывается автоматически при успешном подключении к серверу.
        """

        self.screen_mgr.get_screen('lobby').print_message("Connected succesfully!")
        log.info("Connected!")
        self.connection = connection
        self.send_chat_register()


    # Обработка сообщений сервера

    def parse_message(self, msg):
        """
        В зависимости от типа сообщения, пришедшего от сервера, вызывает один из обработчиков.
        """

        ev = json.loads(msg)
        ev_type, params = ev[pp.message_struct.TYPE_KEY], ev[pp.message_struct.PARAMS_KEY]

        if ev_type in self.msg_handlers:
            log.info("Calling handler for message of type {h}", h=ev_type)
            self.msg_handlers[ev_type](params)

        elif ev_type in [pp.event_types.ACTION_JUST, \
                         pp.event_types.ACTION_SEQUENCE, \
                         pp.event_types.ACTION_PIPE]:
            log.info("Trying to move game forward")
            self.handle_game_action(msg)

        else:
            log.debug("Unknown event type: {evt}", evt=ev_type)

    def handle_chat_join(self, params):
        """
        Обработчик для появления на сервере нового игрока.
        """

        users = params[pp.chat.NAMES_KEY]
        log.info("Online changed: {users}", users=users)
        self.users = users

    def handle_chat_part(self, params):
        """
        Обработчик для ухода игрока с сервера.
        """

        name = params[pp.chat.NAME_KEY]
        log.info("Someone has left: {user}", user=name)
        self.screen_mgr.get_screen('lobby').print_message("{user} has left".format(user=name))

        for i, u in enumerate(self.users):
            if u == name:
                self.users.pop(i)
                break

    def handle_chat_message(self, params):
        """
        Обработчик для приходящих сообщений чата.
        """

        name = params[pp.chat.NAME_KEY]
        msg_type, text = params[pp.chat.MESSAGE_TYPE_KEY], params[pp.chat.TEXT_KEY].encode('utf-8')
        log.info("Received message {m} from user {u}, type {t}", m=msg_type, u=name, t=msg_type)
        self.screen_mgr.get_screen('lobby').print_message("<{name}> {msg}".format(name=name, msg=text))

    def handle_lobby_start_game(self, params):
        """
        Обработчик для сообщения «все готовы, пора играть».
        """

        rg = retard_game.RetardGame(
                [{'name': user} for user in self.users],
                mode=predef.CLIENT)

        log.info("Starting game, players are: {pl}", pl=self.users)
        rgw = rg.make_widget(name='game', app=self)
        self.screen_mgr.add_widget(rgw)
        self.game_scr = self.screen_mgr.get_screen('game')

        self.screen_mgr.current = 'game'

    def handle_lobby_name_already_exists(self, params):
        """
        Когда игрок с таким именем уже есть на сервере.
        """

        log.debug("Name {n} already exists on server", n=self.player_name)
        self.connection.loseConnection()
        self.notify('Name {n} is already taken, please pick another one.'.format(n=self.player_name))
        self.screen_mgr.current = 'connection'

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
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_REGISTER,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: self.player_name,
            }
        }

        self.send_message(msg)

    def send_chat_message(self, text):
        """
        Отправляет сообщение в чат.
        """

        msg = {
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_MESSAGE,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: self.player_name,
                pp.chat.MESSAGE_TYPE_KEY: pp.chat.message_type.BROADCAST, # TODO: implement private messages
                pp.chat.TEXT_KEY: text,
            }
        }

        self.send_message(msg)

    def send_lobby_ready(self):
        """
        Отправляет сигнал о готовности к началу игры.
        """

        msg = {
            pp.message_struct.TYPE_KEY: pp.event_types.LOBBY_READY,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: self.player_name
            }
        }

        self.send_message(msg)

    def send_lobby_not_ready(self):
        """
        Отправляет сигнал об отмене готовности к началу игры.
        """

        msg = {
            pp.message_struct.TYPE_KEY: pp.event_types.LOBBY_NOT_READY,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: self.player_name
            }
        }

        self.send_message(msg)



    # Обработка событий с виджетов

    def notify(self, text):
        """
        Показывает уведомление вверху экрана.
        """

        self.notifications_mgr.notify(text)


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
