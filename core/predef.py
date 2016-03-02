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

(
	ACTION_JUST,
	ACTION_SEQUENCE,
	ACTION_PIPE,
	CHAT_JOIN,
	CHAT_PART,
	CHAT_MESSAGE
) = xrange(6)


ALL, AUTHOR = "all", "author"

CLIENT, SERVER = xrange(2)

MESSAGE_TYPE_KEY = "type"
MESSAGE_PARAMS_KEY = "params"
MESSAGE_ACTION_KEY = "action"
MESSAGE_AUTHOR_KEY = "author"

SUBSTITUTION_SYMBOL = "!"

SYSTEM = "system"

# keys and predefined values related to chat

CHAT_MESSAGE_PRIVATE, CHAT_MESSAGE_BROADCAST = xrange(2)
CHAT_NAME_KEY, CHAT_AUTHOR_KEY, CHAT_MESSAGE_TYPE_KEY, CHAT_TEXT_KEY, CHAT_RECEIVER_KEY = (
	'name',
	'author',
	'message_type',
	'text',
	'receiver'
)