# -*- coding: utf-8 -*-
__author__ = 'Ecialo'
FIRST_PLAYER_TOKEN = 'first player'
PLAYER, DECK, DESK, RESOURCE, HAND, CARD, TABLE, ACTION, GAME = (
    'player',
    'deck',
    'desk',
    'resource',
    'hand',
    'card',
    'table',
    'action',
    'game',
)

GAME_ACTION_TABLE, SYSTEM_ACTION_TABLE = "game_action_table", "system_action_table"
UNINDEXABLE = {PLAYER, TABLE}
ACTION_JUST, ACTION_SEQUENCE, ACTION_PIPE = xrange(3)

(
    ACTION_JUST,
    ACTION_SEQUENCE,
    ACTION_PIPE,
    CHAT_REGISTER,
    CHAT_JOIN,
    CHAT_PART,
    CHAT_MESSAGE,
    LOBBY_READY,
    LOBBY_NOT_READY,
    LOBBY_ALL_READY,
    LOBBY_START_GAME,
    LOBBY_NAME_ALREADY_EXISTS
) = xrange(12)
CARD_BACK = "back"

ALL, AUTHOR = "all", "author"

CLIENT, SERVER = xrange(2)

MESSAGE_TYPE_KEY = "type"
MESSAGE_PARAMS_KEY = "params"
MESSAGE_ACTION_KEY = "action"
MESSAGE_AUTHOR_KEY = "author"

SUBSTITUTION_SYMBOL = "!"

HAND_CONTEXT = HAND

SYSTEM = "system"

# keys and predefined values related to chat

CHAT_MESSAGE_PRIVATE, CHAT_MESSAGE_BROADCAST = xrange(2)

CHAT_NAME_KEY, CHAT_NAMES_KEY, CHAT_MESSAGE_TYPE_KEY, CHAT_TEXT_KEY, CHAT_RECEIVER_KEY, \
CHAT_PLAYER_ID_KEY = (
    'name',
    'names',
    'message_type',
    'text',
    'receiver',
    'player_id'
)
