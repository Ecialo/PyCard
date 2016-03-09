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
from core.game import GameOver
from core import predef


class TestReactor(object):

    def __init__(self, game):
        self.game = game
        self.asserts = {

        }

    @staticmethod
    def _lock_log(log):
        return iter(log)

    def _make_predef(self, log):
        """
        Делает предустановки из лога.
        :param log:
        :return:
        """
        for line in log:
            if line.startswith("---"):
                self.complete_configure()
                return log

    def complete_configure(self):
        """
        Завершает предварительную конфигурацию
        :return:
        """
        pass

    def autotest(self, log):
        """
        Читает лог.
        * Если видит Сообщение, то принимает и исполняет его.
        * Если видит Проверку выполняет её. В случае неуспеха завершается с ошибкой,
          а в случае успеха продолжает выполнение.  Не реализовано.
        * Если видит точку остановки - переходит в интерактивный режим. Не реализовано.
        :return:
        """
        locked_log = self._lock_log(log)
        self._make_predef(locked_log)
        self._autotest(locked_log)

    def _autotest(self, log):
        for line in log:
            if line.startswith(">>>"):   # TODO remove hardcode
                self.game.run()
            elif line.startswith(predef.SUBSTITUTION_SYMBOL):
                self._test_components(line)
            else:
                author, message = line.rstrip().split(" ", 1)
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
                component_1 = self.game[raw_component_1]
                component_2 = (
                    self.game[raw_component_2]
                    if raw_component_2.startswith(predef.SUBSTITUTION_SYMBOL) else
                    eval(raw_component_2)
                )
                self.asserts[assertion](component_1, component_2, line)


def make_test_method(path_to_test_scenario):

    def test_method(self):
        with open(path_to_test_scenario) as test_scenario:
            try:
                self.reactor.autotest(test_scenario)
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
        self.reactor = TestReactor(self.game())
        self.reactor.asserts["=="] = self.assertEqual

    def tearDown(self):
        self.reactor = None


def test(game):         # TODO переписать на argparse
    test_reactor = TestReactor(game)
    try:
        filename = sys.argv[1]
        # print filename
        # print "\n"
        with open(filename) as f:
            test_reactor.autotest(f)
    except IndexError:
        sys.exit(1)
