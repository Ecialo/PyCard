# -*- coding: utf-8 -*-
"""
Попытка запилить асинхронный сервер, который общается с клиентами
с помощью текстовых сообщений
"""

import io
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet import protocol
from kivy.app import App
from kivy.uix.label import Label
from twisted.logger import Logger, jsonFileLogObserver

__author__ = 'Anton Korobkov'

log = Logger(observer=jsonFileLogObserver(io.open("server.json", "a")),
                 namespace="server")

class MultiEcho(protocol.Protocol):
    # TODO: исправить оставшиеся хаки

    def __init__(self, factory, players):
        self.factory = factory
        self.required_players_number = players
        self.current_player_index = None
        self.players = {}
        self.players_settled = False

    def connectionMade(self):
        self.factory.echoers.append(self)

    def dataReceived(self, data):
        # TODO: пока это будет работать так, но лучше избавиться от этой фигни

        if len(self.factory.echoers) < self.required_players_number:
            for client in self.factory.echoers:
                client.transport.write('Not enough players. Wait for others to join the room')
        else:
            if self.players_settled is False:
                self.set_players(self.factory.echoers)

            response = self.factory.app.handle_message(data)
            self.send_stuff(response)



    def connectionLost(self, reason):
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

    def buildProtocol(self, addr):
        return MultiEcho(self, self.players)


class TwistedServerApp(App):
    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(self.port, MultiEchoFactory(self))
        return self.label

    def handle_message(self, msg):
        """
        Обрабатывает входящие сообщения от клиентов
        :param msg: str
        :return:
        """
        # TODO: Add some real message processing

        self.label.text = "received:  %s\n" % msg

        # Попытка передать разные сообщения двум разным людям

        if msg == "ping":
            player_one_msg = "ping"
            player_two_msg = "pong"
        else:
            player_one_msg = "I am sending this message"
            player_two_msg = "I am receiving this message"

        self.label.text += "responded: %s\n" % msg
        return [player_one_msg, player_two_msg]

if __name__ == '__main__':
    TwistedServerApp(8000).run()
