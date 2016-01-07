#! /usr/bin/python
# -*- coding: utf-8 -*-
import PyCard_lib.core.action.action
from PyCard_lib.core import predef
from . import resources
__author__ = 'Ecialo'


class Get(PyCard_lib.core.action.action.Action):

    name = "get"

    def __init__(self):
        super(Get, self).__init__()
        self.category = None
        self.name = None
        self.target = None

    def apply(self):
        return {'target': self.target[self.category][self.name]}


class Set(PyCard_lib.core.action.action.Action):

    name = "set"

    def __init__(self):
        super(Set, self).__init__()
        self.target = None
        self.value = None

    def apply(self):
        self.target.set(self.value)
        return {'target': self.target}


class SelectFirstPlayer(PyCard_lib.core.action.action.Action):

    name = "select_first_player"

    def __init__(self):
        super(SelectFirstPlayer, self).__init__()
        self.game = None
        self.token_path = None

    def apply(self):
        self.game[predef.RESOURCE][self.token_path].set(True)
