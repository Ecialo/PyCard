# -*- coding: utf-8 -*-
"""
Попытка запилить асинхронный сервер, который общается с клиентами
с помощью текстовых сообщений
"""

import io
from twisted.internet.task import LoopingCall
from twisted.application import service
from twisted.application.internet import TimerService
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, defer
from twisted.internet import protocol
from kivy.app import App
from kivy.uix.label import Label
from twisted.logger import Logger, jsonFileLogObserver
from testing.retard_game import RetardGame
from core.utility import check_playnum

__author__ = 'Anton Korobkov'

log = Logger(observer=jsonFileLogObserver(io.open("server.json", "a")),
                 namespace="server")

class MultiEcho(protocol.Protocol):

    def __init__(self, factory, players):
        self.factory = factory
        self.required_players_number = players
        self.current_player_index = None
        self.players = {}
        self.players_settled = False

    def connectionMade(self):
        log.info('Incoming connection on {host}', host=self)
        self.factory.echoers.append(self)

    @check_playnum(log)
    def dataReceived(self, data):
        log.info('Data obtained {data}', data=data)

        if self.players_settled is False:
            self.set_players(self.factory.echoers)

        response = self.factory.app.handle_message(data)
        self.send_stuff(response)


    def connectionLost(self, reason):
        log.debug('Connection {conn} is lost because of {lost_reason}',
                  conn=self, lost_reason=reason)
        self.factory.echoers.remove(self)
        self.players_settled = False

    def send_stuff(self, data):
        self.current_player_index = self.factory.echoers.index(self)
        self.factory.echoers[self.current_player_index].transport.write(data[0])

        # Переделать когда настанет пора отсылать совсем разным клиентам совсем разные данные
        for player_num in xrange(len(self.factory.echoers)):
            if player_num != self.current_player_index:
                self.factory.echoers[player_num].transport.write(data[1])

    def set_players(self, players):
        # Пока не используется. Юзать когда разным клиентам нужно будет совсем разные сообщения посылать

        for player_num, player in enumerate(players):
            self.players[player_num] = player

        self.players_settled = True


class MultiEchoFactory(protocol.Factory):

    def __init__(self, app):
        self.echoers = []
        self.app = app
        self.players = 2
        log.info('Instantiated server for {playernum} players', playernum=self.players)

    def buildProtocol(self, addr):
        return MultiEcho(self, self.players)


class TwistedServerApp(App):
    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, MultiEchoFactory(self))
        self.retard = RetardGame()
        test_call = LoopingCall(self.retard.run)
        test_call.start(0.5)
        return self.label

    def handle_message(self, msg):
        """
        Обрабатывает входящие сообщения от клиентов
        :param msg: str
        :return:
        """
        # TODO: fix retard.recieve_message

        # Если запускать это с сообщениями неподходящего формата то все валится НАХУЙ
        self.retard.receive_message(msg)
        action = self.retard.run()
        self.label.text = "received:  %s\n" % msg
        player_one_msg = action.make_message()
        player_two_msg = action.make_message()

        self.label.text += "responded: %s\n" % msg
        log.info('Message for player one is {message_one}, for player two is {message_two}'
                 , message_one=player_one_msg, message_two=player_two_msg)
        return [player_one_msg, player_two_msg]

if __name__ == '__main__':
    TwistedServerApp().run()
