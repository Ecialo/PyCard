# -*- coding: utf-8 -*-
import json
from . import predef
__author__ = 'Ecialo'


class ChangeIdentityError(Exception):
    pass


class Component(object):

    name = None
    categories = []
    associated_components = []
    hooks = []

    def __init__(self):
        self._name = self.name
        self._id = None

    def setup_prefix(self, prefix):
        self._name = prefix + "_" + self._name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if self._id is None:
            self._id = value
            self._name += "_" + str(value)
        else:
            raise ChangeIdentityError()

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


def make_message(author, message_struct):        # TODO нужно немного обобщить
    """
    Формат сообщения {имя_сообщения: {параметр: значение}}
    """
    message = {
        predef.MESSAGE_TYPE_KEY: predef.ACTION_JUST,
        predef.MESSAGE_PARAMS_KEY: {
            predef.MESSAGE_ACTION_KEY: message_struct,
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


def check_pycard_protocol(message_or_action_struct):
    action_struct = message_or_action_struct if not isinstance(message_or_action_struct, basestring) else json.loads(message_or_action_struct)
    valid_type = action_struct.get('type') in range(12)
    params = action_struct.get('params')
    params_valid_type = isinstance(params, dict)
    return valid_type and params_valid_type
    # return "(" + "&".join(args) + ")"
