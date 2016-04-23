# -*- coding: utf-8 -*-
import unittest
import retard_game
import protocol_checker
__author__ = 'ecialo'

test_suit = unittest.TestSuite(
    [
        unittest.makeSuite(retard_game.TestRetardGame),
        unittest.makeSuite(protocol_checker.TestProtocolChecker),
    ]
)
