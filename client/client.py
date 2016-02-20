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
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
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
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        log.debug('Failed to connect to {connection} because of {fail_reason}',
                  connection=conn, fail_reason=reason)
        self.app.print_message("connection failed")


# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None

    def build(self):
        root = self.setup_gui()
        self.connect_to_server('localhost', 8000)
        return root

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def connect_to_server(self, host, port):
        reactor.connectTCP(host, port, EchoFactory(self))
        log.info('Successfully connected to server {server} on port {port}',
                 server=host, port=port)


    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    def print_message(self, msg):
        self.label.text += msg + "\n"

if __name__ == '__main__':
    TwistedClientApp().run()