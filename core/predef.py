# -*- coding: utf-8 -*-
__author__ = 'Ecialo'
FIRST_PLAYER_TOKEN = 'first player'
PLAYER, DECK, DESK, RESOURCE, HAND, CARD, TABLE, ACTION = (
    'player',
    'deck',
    'desk',
    'resource',
    'hand',
    'card',
    'table',
    'action',
)

GAME_ACTION_TABLE, SYSTEM_ACTION_TABLE = "game_action_table", "system_action_table"
ACTION_JUST, ACTION_SEQUENCE, ACTION_PIPE = xrange(3)

ALL, AUTHOR = "all", "author"

CLIENT, SERVER = xrange(2)

MESSAGE_TYPE_KEY = "type"
MESSAGE_ACTION_KEY = "action"
MESSAGE_AUTHOR_KEY = "author"

SUBSTITUTION_SYMBOL = "!"

SYSTEM = "system"
