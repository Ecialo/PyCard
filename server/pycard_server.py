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
from core.utility import check_is_false

class MultiEcho(protocol.Protocol):
    # TODO: исправить хаки

    def __init__(self, factory):
        self.factory = factory
        self.current_player_index = None
        self.another_player_index = None

    def connectionMade(self):
        self.factory.echoers.append(self)

    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        self.send_response(response, self)

    def connectionLost(self, reason):
        self.factory.echoers.remove(self)
        # self.players_settled = False

    def send_response(self, data, echoer):
        if echoer == self.factory.echoers[1]:
            rev_data = data[::-1]
            for echoer in xrange(len(self.factory.echoers)):
                self.factory.echoers[echoer].transport.write(rev_data[echoer])

        else:
            for echoer in xrange(len(self.factory.echoers)):
                self.factory.echoers[echoer].transport.write(data[echoer])

    def send_stuff(self, data):
        self.factory.echoers[self.current_player_index].transport.write(data[0])
        self.factory.echoers[self.another_player_index].transport.write(data[1])


    def determine_current_player(self):
        self.current_player_index = self.factory.echoers.index(self)
        # TODO: это хак на 2 человек - нужно что-то поумнее придумать и допилить
        if self.current_player_index == 0:
            self.another_player_index = 1
        else:
            self.another_player_index = 0



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
