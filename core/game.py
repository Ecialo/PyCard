# -*- coding: utf-8 -*-
from itertools import chain
from predef import *
from flow.flow import EndOfCurrentFlow
__author__ = 'Ecialo'


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
    ):
        self._components = {
            PLAYER: {},
            DESK: {},
            DECK: {},
            RESOURCE: {},
            HAND: {},
            TABLE: {},
        }
        components = chain(
            components,
            *(map(
                lambda component: component.associated_components,
                components
            ) + flow.associated_components)
        )
        for component in components:
            self.register_component(component)
        self._flow = flow(self._components[PLAYER].values())

    def __getitem__(self, item):
        return self._components[item[0]][item[1]]

    def run(self):
        try:
            return self._flow.run()
        except EndOfCurrentFlow:
            raise GameOver()

    def apply_action(self, action):
        action.apply(self)

    def register_component(self, component):
        for category in component.categories:
            self._components[category][component.fullname] = component

    def receive_message(self, message):
        """
        Принимает сообщение, передаёт его в парсер, а затем применяет вернувшееся действие
        """
        self._components[TABLE][ACTION].receive_message(message, self).apply()
