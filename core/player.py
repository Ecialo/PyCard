# -*- coding: utf-8 -*-
import collections
import predef
import utility
__author__ = 'Ecialo'


class Player(utility.Component):
    """
    Хранит ассоциированные с игроком данные
    """
    categories = [predef.PLAYER]
    available_resources = []

    def __init__(
            self,
            name
    ):
        # super(Player, self).__init__()
        self._components = collections.defaultdict(dict)
        self._name = name
        for resource in self.available_resources:
            self.register_resource(resource)

    @property
    def name(self):
        return self._name

    @property
    def resources(self):
        return self._components[predef.RESOURCE]

    def register_resource(self, resource):
        player_resource = resource()
        self._components[predef.RESOURCE][resource.name] = player_resource
        player_resource.setup_prefix(self._name)
