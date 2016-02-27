# -*- coding: utf-8 -*-
from itertools import chain
from predef import *
from flow.flow import EndOfCurrentFlow
__author__ = 'Ecialo'


class WTFError(Exception):
    pass


class GameOver(Exception):
    pass


class Game(object):
    """
    Агрегирует все компоненты необходимые для игры. Так же через этот класс
    реализуется игровое взаимодействие, тут регистрируются эффекты и прочее.
    Компоненты: Доски, Колоды, Таблица карт, таблица допустимых действий.
    Многие прочие компоненты вместе с именами генерируются на основе flow игры.
    Генерируемые компоненты лежат в общих таблицах под своими полными именами.
    """
    def __init__(
            self,
            components,
            flow,
            mode
    ):

        self._mode = mode
        if mode is CLIENT:      # TODO сделать более умное разделение режимов
            self.run = None

        self._components = {
            PLAYER: {},
            DESK: {},
            DECK: {},
            RESOURCE: {},
            HAND: {},
            TABLE: {},
        }
        # components = chain(
        #     components,
        #     *(map(
        #         lambda component: component.associated_components,
        #         components
        #     ) + flow.associated_components)
        # )
        for component in components:
            self.register_component(component)
        self._flow = flow(self)

    def __getitem__(self, (category, name)):
        return self._components[category][name]

    def get_category(self, category):
        return self._components[category]

    def run(self):
        try:
            action = self._flow.run()
            # print action
        except EndOfCurrentFlow:
            raise GameOver()
        else:
            if action:
                action.apply()
                visibility = self.expand_visibility(action)
                return self.response(action, visibility)
            else:
                return None

    # def make_response(self):

    def expand_visibility(self, action):
        players = self.get_category(PLAYER).keys()
        visibility = action.visibility
        if visibility == ALL:
            return {
                player: True
                for player in players
            }
        elif visibility == AUTHOR:
            return {
                player: (player == action.author)
                for player in players
            }
        else:
            return {
                player: False
                for player in players
            }

    # def apply_action(self, action):
    #     action.apply(self)

    def response(self, action, visibility):
        players = self.get_category(PLAYER).keys()
        return {
            player: (action.make_visible_response() if visibility[player] else action.make_invisible_response())
            for player in players
        }

    def register_component(self, component):
        for category in component.categories:
            self._components[category][component.fullname] = component
        for associated_component in component.associated_components:
            self.register_component(associated_component)

    def receive_message(self, message):
        """
        Принимает сообщение, передаёт его в парсер, а затем передаёт полученное действие в игровой поток
        """
        action = self._components[TABLE][ACTION].receive_message(message, self)
        if self._mode is SERVER:
            self._flow.receive_action(action)
        elif self._mode is CLIENT:
            action.apply()
        else:
            raise WTFError()
