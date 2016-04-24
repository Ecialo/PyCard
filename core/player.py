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
        self._components = collections.defaultdict(dict)
        self._name = name
        for resource in self.available_resources:
            self.register_resource(resource)
        super(Player, self).__init__()

    @property
    def name(self):
        return self._name

    @property
    def resources(self):
        return self._components[predef.RESOURCE]

    @property
    def associated_components(self):
        return self.resources.values()

    def register_resource(self, resource):
        player_resource = resource()
        player_resource.setup_prefix(self._name)
        self._components[predef.RESOURCE][resource.name] = player_resource

    def __eq__(self, other):
        if not other:
            return False
        if isinstance(other, basestring):
            return self.name == other
        else:
            return self.name == other.name

    def __repr__(self):
        return self.name
