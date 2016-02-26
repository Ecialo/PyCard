# -*- coding: utf-8 -*-
import json
from ..utility import Table
from .. import predef
__author__ = 'Ecialo'


class ActionTable(Table):
    """
    Таблица допустимых действий.
    """

    name = predef.ACTION
    actions = []

    _actions = {}

    def init(self):
        for action in self.actions:
            self._actions[action.name] = action
        # print self._actions, 123

    def receive_message(self, message, game):
        """
        Создать на основе полученного Сообщения Действие с контекстом.

        :param message: Сообщение
        :type message: str
        :param game: Игра для которой предназначено сообщение
        :type game: core.game.Game
        :return: Действие полученное в результате разбора и подстановки.
        :rtype: core.action.Action
        """
        action = self._parse_message(message)
        action.substitute_enviroment(game)
        return action

    # @staticmethod
    def _parse_message(self, message):
        """
        Разобрать Сообщение основываясь на известных Действиях.

        :param message: Сообщение
        :type message: str
        :return: Действие без контекста
        """
        raw_action = json.loads(message)
        action_type = raw_action[predef.MESSAGE_TYPE_KEY]
        if action_type is predef.ACTION_JUST:
            action_name, action_args = raw_action[predef.MESSAGE_ACTION_KEY].items()[0]
            action = self._actions[action_name]()
            # print action_args
            return action.setup(**action_args)

    # def _distinct_sequence(self, message):
    #     return message.split("&")
