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
from twisted.internet import protocol
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
    CHAT_PLAYER_ID_KEY,
    CHAT_NAME_KEY,
    CHAT_JOIN,
    CHAT_PART,
    CHAT_MESSAGE_BROADCAST,
    MESSAGE_TYPE_KEY,
    CHAT_AUTHOR_KEY,
    CHAT_MESSAGE_TYPE_KEY,
    CHAT_TEXT_KEY
)

from player.player_class import LobbyPerson

__author__ = 'Anton Korobkov'

log = Logger(
    observer=jsonFileLogObserver(io.open("server.json", "a")),
    namespace="server"
)


class MultiEcho(protocol.Protocol):

    def __init__(self, factory, playernum):
        self.factory = factory
        self.playernum = playernum

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
            msg = {
                MESSAGE_TYPE_KEY: CHAT_MESSAGE,
                MESSAGE_PARAMS_KEY: {
                    CHAT_AUTHOR_KEY: u'Server message',
                    CHAT_MESSAGE_TYPE_KEY: CHAT_MESSAGE_BROADCAST,
                    CHAT_TEXT_KEY: u'game is about to start!',
                }
            }

            log.info('starting the {game}', game=self)

            self.send_global_message(json.dumps(msg))

    # Обработка сообщений клиента

    def parse_incoming_message(self, msg):
        """
        Родной брат метода client.parse_message
        """

        event = json.loads(msg)
        test = open('hi.txt', 'a')
        test.write(str(event) + '\n')
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

    # Отправка сообщений клиентам

    def handle_chat_join(self, params):
        """
        Посылаем всем клиентам сообщения о том кто зашел и сохраняем адрес и ник
        """

        self.factory.players[self] = LobbyPerson(params[MESSAGE_PARAMS_KEY][CHAT_PLAYER_ID_KEY],
                                                 params[MESSAGE_PARAMS_KEY][CHAT_NAME_KEY])

        params[MESSAGE_TYPE_KEY] = CHAT_JOIN

        log.info('some {data} sent', data=str(params))
        self.send_global_message(json.dumps(params))
        self.factory.echoers.append(self)

    def handle_chat_disconnection(self):
        """
        Говорим всем о том кто ушел
        """

        # TODO: понять почему это работает, сделать нормально
        parted = self.factory.players.pop(self, 'not found')

        part_message = {MESSAGE_TYPE_KEY: CHAT_PART,
                        MESSAGE_PARAMS_KEY: {
                            CHAT_NAME_KEY: getattr(parted, 'name'),
                            CHAT_PLAYER_ID_KEY: getattr(parted, 'identifier')
                        }
                        }

        log.info('some {data} sent', data=str(part_message))
        self.send_global_message(json.dumps(part_message))

    def handle_lobby_ready(self, params):
        """ Вызывать если клиент жмет чекбокс "ready" """

        self.factory.players[self].get_ready()
        log.info('This {player} now is ready: ', player=str(params[MESSAGE_PARAMS_KEY][CHAT_PLAYER_ID_KEY]))
        self.check_playnum()

    def handle_lobby_not_ready(self, params):
        """ Вызывать если клиент отжимает чекбокс "ready" """

        self.factory.players[self].get_unready()
        log.info('This {player} now is not ready: ', player=str(params[MESSAGE_PARAMS_KEY][CHAT_PLAYER_ID_KEY]))

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
        log.info('Instantiated server for {playernum} players', playernum=self.player_num)

    def buildProtocol(self, addr):
        return MultiEcho(self, self.player_num)


if __name__ == '__main__':
    reactor.listenTCP(8000, MultiEchoFactory(2))
    reactor.run()
