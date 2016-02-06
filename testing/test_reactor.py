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


class TestReactor(object):

    def __init__(self, game):
        pass
        # self.game = game

    def make_predef(self, log):
        """
        Делает предустановки из лога.
        :param log:
        :return:
        """
        pass

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
          а в случае успеха продолжает выполнение.
        * Если видит точку остановки - переходит в интерактивный режим.
        :return:
        """
        pass

    def _autotest(self, log):
        pass

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


def test(game):         # TODO переписать на argparse
    test_reactor = TestReactor(game)
    try:
        filename = sys.argv[1]
        with open(filename) as f:
            test_reactor.autotest(f)
    except IndexError:
        sys.exit(0)
