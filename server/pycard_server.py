# -*- coding: utf-8 -*-
"""
Попытка запилить асинхронный сервер, который общается с клиентами
с помощью текстовых сообщений
"""


__author__ = 'Ecialo'

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet import protocol
from kivy.app import App
from kivy.uix.label import Label
from core import game


class MultiEcho(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.echoers.append(self)

    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        for echnum in xrange(len(self.factory.echoers)):
            self.factory.echoers[echnum].transport.write(response[echnum])

    def connectionLost(self, reason):
        self.factory.echoers.remove(self)


class MultiEchoFactory(protocol.Factory):

    def __init__(self, app):
        self.echoers = []
        self.app = app

    def buildProtocol(self, addr):
        return MultiEcho(self)


class TwistedServerApp(App):
    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, MultiEchoFactory(self))
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
            player_one_msg = "I am player one"
            player_two_msg = "I am player two"

        self.label.text += "responded: %s\n" % msg
        return [player_one_msg, player_two_msg]

if __name__ == '__main__':
    TwistedServerApp().run()
