# -*- coding: utf-8 -*-
import json
from . import predef
__author__ = 'Ecialo'


class Component(object):

    name = None
    categories = []
    associated_components = []

    def __init__(self):
        self._name = self.name

    def setup_prefix(self, prefix):
        self._name = prefix + "_" + self.name

    @property
    def fullname(self):
        return self._name

    @property
    def path(self):
        return self.categories[0] + "_" + self.fullname

    # def make_get_action(self):
    #     componet_action = action.Get()
    #     componet_action.setup(
    #         category=self.categories[0],
    #         name=self.fullname,
    #     )
    #     return componet_action


class Singleton(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    def init(self):
        pass


class Table(Singleton, Component):

    categories = [predef.TABLE]

    @classmethod
    def setup_prefix(cls, prefix):
        cls._name = prefix + "_" + cls.name


def make_message(author, action_name, **kwargs):        # TODO нужно немного обобщить
    """
    Формат сообщения {имя_сообщения: {параметр: значение}}
    """
    message = {
        predef.MESSAGE_TYPE_KEY: predef.ACTION_JUST,
        predef.MESSAGE_PARAMS_KEY: {
            predef.MESSAGE_ACTION_KEY: {action_name: kwargs},
            predef.MESSAGE_AUTHOR_KEY: author,
        }
    }
    # return "(" + action_name + " " + json.dumps(kwargs) + ")"
    return json.dumps(message)


def make_pipe_message(author, *args):
    message = {
        predef.MESSAGE_TYPE_KEY: predef.ACTION_PIPE,
        predef.MESSAGE_PARAMS_KEY: {
            predef.MESSAGE_ACTION_KEY: args,
            predef.MESSAGE_AUTHOR_KEY: author
        }
    }
    # return "(" + "|".join(args) + ")"
    return json.dumps(message)


def make_sequence_message(author, *args):
    message = {
        predef.MESSAGE_TYPE_KEY: predef.ACTION_SEQUENCE,
        predef.MESSAGE_PARAMS_KEY: {
            predef.MESSAGE_ACTION_KEY: args,
            predef.MESSAGE_AUTHOR_KEY: author
        }
    }
    return json.dumps(message)
    # return "(" + "&".join(args) + ")"


def check_playnum(server_log):
    """
    Декоратор для server.pycard_server.MultiEcho.dataReceived
    Суть в том чтобы произвести проверку числа клиентов и не возвращать метод если
    их слишком мало, а вместо этого вернуть соответсвующий мессаг клиентам и
    написать об этом в лог
    :param server_log: twisted.logger.Logger
    :return:
    """

    def decorator_playnum(method):

        def compare_number(self, data):
            if len(self.factory.echoers) < self.required_players_number:
                for client in self.factory.echoers:
                    client.transport.write('Not enough players. Wait for others to join the room')
                server_log.info('Not enough players on {server}', server=self)
            else:
                return method(self, data)

        return compare_number

    return decorator_playnum
