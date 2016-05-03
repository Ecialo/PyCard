# -*- coding: utf-8 -*-
"""
PyCard client application
"""

import io, sys
import json

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol
from twisted.logger import Logger, jsonFileLogObserver

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from notifications.notifications import NotificationsManager
from client_ui.connection_screen import ConnectionScreen
from client_ui.lobby_screen import LobbyScreen
from client_ui.chat_widget import ChatWidget

import core.predef as predef
from core.predef import pycard_protocol as pp
from sample_games.retard_game import retard_game


log = Logger(
    observer=jsonFileLogObserver(io.open("client.json", "a")),
    namespace="client"
)

__author__ = 'Anton Korobkov'


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        messages = data.split(pp.message_delimiter)
        for m in messages:
            if m:
                self.factory.app.parse_message(m)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        log.error('Connection {connection} lost because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.chat.print_message("Connection lost!")

    def clientConnectionFailed(self, conn, reason):
        log.error('Failed to connect to {connection} because of {fail_reason}',
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
            pp.event_types.LOBBY_NAME_ALREADY_EXISTS:   self.handle_lobby_name_already_exists,
            pp.event_types.LOBBY_GAME_OVER:             self.handle_lobby_game_over,
        }

    def build(self):
        self.set_message_handlers()

        root = Builder.load_file('./client/client_ui/client.kv')

        nm = NotificationsManager()
        root.ids.notifications_container.add_widget(nm)

        cw = ChatWidget(app=self)
        root.ids.chat_container.add_widget(cw)

        sm = root.ids.screen_mgr
        sm.transition = FadeTransition()

        sm.add_widget(ConnectionScreen(app=self, name='connection'))
        sm.add_widget(LobbyScreen(app=self, name='lobby'))

        self.screen_mgr = sm
        self.notifications_mgr = nm
        self.chat = cw

        root.ids.chat_button.bind(on_press=self.toggle_chat)
        return root

    def on_start(self):
        """
        Вызывается автоматически после создания интерфейса.
        """

        self.stdout_hook = StdoutHook(self.chat.ids.chatlog)

    def connect_to_server(self, host, port):
        self.screen_mgr.current = 'lobby'
        reactor.connectTCP(host, port, EchoFactory(self))
        log.info('Connecting to server {server} on port {port}',
            server=host, port=port, player_name=self.player_name)

    def on_connection(self, connection):
        """
        Вызывается автоматически при успешном подключении к серверу.
        """

        self.chat.print_message("Connected succesfully!")
        log.info("Connected!", player_name=self.player_name)
        self.connection = connection
        self.send_chat_register()


    # Обработка сообщений сервера

    def parse_message(self, msg):
        """
        В зависимости от типа сообщения, пришедшего от сервера, вызывает один из обработчиков.
        """

        log.debug('Message from server: {message}', message=msg)
        ev = json.loads(msg)
        ev_type, params = ev[pp.message_struct.TYPE_KEY], ev[pp.message_struct.PARAMS_KEY]

        if ev_type in self.msg_handlers:
            log.debug("Calling handler for message of type {h}", h=ev_type, player_name=self.player_name)
            self.msg_handlers[ev_type](params)

        elif ev_type in [pp.event_types.ACTION_JUST, \
                         pp.event_types.ACTION_SEQUENCE, \
                         pp.event_types.ACTION_PIPE]:
            log.debug("Trying to move game forward", player_name=self.player_name)
            self.handle_game_action(msg)

        else:
            log.warn("Unknown event type: {evt}", evt=ev_type, player_name=self.player_name)

    def handle_chat_join(self, params):
        """
        Обработчик для появления на сервере нового игрока.
        """

        users = params[pp.chat.NAMES_KEY]
        log.debug("Online changed: {users}", users=users, player_name=self.player_name)
        self.users = users

    def handle_chat_part(self, params):
        """
        Обработчик для ухода игрока с сервера.
        """

        name = params[pp.chat.NAME_KEY]
        log.debug("Someone has left: {user}", user=name, player_name=self.player_name)
        self.chat.print_message("{user} has left".format(user=name))

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
        log.debug("Received message {m} from user {u}, type {t}", m=msg_type, u=name, t=msg_type, player_name=self.player_name)
        self.chat.print_message("<{name}> {msg}".format(name=name, msg=text))

    def handle_lobby_start_game(self, params):
        """
        Обработчик для сообщения «все готовы, пора играть».
        """

        rg = retard_game.RetardGame(
                [{'name': user} for user in self.users],
                mode=predef.CLIENT)

        log.info("The game has started, players are: {pl}", pl=self.users, player_name=self.player_name)
        rgw = rg.make_widget(name='game', app=self)
        self.screen_mgr.add_widget(rgw)
        self.game_scr = self.screen_mgr.get_screen('game')

        self.chat.print_message('The game has started!')
        self.chat.fold()
        self.screen_mgr.current = 'game'

    def handle_lobby_name_already_exists(self, params):
        """
        Когда игрок с таким именем уже есть на сервере.
        """

        log.error("Name {n} already exists on server", n=self.player_name, player_name=self.player_name)
        self.connection.loseConnection()
        self.notify('Name {n} is already taken, please pick another one.'.format(n=self.player_name))
        self.screen_mgr.current = 'connection'

    def handle_lobby_game_over(self, params):
        """
        Обработчик для сообщения о конце игры.
        """

        self.screen_mgr.remove_widget(self.screen_mgr.get_screen('game'))
        data = params[pp.lobby.GAME_RESULT_KEY]

        self.screen_mgr.current = 'lobby'

        column_width = 20
        line_template = '| {:<{cw}} | {:<{cw}} |'

        self.chat.print_message('* Game is over!')
        self.chat.print_message(line_template.format('Place', 'Name', cw=column_width))
        self.chat.print_message('-' * (2 * column_width + 7))

        for entry in sorted(data.items(), key=lambda x: x[1]):
            self.chat.print_message(line_template.format(entry[1][0], entry[0], cw=column_width))

    def handle_game_action(self, action_msg):
        """
        Обработка игровых событий (простая передача их по цепочке).
        """

        self.game_scr.push_game_forward(action_msg)


    # Генерация сообщений для сервера

    def send_raw_message(self, raw_msg):
        log.debug("Sending message: {m}", m=raw_msg, player_name=self.player_name)
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

    def toggle_chat(self, button):
        self.chat.toggle()


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
    log.info('Start client')
    TwistedClientApp().run()
