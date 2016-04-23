# -*- coding: utf-8 -*-
from itertools import chain
from collections import defaultdict
import inspect
from predef import *
from . import utility as util
from flow.flow import EndOfCurrentFlow
__author__ = 'Ecialo'


class WTFError(Exception):
    pass


class GameOver(Exception):
    pass


class EndOfGame(Exception):
    pass


class Game(util.Component):
    """
    Агрегирует все компоненты необходимые для игры. Так же через этот класс
    реализуется игровое взаимодействие, тут регистрируются эффекты и прочее.
    Компоненты: Доски, Колоды, Таблица карт, таблица допустимых действий.
    Многие прочие компоненты вместе с именами генерируются на основе flow игры.
    Генерируемые компоненты лежат в общих таблицах под своими полными именами.
    """
    categories = [GAME]

    def __init__(
            self,
            components,
            flow,
            win_condition,
            mode
    ):
        super(Game, self).__init__()
        self._mode = mode
        if mode is CLIENT:      # TODO сделать более умное разделение режимов
            self.run = None

        self._components = {
            GAME: {},
            PLAYER: {},
            DESK: {},
            DECK: {},
            RESOURCE: {},
            HAND: {},
            TABLE: {},
        }
        self._next_id = 0
        self._components_by_id = {}
        # self._components_factories = {}
        #
        # for component in components:
        #     if inspect.isclass(component):
        #         self._components_factories[component.__name__] = component

        components = filter(lambda x: not inspect.isclass(x), components)
        components.append(self)

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
        self.win_condition = win_condition

    def __getitem__(self, item):
        if isinstance(item, tuple):
            category, name = item
            return self._components[category][name]
        else:
            category, name = item.lstrip(SUBSTITUTION_SYMBOL).split("_", 1)
            # category = category
            return self[(category, name)]

    def get_category(self, category):
        return self._components[category]

    # def run(self):
    #     try:
    #         action = self._flow.run()
    #         # print action
    #     except EndOfCurrentFlow:
    #         raise GameOver()
    #     else:
    #         if action:
    #             action.apply()
    #             visibility = self.expand_visibility(action)
    #             return self.response(action, visibility)
    #         else:
    #             return None

    def run(self):
        try:
            # self.win_condition((self.current_flow, self))
            action = self._flow.run()
            if action:
                try:
                    action.apply()
                except EndOfCurrentFlow:
                    raise EndOfGame()
                else:
                    visibility = self.expand_visibility(action)
                    response = self.response(action, visibility)
                    return {
                        receiver: response_action.make_message()
                        for receiver, response_action in response.iteritems()
                    }
            else:
                return None
        except EndOfGame:
            self.win_condition((None, self))
            raise GameOver()

    @property
    def current_flow(self):
        return self._flow.current_flow()

    def next_stage(self):
        self._flow.next_stage()

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
                player: (player == action.author.name)
                for player in players
            }
        else:
            return {
                player: False
                for player in players
            }

    def response(self, action, visibility):
        players = self.get_category(PLAYER).keys()
        return {
            player: (action.make_visible_response() if visibility[player] else action.make_invisible_response())
            for player in players
        }

    def get_component_by_id(self, id_):
        return self._components_by_id.get(id_)

    def _get_new_id(self):
        res = self._next_id
        self._next_id += 1
        return res

    def make_card(self, card_name, id_=None):
        """
        Ввести карту в игру. Если id карты известен, то он и будет выдан, иначе - сгенерирован
        :param card_name: Название нужной карты
        :type card_name: str
        :param id_: известный id карты
        :type id_: int | None
        :return: Зарегистрированная полная версия карты
        :rtype: core.card.card.Card
        """
        card = self.view_card(card_name)
        self.register_component(card, id_=id_)
        return card

    # def make_component(self, component_name, **kwargs):
    #     """
    #     Создает, но не регистрирует асоциированый с игрой компонент.
    #     :param component_name:
    #     :type component_name:
    #     :param kwargs:
    #     :type kwargs:
    #     :return:
    #     :rtype:
    #     """
    #     return self._components_factories[component_name](**kwargs)

    def view_card(self, card_name):
        """
        Взглянуть на полную версию карты.
        :param card_name: Название интересующей карты
        :type card_name: str
        :return: Полная версия карты
        :rtype: core.card.card.Card
        """
        return self[(TABLE, CARD)][card_name]()

    def register_component(self, component, id_=None):
        # print set(component.categories) & UNINDEXABLE, component.categories, UNINDEXABLE
        if not set(component.categories) & UNINDEXABLE:
            if id_ is None:
                component.id = self._get_new_id()
            else:
                component.id = id_
            self._components_by_id[component.id] = component
        # print component, component.id
        for category in component.categories:
            if component.fullname in self._components[category]:
                raise WTFError()
            else:
                self._components[category][component.fullname] = component
        for associated_component in component.associated_components:
            self.register_component(associated_component)

    def receive_message(self, message):
        """
        Принимает сообщение, передаёт его в парсер, а затем передаёт полученное действие в игровой поток
        """
        if self._mode is SERVER:
            action = self._components[TABLE][GAME_ACTION_TABLE].receive_message(message, self)
            self._flow.receive_action(action)
        elif self._mode is CLIENT:
            action = self._components[TABLE][SYSTEM_ACTION_TABLE].receive_message(message, self)
            action.apply()
        else:
            raise WTFError()
