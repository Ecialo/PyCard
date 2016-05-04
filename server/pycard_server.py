# -*- coding: utf-8 -*-
"""
Попытка запилить асинхронный сервер, который общается с клиентами
с помощью текстовых сообщений
"""

import io
import json
from zope.interface import implements
from twisted.internet import (
    reactor,
    defer,
    interfaces
)
from twisted.internet import (
    protocol,
    task
)
from twisted.logger import (
    Logger,
    jsonFileLogObserver,
)
from core.predef import (pycard_protocol as pp,
    table_type as tt
)
from player.player_class import LobbyPerson
from sample_games.retard_game import retard_game
from core.game import GameOver

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
            self.factory.instantiate_game()
            self.prepare_session()

    def warning(self):
        """
        Оповещает всех о скором запуске
        """
        # TODO: перенести заранее сгенерированные сообщения куда-то
        # и сделать так чтобы снятие флага "ready" отменяло запуск

        msg = {
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_MESSAGE,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: 'Server message',
                pp.chat.MESSAGE_TYPE_KEY: pp.chat.message_type.BROADCAST,
                pp.chat.TEXT_KEY: ' '.join(['game is going to start in', str(5 - self.anncounter), 'seconds'])
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
            pp.message_struct.TYPE_KEY: pp.event_types.LOBBY_START_GAME,
            pp.message_struct.PARAMS_KEY: {}
        }
        self.send_global_message(json.dumps(msg))
        log.info('this is our game: {game}', game=self.factory.game)

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
        event_type, params = event[pp.message_struct.TYPE_KEY], event[pp.message_struct.PARAMS_KEY]

        # Не будем лепить костылей по отсылке приватных сообщений до тех пор пока это не будет
        # запилено на стороне клиента

        log.info('{signal} caught', signal=msg)

        if event_type == pp.event_types.CHAT_REGISTER:
            self.handle_chat_register(event)
        elif event_type == pp.event_types.CHAT_MESSAGE:
            self.handle_chat_message(event)
        elif event_type == pp.event_types.LOBBY_READY:
            self.handle_lobby_ready(event)
        elif event_type == pp.event_types.LOBBY_NOT_READY:
            self.handle_lobby_not_ready(event)
        elif event_type in [pp.event_types.ACTION_JUST, \
                            pp.event_types.ACTION_PIPE, \
                            pp.event_types.ACTION_SEQUENCE]:
            # print self.game
            self.factory.game.receive_message(msg)
            self.send_game_flow()


    # Отправка сообщений клиентам

    def handle_chat_register(self, params):
        """
        Посылаем всем клиентам сообщения о том, кто подключился, и сохраняем адрес и ник
        """

        # TODO: this is hacky
        self.factory.echoers.append(self)

        new_user_name = params[pp.message_struct.PARAMS_KEY][pp.chat.NAME_KEY]
        if new_user_name in [player.name for player in self.factory.players.values()]:
            msg = {
                pp.message_struct.TYPE_KEY: pp.event_types.LOBBY_NAME_ALREADY_EXISTS,
                pp.message_struct.PARAMS_KEY: {}
            }
            self.factory.echoers[-1].transport.write(json.dumps(msg))
            del self.factory.echoers[-1]

        else:
            self.factory.players[self] = LobbyPerson(new_user_name)

            # first, tell about users online to a newly joined person (they're already on the list)
            online_msg = {
                pp.message_struct.TYPE_KEY: pp.event_types.CHAT_USERS_ONLINE,
                pp.message_struct.PARAMS_KEY: {
                    pp.chat.NAMES_KEY: [player.name for player in self.factory.players.values()]
                }
            }
            self.factory.send_individual_message(new_user_name, json.dumps(online_msg))

            # after that, tell everyone else someone's just joined
            params[pp.message_struct.TYPE_KEY] = pp.event_types.CHAT_JOIN
            # TODO: fix later
            params[pp.message_struct.PARAMS_KEY][pp.chat.NAME_KEY] = new_user_name
            log.info('some {data} sent', data=str(params))
            for player in self.factory.players.itervalues():
                if player.name != new_user_name:
                    self.factory.send_individual_message(player.name, json.dumps(params))

    def handle_chat_disconnection(self):
        """
        Говорим всем о том кто ушел
        """

        # TODO: понять почему это работает, сделать нормально
        parted = self.factory.players.pop(self, 'not found')

        part_message = {
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_PART,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: getattr(parted, 'name')
            }
        }

        log.info('some {data} sent', data=str(part_message))
        self.send_global_message(json.dumps(part_message))

    def handle_lobby_ready(self, params):
        """ Вызывать если клиент жмет чекбокс "ready" """

        self.factory.players[self].get_ready()
        log.info('This {player} now is ready: ', player=str(params[pp.message_struct.PARAMS_KEY][pp.chat.NAME_KEY]))
        self.check_playnum()

    def handle_lobby_not_ready(self, params):
        """ Вызывать если клиент отжимает чекбокс "ready" """

        self.factory.players[self].get_unready()


        if self.run_game_launcher is not None and self.run_warning is not None:
            self.run_game_launcher.cancel()
            self.run_warning.stop()
        self.anncounter = 0
        # TODO: make smth with this hack
        if hasattr(self.factory, 'game'):
            del self.factory.game

        log.info('This {player} now is not ready: ', player=str(params[pp.message_struct.PARAMS_KEY][pp.chat.NAME_KEY]))

    def handle_chat_message(self, params):
        """
        Просто отсылаем всем то, что нам пришло
        """
        self.send_global_message(json.dumps(params))

    # Здесь будет все что имеет отношение уже к сессии

    def send_game_flow(self):
        # Передаем продюсеру инфу о порождающем классе
        message_producer = Producer(self.factory)
        try:
            message_producer.resumeProducing()
        except GameOver as game_over:
            msg = {
                pp.message_struct.TYPE_KEY: pp.event_types.LOBBY_GAME_OVER,
                pp.message_struct.PARAMS_KEY: {
                    pp.lobby.GAME_RESULT_KEY: game_over.players_stats,
                }
            }
            self.send_global_message(json.dumps(msg))
            self.finish_game()

    def finish_game(self):
        self.anncounter = 0
        self.factory.game = None
        self.run_game_launcher = None
        self.run_warning = None

class MultiEchoFactory(protocol.Factory):

    def __init__(self, playnum):
        self.echoers = []
        self.player_num = playnum
        self.players = {}
        self.announcment_counter = 0
        self.game = ''
        log.info('Instantiated server for {playernum} players', playernum=self.player_num)

    def buildProtocol(self, addr):
        return MultiEcho(self, self.player_num, self.announcment_counter)

    def instantiate_game(self):
        self.game = retard_game.RetardGame([{'name': str(x.name)} for x in self.players.values()])

    # Рассылка индивидуальных сообщений перенесена в класс-фабрику, т.к.
    # 1. её реализация в MultiEcho использовала только фабричные аттрибуты
    # 2. этот метод скорее всего пригодится для класса Producer
    def send_individual_message(self, player, msg):
        for identifier, person in self.players.iteritems():
            if person.name == player:
                endpoint = identifier

        # TODO: доработать если попытка отправит несуществующему клиенту
        endpoint_index = self.echoers.index(endpoint)
        self.echoers[endpoint_index].transport.write(msg)

class Producer:
    """Apply .run() until the responce is None """
    implements(interfaces.IPushProducer)

    def __init__(self, factory):
        self._paused = False
        self.factory = factory

    def pauseProducing(self):
        self._paused = True

    def resumeProducing(self):
        self._paused = False
        response = True

        while response:
            response = self.factory.game.run()
            if response is not None:
                for client_name in response:

                    self.factory.send_individual_message(
                        client_name,
                        response[client_name] + pp.message_delimiter
                    )

        self.pauseProducing()

    def stopProducing(self):
        pass

if __name__ == '__main__':
    reactor.listenTCP(8000, MultiEchoFactory(2))
    reactor.run()
