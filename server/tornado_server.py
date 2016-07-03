# -*- coding: utf-8 -*-
"""
Перенос логики pycard_server на tornado
"""
import sys
import json
from tornado import (
    ioloop,
    tcpserver,
    gen,
    queues,
)
from core.predef import (
    pycard_protocol as pp,
    ALL,
)
from sample_games.retard_game import retard_game
from core.game import GameOver

__author__ = 'ecialo', 'Anton Korobkov'


class User(object):

    def __init__(self, stream, server):
        self.is_alive = True
        self.is_ready = False
        self.stream = stream
        self.name = None
        self.message_queue = queues.Queue()
        self.server = server

    @gen.coroutine
    def emmit_message(self, message):
        yield self.server.enqueue_messages(message)

    @gen.coroutine
    def await_messages(self):
        while self.is_alive:
            # print "ololo"
            msg = yield self.stream.read_bytes(1000, partial=True)
            # msg = yield self.stream.read_until(pycard_protocol.message_delimiter)
            ioloop.IOLoop.current().spawn_callback(self.parse_incoming_message, msg)

    @gen.coroutine
    def await_handshake(self):
        msg = yield self.stream.read_bytes(1000, partial=True)
        event = json.loads(msg)
        # event_type, params = event[pp.message_struct.TYPE_KEY], event[pp.message_struct.PARAMS_KEY]
        self.handle_chat_register(event)

    @gen.coroutine
    def parse_incoming_message(self, msg):
        """
        Родной брат метода client.parse_message
        """
        print "PARSE", msg
        event = json.loads(msg)
        event_type, params = event[pp.message_struct.TYPE_KEY], event[pp.message_struct.PARAMS_KEY]

        # Не будем лепить костылей по отсылке приватных сообщений до тех пор пока это не будет
        # запилено на стороне клиента

        # log.info('{signal} caught', signal=msg)
        #
        # if event_type == pp.event_types.CHAT_REGISTER:
        #     yield self.handle_chat_register(event)
        if event_type == pp.event_types.CHAT_MESSAGE:
            yield self.handle_chat_message(event)
        elif event_type == pp.event_types.LOBBY_READY:
            yield self.handle_lobby_ready(event)
        elif event_type == pp.event_types.LOBBY_NOT_READY:
            yield self.handle_lobby_not_ready(event)
        # elif event_type in [pp.event_types.ACTION_JUST, \
        #                     pp.event_types.ACTION_PIPE, \
        #                     pp.event_types.ACTION_SEQUENCE]:
        #     # print self.game
        #     self.factory.game.receive_message(msg)
        #     self.send_game_flow()

    # @gen.coroutine
    def handle_chat_register(self, event):
        self.name = event[pp.message_struct.PARAMS_KEY][pp.chat.NAME_KEY]

    @gen.coroutine
    def handle_chat_message(self, event):
        yield self.emmit_message(
            {ALL: json.dumps(event)}
        )

    @gen.coroutine
    def handle_lobby_ready(self, _):
        self.is_ready = True
        yield self.server.start_preparation()

    @gen.coroutine
    def handle_lobby_not_ready(self, _):
        self.is_ready = False
        yield self.server.break_preparation()

    @gen.coroutine
    def send_message(self):
        while self.is_alive:
            message = yield self.message_queue.get()
            # print message, isinstance(message, bytes), type(message)
            yield self.stream.write(message)
            self.message_queue.task_done()

    @gen.coroutine
    def enqueue_message(self, message):
        yield self.message_queue.put(message)


class PyCardServer(tcpserver.TCPServer):

    def __init__(self, players_per_game, *args):
        super(PyCardServer, self).__init__(*args)
        self.users = {}
        self.is_ready = False
        self.queue = queues.Queue()

        self.player_num = players_per_game
        self.game = None

        ioloop.IOLoop.current().spawn_callback(self.send_message)

    @gen.coroutine
    def handle_stream(self, stream, address):
        user = User(stream, self)
        yield user.await_handshake()
        yield self.add_user(user)

    @gen.coroutine
    def add_user(self, user):
        self.users[user.name] = user
        loop = ioloop.IOLoop.current()
        loop.spawn_callback(user.await_messages)
        loop.spawn_callback(user.send_message)
        online_msg = {
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_USERS_ONLINE,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAMES_KEY: [username for username in self.users.iterkeys()]
            }
        }
        yield self.enqueue_messages({user.name: json.dumps(online_msg)})

        chat_join_message = json.dumps({
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_JOIN,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: user.name
            }
        })

        yield self.enqueue_messages(
            {username: chat_join_message for username in self.users if username != user.name}
        )

    def remove_user(self, user):
        pass

    @gen.coroutine
    def send_message(self):
        """
        Достает из очереди словарь {receiver: message} и отправляет всем reciever их message
        Если receiver это ALL, то отправляет message всем
        :return:
        :rtype:
        """
        while True:
            rec_messages = yield self.queue.get()
            if ALL in rec_messages:
                message = rec_messages[ALL]
                yield [user.enqueue_message(message + pp.message_delimiter) for user in self.users.itervalues()]
            else:
                yield [self.users[user].enqueue_message(message + pp.message_delimiter) for user, message in rec_messages.iteritems()]
            self.queue.task_done()

    @gen.coroutine
    def enqueue_messages(self, messages):
        yield self.queue.put(messages)

    @gen.coroutine
    def start_preparation(self):
        if all([user.is_ready for user in self.users.itervalues()]) and len(self.users) == self.player_num:
            self.is_ready = True
            yield self.prepare_and_launch()
            # self.game = retard_game.RetardGame([{'name': str(x.name)} for x in self.users.values()])

    @gen.coroutine
    def break_preparation(self):
        self.is_ready = False
        msg = {
                pp.message_struct.TYPE_KEY: pp.event_types.CHAT_MESSAGE,
                pp.message_struct.PARAMS_KEY: {
                    pp.chat.NAME_KEY: 'Server message',
                    pp.chat.MESSAGE_TYPE_KEY: pp.chat.message_type.BROADCAST,
                    pp.chat.TEXT_KEY: "Cancel"
                }
            }
        msg = {
            ALL: json.dumps(msg)
        }
        yield self.enqueue_messages(msg)

    @gen.coroutine
    def prepare_and_launch(self):
        for i in xrange(5):
            # print self.is_ready
            if not self.is_ready:
                break
            msg = {
                pp.message_struct.TYPE_KEY: pp.event_types.CHAT_MESSAGE,
                pp.message_struct.PARAMS_KEY: {
                    pp.chat.NAME_KEY: 'Server message',
                    pp.chat.MESSAGE_TYPE_KEY: pp.chat.message_type.BROADCAST,
                    pp.chat.TEXT_KEY: ' '.join(['game is going to start in', str(5 - i), 'seconds'])
                }
            }
            msg = {
                ALL: json.dumps(msg)
            }
            yield [self.enqueue_messages(msg), gen.sleep(1)]
        else:
            yield self.launch_game()

    @gen.coroutine
    def launch_game(self):
        msg = {
            pp.message_struct.TYPE_KEY: pp.event_types.CHAT_MESSAGE,
            pp.message_struct.PARAMS_KEY: {
                pp.chat.NAME_KEY: 'Server message',
                pp.chat.MESSAGE_TYPE_KEY: pp.chat.message_type.BROADCAST,
                pp.chat.TEXT_KEY: "OLOLO"
            }
        }
        msg = {
            ALL: json.dumps(msg)
        }
        yield self.enqueue_messages(msg)

if __name__ == '__main__':
    config_file = sys.argv[1]
    with open(config_file) as conf:
        config = json.load(conf)
    port = config['configs']['port']
    players_per_game = config['configs']['playnum']

    server = PyCardServer(players_per_game)
    server.listen(port)
    ioloop.IOLoop.current().start()
