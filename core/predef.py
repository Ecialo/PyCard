# -*- coding: utf-8 -*-
__author__ = 'Ecialo'


class Namespace(object):

    def __init__(self, **consts):
        for const_name, const_val in consts.iteritems():
            setattr(self, const_name, const_val)

    def __repr__(self):
        return "\n".join(map(lambda name_val: "{0} = {1}".format(name_val[0], name_val[1]), self.items()))

    def values(self):
        return self.__dict__.itervalues()

    def names(self):
        return self.__dict__.iterkeys()

    def items(self):
        return self.__dict__.iteritems()


class Enum(Namespace):

    def __init__(self, *consts):
        for const_name, const_val in zip(consts, xrange(len(consts))):
            setattr(self, const_name, const_val)


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
UNINDEXABLE = {PLAYER, TABLE}

game_component_types = Namespace(
    PLAYER='player',
    DECK='deck',
    DESK='desk',
    RESOURCE='resource',
    HAND='hand',
    CARD='card',
    TABLE='table',
    ACTION='action',
    GAME='game'
)
game_component_types.UNINDEXABLE = {game_component_types.PLAYER, game_component_types.TABLE}


GAME_ACTION_TABLE, SYSTEM_ACTION_TABLE = "game_action_table", "system_action_table"

table_type = Namespace(
    GAME_ACTION_TABLE="game_action_table",
    SYSTEM_ACTION_TABLE="system_action_table",
)


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
MESSAGE_TYPE_KEY = "type"
MESSAGE_PARAMS_KEY = "params"
MESSAGE_ACTION_KEY = "action"
MESSAGE_AUTHOR_KEY = "author"

pycard_protocol = Namespace(
    event_types=Enum(
        "ACTION_JUST",
        "ACTION_SEQUENCE",
        "ACTION_PIPE",
        "CHAT_REGISTER",
        "CHAT_JOIN",
        "CHAT_PART",
        "CHAT_MESSAGE",
        "LOBBY_READY",
        "LOBBY_NOT_READY",
        "LOBBY_ALL_READY",
        "LOBBY_START_GAME",
        "LOBBY_NAME_ALREADY_EXISTS",
    ),
    message_struct=Namespace(
        MESSAGE_TYPE_KEY="type",
        MESSAGE_PARAMS_KEY="params",
        MESSAGE_ACTION_KEY="action",
        MESSAGE_AUTHOR_KEY="author",
    ),
)


CARD_BACK = "back"

ALL, AUTHOR = "all", "author"

CLIENT, SERVER = xrange(2)

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


# UI
CARD_FROM_OUR_HAND, CARD_FROM_ANOTHER_HAND, CARD_FROM_DECK, CARD_FROM_DESK = xrange(4)

ui = Enum(
    "CARD_FROM_OUR_HAND",
    "CARD_FROM_ANOTHER_HAND",
    "CARD_FROM_DECK",
    "CARD_FROM_DESK",
)

if __name__ == '__main__':
    print Namespace(ololo=3, kokoko=4)
    print Enum('ololo', 'kokoko')
    print Namespace(ololo=3, kokoko=4).ololo
    a = Namespace()
    a.qqqq = "11311"
    print a