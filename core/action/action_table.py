# -*- coding: utf-8 -*-
import json
from ..utility import Table
from .. import predef
__author__ = 'Ecialo'


class ActionTable(Table):

    name = predef.ACTION
    actions = []
    _actions = {}

    def init(self):
        for action in self.actions:
            self._actions[action.name] = action
        # print self._actions, 123

    def receive_message(self, message, game):
        """
        Формат сообщения (имя_сообщения именованный_аргумент=сообщение_или_значение;другой_именованный_аргумент=...
        """
        action = self._parse_message(message)
        action.substitute_enviroment(game)
        return action

    # @staticmethod
    def _parse_message(self, message):
        raw_action = json.loads(message)
        action_type = raw_action[predef.MESSAGE_TYPE_KEY]
        author = raw_action[predef.MESSAGE_AUTHOR_KEY]
        if action_type is predef.ACTION_JUST:
            action_name, action_args = raw_action[predef.MESSAGE_ACTION_KEY].items()[0]
            action = self._actions[action_name](author)
            # print action_args
            return action.setup(**action_args)

    # def _distinct_sequence(self, message):
    #     return message.split("&")
