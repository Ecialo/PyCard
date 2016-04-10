# -*- coding: utf-8 -*-
"""
Это то что запускается когда в лобби (pycard_server)
набирается достаточное число людей
"""

from sample_games.retard_game import retard_game
from server.player.player_class import LobbyPerson

__author__ = 'Anton Korobkov'

# что делаем - берем игроков которые ready и перемещаем их в экземпляр игры в core.game
# потом запускаем создаем методы по переброске на сервер сообщений описываюших что происходит

class ServerGame(object):
    """
    Создать экземпляр класса core.game с заданными параметрами
    """

    def __init__(self, players):
        # Список игроков в сессии - экземпляров класса LobbyPerson
        self.players = players
        self.game_factory()

    def game_factory(self):
        """
        Вызывать для создания объекта игры
        Пока работает только с retard_game
        """
        return retard_game.RetardGame(
            self.players,
        )


def main():
    """
    Потом выпилить, а пока использовать для обезьяньего тестирования
    """
    a = ServerGame([LobbyPerson('1', 'Eustas').get_person_data()])

if __name__ == '__main__':
    main()
