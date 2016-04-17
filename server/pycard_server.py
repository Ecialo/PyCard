# -*- coding: utf-8 -*-
"""
Попытка запилить асинхронный сервер, который общается с клиентами
с помощью текстовых сообщений
"""

import io
import json
from twisted.internet import (
    reactor,
    defer,
)
from twisted.internet import (
    protocol,
    task
)
from twisted.logger import (
    Logger,
    jsonFileLogObserver,
)
from core.predef import (
    CHAT_REGISTER,
    CHAT_MESSAGE,
    LOBBY_READY,
    LOBBY_NOT_READY,
    MESSAGE_PARAMS_KEY,
    LOBBY_START_GAME,
    CHAT_NAMES_KEY,
    CHAT_JOIN,
    CHAT_PART,
    CHAT_MESSAGE_BROADCAST,
    MESSAGE_TYPE_KEY,
    CHAT_MESSAGE_TYPE_KEY,
    CHAT_TEXT_KEY,
    LOBBY_ALL_READY,
    ACTION_JUST,
    ACTION_PIPE,
    ACTION_SEQUENCE,
    CHAT_NAME_KEY,

)

from player.player_class import LobbyPerson
from sample_games.retard_game import retard_game

__author__ = 'Anton Korobkov'

log = Logger(
    observer=jsonFileLogObserver(io.open("server.json", "a")),
    namespace="server"
)


class MultiEcho(protocol.Protocol):

    def __init__(self, *args):
        self.factory = args[0]
        self.playernum = args[1]
        self.anncounter = args[2]

    # Twisted методы

    def connectionMade(self):
        log.info('Incoming connection on {host}', host=self)

    def dataReceived(self, data):
        log.info('Data obtained {data}', data=data)
        self.parse_incoming_message(data)

    def connectionLost(self, reason):
        log.debug('Connection {conn} is lost because of {lost_reason}',
                  conn=self, lost_reason=reason)

        self.handle_chat_disconnection()

    # Вспомогательные методы

    def send_global_message(self, msg):
        """
        Юзать этот метод когда нужно что-то одинаковое написать всем клиентам
        """

        for player in self.factory.echoers:
            player.transport.write(msg)

    def check_playnum(self):
        """
        Проверяем достаточно ли клиентов (вызываем каждый раз после того как
        произошло нажатие ready); если достаточно - запускаем игровую сессию
        Надо этот метод переписать, т.к. быдлокод
        """
        # TODO: это можно наверное получше сделать
        counter = 0

        for client in self.factory.players:
            if self.factory.players[client].ready is True:
                counter += 1

        if counter == self.playernum:
            self.prepare_session()

    def warning(self):
        """
        Оповещает всех о скором запуске
        """
        # TODO: перенести заранее сгенерированные сообщения куда-то
        # и сделать так чтобы снятие флага "ready" отменяло запуск

        msg = {
            MESSAGE_TYPE_KEY: CHAT_MESSAGE,
            MESSAGE_PARAMS_KEY: {
                CHAT_NAME_KEY: 'Server message',
                CHAT_MESSAGE_TYPE_KEY: CHAT_MESSAGE_BROADCAST,
                CHAT_TEXT_KEY: ' '.join(['game is going to start in', str(5 - self.anncounter), 'seconds'])
            }
        }

        log.info('starting the {game}', game=self)

        self.send_global_message(json.dumps(msg))
        self.anncounter += 1
        # Через 5 секунд сообщаем о запуске игры
        if self.anncounter == 5:
            self.run_warning.stop()

    def launch_game(self):
        """
        Запустить игру
        """
        msg = {
            MESSAGE_TYPE_KEY: LOBBY_START_GAME,
            MESSAGE_PARAMS_KEY: {}
        }
        self.send_global_message(json.dumps(msg))
        self.game = retard_game.RetardGame([x.name for x in self.factory.players.values()])
        log.info('this is our game: {game}', game=self.game)

    def dummy_sender(self):
        pass

    def prepare_session(self):
        """ Подготовить сессию игровую к запуску. Если кто-то
         из клиентов в течении n секунд отожмет чекбокс "готов" -
         сессию не запускать
        """

        self.run_game_launcher = reactor.callLater(5, self.launch_game)
        self.run_warning = task.LoopingCall(self.warning)
        self.run_warning.start(1)

    # Обработка сообщений клиента

    def parse_incoming_message(self, msg):
        """
        Родной брат метода client.parse_message
        """

        event = json.loads(msg)
        event_type, params = event[MESSAGE_TYPE_KEY], event[MESSAGE_PARAMS_KEY]

        # Не будем лепить костылей по отсылке приватных сообщений до тех пор пока это не будет
        # запилено на стороне клиента

        log.info('{signal} caught', signal=msg)

        if event_type == CHAT_REGISTER:
            self.handle_chat_join(event)
        elif event_type == CHAT_MESSAGE:
            self.handle_chat_message(event)
        elif event_type == LOBBY_READY:
            self.handle_lobby_ready(event)
        elif event_type == LOBBY_NOT_READY:
            self.handle_lobby_not_ready(event)
        elif event_type in [ACTION_JUST, ACTION_PIPE, ACTION_SEQUENCE]:
            self.game.receive_message(event)


    # Отправка сообщений клиентам

    def handle_chat_join(self, params):
        """
        Посылаем всем клиентам сообщения о том кто зашел и сохраняем адрес и ник
        """

        self.factory.players[self] = LobbyPerson(params[MESSAGE_PARAMS_KEY][CHAT_NAME_KEY])
        self.factory.echoers.append(self)

        params[MESSAGE_TYPE_KEY] = CHAT_JOIN
        # TODO: fix later
        params[MESSAGE_PARAMS_KEY][CHAT_NAMES_KEY] = json.dumps([player.name for player in self.factory.players.values()])
        h = open('hi.txt', 'a')
        h.write(json.dumps(params))

        log.info('some {data} sent', data=str(params))
        self.send_global_message(json.dumps(params))

    def handle_chat_disconnection(self):
        """
        Говорим всем о том кто ушел
        """

        # TODO: понять почему это работает, сделать нормально
        parted = self.factory.players.pop(self, 'not found')

        part_message = {MESSAGE_TYPE_KEY: CHAT_PART,
                        MESSAGE_PARAMS_KEY: {
                            CHAT_NAME_KEY: getattr(parted, 'name')
                        }
                        }

        log.info('some {data} sent', data=str(part_message))
        self.send_global_message(json.dumps(part_message))

    def handle_lobby_ready(self, params):
        """ Вызывать если клиент жмет чекбокс "ready" """

        self.factory.players[self].get_ready()
        log.info('This {player} now is ready: ', player=str(params[MESSAGE_PARAMS_KEY][CHAT_NAME_KEY]))
        self.check_playnum()

    def handle_lobby_not_ready(self, params):
        """ Вызывать если клиент отжимает чекбокс "ready" """

        self.factory.players[self].get_unready()
        h = open('hi.txt', 'w')
        h.write('ureadied')

        if self.run_game_launcher:
            # Кина не будет, все вырубаем
            self.run_game_launcher.cancel()
            self.run_warning.stop()
            self.anncounter = 0

        log.info('This {player} now is not ready: ', player=str(params[MESSAGE_PARAMS_KEY][CHAT_NAME_KEY]))

    def handle_chat_message(self, params):
        """
        Просто отсылаем всем то, что нам пришло
        """
        self.send_global_message(json.dumps(params))

    # Здесь будет все что имеет отношение уже к сессии


class MultiEchoFactory(protocol.Factory):

    def __init__(self, playnum):
        self.echoers = []
        self.player_num = playnum
        self.players = {}
        self.announcment_counter = 0
        log.info('Instantiated server for {playernum} players', playernum=self.player_num)

    def buildProtocol(self, addr):
        return MultiEcho(self, self.player_num, self.announcment_counter)


if __name__ == '__main__':
    reactor.listenTCP(8000, MultiEchoFactory(2))
    reactor.run()
