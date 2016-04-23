# -*- coding: utf-8 -*-
import unittest
from core.utility import check_pycard_protocol

__author__ = 'ecialo'


class TestProtocolChecker(unittest.TestCase):

    def testActionJustValidMessage(self):
        message = '{"params": {"action": {"draw_cards": {"source": "!deck_retard_deck_0", "number": 1, "target": "!resource_Eustace_hand_1"}}, "author": "Eustace"}, "type": 0}'
        self.assertTrue(check_pycard_protocol(message))

    def testActionJustValidStruct(self):
        struct = {
            "params": {
                "action": {
                    "draw_cards": {
                        "source": "!deck_retard_deck_0",
                        "number": 1,
                        "target": "!resource_Eustace_hand_1"
                    }
                },
                "author": "Eustace"
            },
            "type": 0
        }
        self.assertTrue(check_pycard_protocol(struct))

    def testActionJustInvalidMessage(self):
        message = '{"params": {"action": {"draw_cards": {"source": "!deck_retard_deck_0", "number": 1, "target": "!resource_Eustace_hand_1"}}, "author": "Eustace"}, "type": "0"}'
        self.assertFalse(check_pycard_protocol(message))

    def testActionJustInvalidStruct(self):
        struct = {
            "params": {
                "action": {
                    "draw_cards": {
                        "source": "!deck_retard_deck_0",
                        "number": 1,
                        "target": "!resource_Eustace_hand_1"
                    }
                },
                "author": "Eustace"
            },
            "type": "0"
        }
        self.assertFalse(check_pycard_protocol(struct))
