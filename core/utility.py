# -*- coding: utf-8 -*-
from . import predef
__author__ = 'Ecialo'


class Component(object):

    name = None
    categories = None
    associated_components = []

    def __init__(self):
        self._name = self.name

    def setup_prefix(self, prefix):
        self._name = prefix + "_" + self.name

    @property
    def fullname(self):
        return self._name

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

    def __init__(self):
        pass

    @classmethod
    def setup_prefix(cls, prefix):
        cls._name = prefix + "_" + cls.name


def make_message(action_name, **kwargs):
    """
    Формат сообщения (имя_сообщения именованный_аргумент=сообщение_или_значение;другой_именованный_аргумент=...
    """
    return "(" + action_name + " " + ";".join(map(lambda key, value: key + "=" + value, kwargs.iteritems())) + ")"


def make_pipe_message(*args):
    return "(" + "|".join(args) + ")"


def make_sequence(*args):
    return "(" + "&".join(args) + ")"
