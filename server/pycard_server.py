# -*- coding: utf-8 -*-
"""
Попытка запилить асинхронный сервер, который общается с клиентами
с помощью текстовых сообщений
"""

import io
import json
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
import core.predef as predef

__author__ = 'Anton Korobkov'

log = Logger(observer=jsonFileLogObserver(io.open("server.json", "a")),
                 namespace="server")

class MultiEcho(protocol.Protocol):

    def __init__(self, factory, players):
        self.factory = factory
        self.players = {}

    def connectionMade(self):
        log.info('Incoming connection on {host}', host=self)

    def dataReceived(self, data):
        log.info('Data obtained {data}', data=data)
        self.parse_incoming_message(data)

    def connectionLost(self, reason):
        log.debug('Connection {conn} is lost because of {lost_reason}',
                  conn=self, lost_reason=reason)
        self.handle_chat_disconnection()

    def send_global_message(self, msg):
        """
        Юзать этот метод когда нужно что-то одинаковое написать всем клиентам
        """

        for player in self.factory.echoers:
            player.transport.write(msg)

    # Обработка сообщений клиента

    def parse_incoming_message(self, msg):
        """
        Родной брат метода client.parse_message
        """

        event = json.loads(msg)
        event_type, params = event[predef.MESSAGE_TYPE_KEY], event[predef.MESSAGE_PARAMS_KEY]

        # Не будем лепить костылей по отсылке приватных сообщений до тех пор пока это не будет
        # запилено на стороне клиента

        if event_type == predef.CHAT_REGISTER:
            self.handle_chat_join(event)
        elif event_type == predef.CHAT_MESSAGE:
            self.handle_chat_message(event)

    # Отправка сообщений клиентам

    def handle_chat_join(self, params):
        """
        Посылаем всем клиентам сообщения о том кто зашел и сохраняем адрес и ник
        """

        # TODO: отрефакторить это обязательно!
        self.players[self] = [params[predef.MESSAGE_PARAMS_KEY][predef.CHAT_MAC_KEY],
                              params[predef.MESSAGE_PARAMS_KEY][predef.CHAT_NAME_KEY]]

        params[predef.MESSAGE_TYPE_KEY] = predef.CHAT_JOIN

        log.info('some {data} sent', data=str(params))
        self.send_global_message(json.dumps(params))
        self.factory.echoers.append(self)

    def handle_chat_disconnection(self):
        """
        Говорим всем о том кто ушел
        """

        self.factory.echoers.remove(self)

        part_message = {predef.MESSAGE_TYPE_KEY: predef.CHAT_PART,
                        predef.MESSAGE_PARAMS_KEY: {
                            predef.CHAT_NAME_KEY: self.players[self][1],  # TODO: ещё один хак который надо будет убрать
                            predef.CHAT_MAC_KEY: self.players[self][0]
                        }
                        }

        log.info('some {data} sent', data=str(part_message))
        self.send_global_message(json.dumps(part_message))

    def handle_chat_message(self, params):
        """
        Просто отсылаем всем то, что нам пришло
        """
        self.send_global_message(json.dumps(params))


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
        """
        # TODO: fix retard.recieve_message

        # Если запускать это с сообщениями неподходящего формата то все валится НАХУЙ
        self.retard.receive_message(msg)
        action = self.retard.run()
        self.label.text = "received:  %s\n" % msg
        client_one_msg = action.make_message()
        client_two_msg = action.make_message()

        self.label.text += "responded: %s\n" % msg
        log.info('Message for player one is {message_one}, for player two is {message_two}'
                 , message_one=client_one_msg, message_two=client_two_msg)
        return [client_one_msg, client_two_msg]

if __name__ == '__main__':
    TwistedServerApp().run()
