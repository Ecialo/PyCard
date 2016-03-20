# -*- coding: utf-8 -*-
from card import hand
import utility
import predef
__author__ = 'Ecialo'


class Resource(utility.Component):

    categories = [predef.RESOURCE]

    def set(self, value):
        pass

    def clear(self):
        pass


class FlagResource(Resource):

    def __init__(
            self,
            is_active=False
    ):
        super(FlagResource, self).__init__()
        self._active = is_active

    def set(self, value):
        self._active = value

    def clear(self):
        self._active = False


class AmountResource(Resource):

    def __init__(
            self,
            amount=0
    ):
        super(AmountResource, self).__init__()
        self._amount = amount

    def change(self, value=1):
        self._amount += value

    def set(self, value):
        self._amount = value

    def clear(self):
        self.set(0)


class TagResource(Resource):

    def __init__(
            self,
            tag=None
    ):
        super(TagResource, self).__init__()
        self._tag = tag

    def set(self, value):
        self._tag = value


class ParameterResource(Resource):
    pass


class HandResource(Resource, hand.Hand):

    categories = [predef.RESOURCE, predef.HAND]
    name = "hand"
