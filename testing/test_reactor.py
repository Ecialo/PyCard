# -*- coding: utf-8 -*-
"""
Считывает сообщения из лога или ручного ввода, и пропускает их через экземпляр игры.
Служит для упрощения и автоматизации функционального тестирования.

Формат лога/тестового сценария

Предустановки
---
Автор: сообщение | Проверка | Точка остановки
"""

import argparse

import sys
import json
import unittest
import os
import collections as col
from core.game import GameOver
from core import predef

PREDEFS_SCENAIO_SEPARATOR = "---"
NAME = 'name'
AT = "@"


def make_assertion_info_message(assertion_line, **context):
    return "\n".join([
        assertion_line,
        "in context",
        str(context),
    ])



def extract_predefs(log):
    """
    Извлекает предопределённые сценарием параметры.
    :param log:
    :type log:
    :return: Параметры
    :rtype: dict
    """
    params = col.defaultdict(list)
    for line in log:
        if line.startswith(PREDEFS_SCENAIO_SEPARATOR):
            return log, params
        else:
            param = json.loads(line)
            params[param[NAME]].append(param['value'])


class TestReactor(object):
    """
    Прогоняет тестовый сценарий на серверной копии игры.
    """

    def __init__(self, game):
        self.game = game
        self.asserts = {

        }

    def configure(self, params):
        """
        Завершает предварительную конфигурацию
        :return:
        """
        self.game = self.game(**params)

    def autotest(self, log):
        """
        Читает лог.
        * Если видит Сообщение, то принимает и исполняет его.
        * Если видит Проверку выполняет её. В случае неуспеха завершается с ошибкой,
          а в случае успеха продолжает выполнение.  Не реализовано.
        * Если видит точку остановки - переходит в интерактивный режим. Не реализовано.
        :return:
        """
        self._autotest(log)

    def _autotest(self, log):
        for line in log:
            # print line
            if line.startswith(">>>"):   # TODO remove hardcode
                self._run_game()
            elif line.startswith(predef.SUBSTITUTION_SYMBOL):
                self._test_components(line)
            else:
                author, message = line.rstrip().split(" ", 1)
                self._send_message(message)

    def _run_game(self):
        self.game.run()

    def _send_message(self, message):
        self.game.receive_message(message)

    def interactive(self, log=None):
        """
        Работа с реактором и игрой в интерактивном режиме.
        В случае если указан лог можно исполнять записи построчно или перейти в автоматический режим.
        :param log:
        :return:
        """
        pass

    def _interactive(self, log=None):
        pass

    def _test_components(self, line):
        for assertion in self.asserts:
            if assertion in line:
                raw_component_1, raw_component_2 = line.rstrip().split(" " + assertion + " ")
                component_1 = self._parse_component(raw_component_1)
                component_2 = self._parse_component(raw_component_2)

                self.asserts[assertion](
                    component_1,
                    component_2,
                    make_assertion_info_message(
                        line,
                        component_1=component_1,
                        component_2=component_2,
                    )
                )

    def _parse_component(self, raw_component):
        is_path = predef.SUBSTITUTION_SYMBOL in raw_component
        with_address = AT in raw_component
        if is_path:
            if with_address:
                path, _ = raw_component.split(AT)
            else:
                path = raw_component
            return self.game[path]
        else:
            return eval(raw_component)


class FullTestReactor(TestReactor):
    """
    Прогоняет тестовый сценарий на серверной копии игры, но так же отслеживает состояние клиентских частей.
    """
    def __init__(self, game):
        super(FullTestReactor, self).__init__(game)
        self.clients = {}

    def configure(self, params):
        players = params['players']
        for player in players:
            self.clients[player['name']] = self.game(
                mode=predef.CLIENT,
                **params
            )
        self.clients[predef.SYSTEM] = self.game(**params)

    def _run_game(self):
        response = self.clients[predef.SYSTEM].run()
        if response:
            for receiver, message in response.iteritems():
                self.clients[receiver].receive_message(message)

    def _send_message(self, message):
        self.clients[predef.SYSTEM].receive_message(message)

    def _parse_component(self, raw_component):
        is_path = predef.SUBSTITUTION_SYMBOL in raw_component
        with_address = AT in raw_component
        if is_path:
            if with_address:
                path, address = raw_component.split(AT)
            else:
                path, address = raw_component, predef.SYSTEM
            # print "\n\n\n", address
            return self.clients[address][path]
        else:
            return eval(raw_component)


def make_test_method(path_to_test_scenario):

    def test_method(self):
        with open(path_to_test_scenario) as test_scenario:
            try:
                scenario = iter(test_scenario)
                log, params = extract_predefs(scenario)
                self.reactor.configure(params)
                self.reactor.autotest(log)
            except GameOver:
                pass

    return test_method


class TestGameMeta(type):

    def __new__(cls, name, bases, dct):
        # print dct
        if dct.get('path_to_scenarios') is not None:
            top = dct['path_to_scenarios']
            # print "\n\n\n", top, "\n\n\n"

            new_test_methods = {}
            for dirpath, dirnames, filenames in os.walk(top):
                for filename in filenames:
                    testname = "test" + filename
                    new_test_methods[testname] = make_test_method(os.path.join(dirpath, filename))
            dct.update(new_test_methods)
        return super(TestGameMeta, cls).__new__(cls, name, bases, dct)


class TestGame(unittest.TestCase):

    __metaclass__ = TestGameMeta
    game = None
    path_to_scenarios = None

    def setUp(self):
        self.reactor = FullTestReactor(self.game)
        self.reactor.asserts["=="] = self.assertEqual

    def tearDown(self):
        self.reactor = None


def test(game):         # TODO переписать на argparse
    test_reactor = FullTestReactor(game)
    try:
        filename = sys.argv[1]
        # print filename
        # print "\n"
        # with open(filename) as f:
        #     test_reactor.autotest(f)
        with open(filename) as test_scenario:
            # try:
                scenario = iter(test_scenario)
                log, params = extract_predefs(scenario)
                test_reactor.configure(params)
                test_reactor.autotest(log)
            # except GameOver:
            #     pass
    except IndexError:
        sys.exit(1)
