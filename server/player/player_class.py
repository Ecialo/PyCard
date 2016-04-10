# -*- coding: utf-8 -*-
"""
Здесь отдельно будет находиться описание игрока (подсоединяющегося к серверу)
дабы не перегружать функционалом сам сервер
"""

__author__ = 'Anton Korobkov'


class LobbyPerson(object):
    """
    Подсоединяющийся к pycard_server клиент
    """

    def __init__(self, identifier, name):
        """
        На входе принимает те параметры с которыми прилетает коннект
        к серверу от клиента, а именно имя и идентификатор;
        также у игрока есть статус готов/не готов
        """

        self.name = name
        self.identifier = identifier
        self.ready = False

    def get_ready(self):
        """
        Вызвать если клиент жмакает 'готов'
        """
        self.ready = True

    def get_unready(self):
        """
        Вызвать если клиент отменяет готовность
        """
        self.ready = False

    def get_person_data(self):
        """
        Вызвать когда нужно в стороннее место
        скормить аттрибуты этого класса как словарь
        пока возвращает только нужные поля для retard game
        """

        # TODO: fix this hack
        return {'name': self.identifier}

    @property
    def name_getter(self):
        return self.name
