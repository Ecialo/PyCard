# -*- coding: utf-8 -*-
import collections
from .. import utility
from .. import predef
__author__ = 'Ecialo'


class Card(utility.Component):

    categories = [predef.CARD]
    back = predef.CARD_BACK
    description = ""
    available_resources = []
    available_actions = {}

    def __init__(self):
        self._current_context = predef.HAND_CONTEXT
        self._back = None
        self._components = collections.defaultdict(dict)

        for resource in self.available_resources:
            self.register_resource(resource)
        super(Card, self).__init__()

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

    def get_current_available_actions(self):
        return map(
            lambda action: action.setup(source=self),
            self.available_actions[self._current_context.name]
        )

    def change_context(self, context):
        self._current_context = context

    def __eq__(self, other):
        return other is not None and self.name == other.name

