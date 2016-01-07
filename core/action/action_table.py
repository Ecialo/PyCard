# -*- coding: utf-8 -*-
from ..utility import Table
from .. import predef
__author__ = 'Ecialo'


class ActionTable(Table):

    name = predef.ACTION
    actions = []
    _actions = {}

    def init(self):
        for action in self._actions:
            self._actions[action.name] = action

    def receive_message(self, message, game):
        """
        Формат сообщения (имя_сообщения именованный_аргумент=сообщение_или_значение;другой_именованный_аргумент=...
        """
        action = self._parse_message(message)
        action.setup(game=game)
        return action

    # @staticmethod
    def _parse_message(self, message):
        action, args = message.lstrip("(").rstrip(")").split()
        parsed_args = dict(
            map(
                lambda arg: arg.split("="),
                args.split(";")
            )
        )
        action = self._actions[action]
        return action.setup(**parsed_args)

    # def _distinct_sequence(self, message):
    #     return message.split("&")
