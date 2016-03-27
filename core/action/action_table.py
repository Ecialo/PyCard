# -*- coding: utf-8 -*-
import json
from operator import and_
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
        # print "\n\n\n"
        # print message
        # print action
        # print "\n\n\n"
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

        raw_action = raw_action[predef.MESSAGE_PARAMS_KEY]
        author = raw_action[predef.MESSAGE_AUTHOR_KEY]
        if action_type is predef.ACTION_JUST:
            return self._cook_action(raw_action[predef.MESSAGE_ACTION_KEY], author)
        elif action_type is predef.ACTION_SEQUENCE:
            return reduce(
                and_,
                map(
                    lambda canned_raw_action: self._cook_action(canned_raw_action, author),
                    raw_action[predef.MESSAGE_ACTION_KEY]
                )
            )
        elif action_type is predef.ACTION_PIPE:
            pass

    def _cook_action(self, raw_action, author):
        # print "bullshit"
        # print raw_action
        # print raw_action.items()
        action_name, params = raw_action.items()[0]
        cooked_action = self[action_name](author, **params)
        return cooked_action

    def __getitem__(self, item):
        return self._actions[item]
