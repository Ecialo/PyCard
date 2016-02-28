# -*- coding: utf-8 -*-
import random as rnd
import operator as op
from ..predef import FIRST_PLAYER_TOKEN
from ..predef import PLAYER
from condition import CyclesExceedCondition
from .. import utility
from ..action.common_actions import next_stage

__author__ = 'Ecialo'


class EndOfCurrentFlow(Exception):
    pass


class Flow(object):
    """
    Описывает как именно идёт игра, чей сейчас ход и прочее.
    Каждое выполненое действие возвращает сообщение(преобразуемой в дальнейшем в action) с содержанием того как именно обновлять клиеты в связи с событием.
    Если действие не удалось - возврашает None и ждёт новой попытки
    event - это flow, который просходит разово и вне очереди.
    Если текущий flow закончен, то бросается исключение EndOfCurrentFlow
    """
    flow = None
    associated_components = []

    def __init__(
            self,
            game
    ):
        if self.flow:
            self._flow = [flow(game) for flow in self.flow]
        self._event = None
        self._game = game
        self._i = 0
        try:
            self._l = len(self._flow)
        except:         # TODO Уточнить ошибку
            self._l = 0

    # def run(self):
    #     """
    #     Запускаем текущий flow. Если есть сообытие - запускаем его.
    #     Если он закончился делаем текущим следующий и запускаем его.
    #     Если текущего нет - мы закончились.
    #     """
    #     if self._event:
    #         try:
    #             action = self._event.run()
    #         except EndOfCurrentFlow:
    #             self._event = None
    #             action = self.run()
    #     elif self._i >= self._l:
    #         raise EndOfCurrentFlow()
    #     else:
    #         current_flow = self._flow[self._i]
    #         try:
    #             action = current_flow.run()
    #         except EndOfCurrentFlow:
    #             self._i += 1
    #             action = self.run()
    #     return action

    def current_flow(self):
        if self._event:
            return self._event
        else:
            if self._i >= self._l:
                raise EndOfCurrentFlow()
            else:
                return self._flow[self._i].current_flow()

    def next_stage(self):
        if self._event:
            self._event = None
        else:
            try:
                self.current_flow().next_stage()
            except EndOfCurrentFlow:
                self._i += 1

    def run(self):
        try:
            return self.current_flow().run()
        except EndOfCurrentFlow:
            return next_stage.NextStage(game=self._game)

    def raise_event(self, flow):
        if self._event:
            self._event.raise_event(flow)
        else:
            self._event = flow

    @property
    def stage(self):
        return self._i

    def get_all_associated_components(self):
        return (
            self.associated_components +
            reduce(op.add, self.flow.get_all_associated_components()) if self.flow else []
        )

    def receive_action(self, action):
        pass


class Cycle(Flow):
    """
    Повторяет последовательность flow, до выполнения условий
    """
    condition = None

    def __init__(
            self,
            game
    ):
        super(Cycle, self).__init__(game)
        self._cycles = 0

    def next_stage(self):
        super(Cycle, self).next_stage()
        if self._i >= self._l:
            self._i %= self._l
            self._cycles += 1
        if self.condition((self, self._game)):
            raise EndOfCurrentFlow()

    # def run(self):
    #     if self._i >= self._l:
    #         self._i %= self._l
    #         self._cycles += 1
    #     if self.condition((self, self._game)):
    #         raise EndOfCurrentFlow()
    #     return super(Cycle, self).run()

    @property
    def cycles(self):
        return self._cycles


class SelectFirstPlayerAtRandom(Cycle):
    """
    Случайным образом выбирает первого игрока.
    """

    condition = CyclesExceedCondition(1)

    def run(self):
        super(SelectFirstPlayerAtRandom, self).run()
        first_player = rnd.choice(self._game)
        first_player_token = first_player.resources[FIRST_PLAYER_TOKEN].fullname
        return utility.make_message('select_first_player', token_path=first_player_token)


class TurnCycle(Cycle):
    """
    Заставляет игроков ходить в цикле до выполнения условия
    """

    turn = None

    def __init__(
            self,
            game
    ):
        self._flow = [self.turn(player) for player in game.get_category(PLAYER)]
        super(TurnCycle, self).__init__(game)

    def receive_action(self, action):
        self._flow[self.stage].receive_action(action)
