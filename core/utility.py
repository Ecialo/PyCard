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
        predef.MESSAGE_ACTION_KEY: {action_name: kwargs},
        predef.MESSAGE_AUTHOR_KEY: author,
    }
    # return "(" + action_name + " " + json.dumps(kwargs) + ")"
    return json.dumps(message)


def make_pipe_message(*args):
    message = {
        predef.MESSAGE_TYPE_KEY: predef.ACTION_PIPE,
        predef.MESSAGE_ACTION_KEY: args

    }
    # return "(" + "|".join(args) + ")"
    return json.dumps(message)


def make_sequence_message(*args):
    message = {
        predef.MESSAGE_TYPE_KEY: predef.ACTION_SEQUENCE,
        predef.MESSAGE_ACTION_KEY: args

    }
    return json.dumps(message)
    # return "(" + "&".join(args) + ")"
