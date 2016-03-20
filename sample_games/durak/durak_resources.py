# -*- coding: utf-8 -*-
from core import resource
__author__ = 'ecialo'


class Suit(resource.TagResource):
    name = "suit"


class Value(resource.AmountResource):
    name = 'value'