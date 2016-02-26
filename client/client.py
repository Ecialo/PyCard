# -*- coding: utf-8 -*-
""" Test client """

from uuid import getnode as get_mac

# install_twisted_rector must be called before importing the reactor
import io
from kivy.support import install_twisted_reactor
install_twisted_reactor()

# A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory

from twisted.logger import Logger, jsonFileLogObserver

log = Logger(observer=jsonFileLogObserver(io.open("client.json", "a")),
                 namespace="client")

__author__ = 'Anton Korobkov'

class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        log.info('Message recieved {message}', message=data)
        self.factory.app.print_message(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        log.debug('Connection {connection} lost because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.print_message("Connection lost!")

    def clientConnectionFailed(self, conn, reason):
        log.debug('Failed to connect to {connection} because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.print_message("Connection failed!")


# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None

    # spawns a modal widget with connection settings
    def build(self):
        root = Builder.load_file('./client.kv')
        return root

    def on_start(self):
        Factory.ConnectionWidget().open()

    def connect_to_server(self, host, port):
        reactor.connectTCP(host, port, EchoFactory(self))
        log.info('Successfully connected to server {server} on port {port}',
                 server=host, port=port)

    def on_connection(self, connection):
        self.print_message("Connected succesfully!")
        self.connection = connection

    def send_message(self, msg):
        if msg and self.connection:
            self.connection.write(str(msg))
            self.root.ids.input_field.text = ""

    # scroll down if there're less than 2 lines of text below the viewport
    # it turns out that each line is (1.5 * font_h) pixels tall, or so it looks
    def scroll_if_necessary(self):
        hidden_h = self.root.ids.chatlog.height - self.root.ids.scroll_view.height
        font_h = self.root.ids.chatlog.font_size
        near_the_bottom = (self.root.ids.scroll_view.scroll_y * hidden_h < 3.0 * font_h)
        if near_the_bottom:
            self.root.ids.scroll_view.scroll_y = 0

    def print_message(self, msg):
        self.root.ids.chatlog.text += msg + "\n"
        self.scroll_if_necessary()


if __name__ == '__main__':
    TwistedClientApp().run()
