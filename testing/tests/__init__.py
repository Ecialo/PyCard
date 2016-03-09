# -*- coding: utf-8 -*-
import unittest
import retard_game
__author__ = 'ecialo'

test_suit = unittest.TestSuite(
    [unittest.makeSuite(retard_game.TestRetardGame)]
)