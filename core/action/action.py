# -*- coding: utf-8 -*-
import collections
from .. import utility as util
from .. import predef
__author__ = 'Ecialo'

ArgPack = collections.namedtuple('ArgPack', ['category', 'name'])


class Action(object):
    """
    Отложенная мутация над игрой или её компонентами.

    Не стоит обновлять параметры чем-то кроме метода setup.

    :ivar name: название Действия, по которому оно идентифицируется в Таблице действий
    :type name: str
    :ivar default_args: аргументы по умолчанию для этого действия
    :type default_args: dict[str, T]
    """
    name = None
    default_args = {}
    visibility = None       # all | author

    def __init__(self, author=predef.SYSTEM, **kwargs):
        self._author = author

        self.game = None
        self._args = {}

        args = self.default_args.copy()
        args.update(kwargs)

        self.setup(**args)

    def setup(self, **kwargs):
        """
        Правильный способ обновить внутренние параметы.

        :param kwargs:
        :return: Action
        """
        for arg, value in kwargs.iteritems():
            if hasattr(self, arg):
                self.__setattr__(arg, value)
                self._args[arg] = value
        return self

    def substitute_enviroment(self, environment):
        """
        Заменить пути до компонентов (начинается с SUBSTITUTION_SYMBOL) компонентами из окружения.

        :param environment: Игра в которой происходит действие
        :type environment: core.game.Game
        :return:
        """
        substituted_args = {}
        self._author = environment[(predef.PLAYER, self._author)] if self._author != predef.SYSTEM else environment
        self.game = environment
        for argname, argval in self._args.iteritems():
            if isinstance(argval, basestring) and argval.startswith(predef.SUBSTITUTION_SYMBOL):
                # category, name = argval.lstrip(predef.SUBSTITUTION_SYMBOL).split("_", 1)
                # category = category
                substituted_args[argname] = environment[argval]
        self.setup(**substituted_args)

    @property
    def author(self):
        return self._author

    def apply(self):
        """
        Применить мутацию.

        :return: Параметры, которые возможно будут нужны другой мутации
        :rtype: dict[str, T] | None
        """
        return None

    def check(self):
        """
        Проверяет возможно ли выполнить данное действие. По умолчанию любое действие можно выполнить.
        :return: Возможно ли выполнить действие
        :rtype: bool
        """
        return True

    def __ror__(self, other):
        return ActionPipe(self._author, [other, self])

    def __rand__(self, other):
        return ActionSequence(self._author, [other, self])

    def get_message_struct(self):
        messageable_args = {
            argname: ((predef.SUBSTITUTION_SYMBOL + argval.path) if isinstance(argval, util.Component) else argval)
            for argname, argval in self._args.iteritems()
        }
        return {self.name: messageable_args}

    def make_message(self):
        """
        Создает на основе действия json строку сообщения. Сообщение имеет следующий формат:
        {
            MESSAGE_TYPE_KEY: ACTION_JUST | ACTION_SEQUENCE | ACTION_PIPE
            MESSAGE_ACTION_KEY: {arg: val} | [{arg: val}]
        }
        Если val - это компонент, то он представляется виде внутриигрового пути до него.

        :return: json строка с сообщением
        :rtype: str
        """
        messageable_struct = self.get_message_struct()
        return util.make_message(self._author, messageable_struct)

    def make_visible_response(self):
        pass

    def make_invisible_response(self):
        pass


class ActionCollection(Action):

    def __init__(self, author, actions=None):
        self._author = author
        self._actions = collections.deque(actions) or collections.deque()

    def __iter__(self):
        for action in self._actions:
            yield action

    def substitute_enviroment(self, environment):
        for action in self._actions:
            action.substitute_enviroment(environment)


class ActionPipe(ActionCollection):

    def __or__(self, other):
        if isinstance(other, ActionPipe):
            self._actions.extend(other)
        else:
            self._actions.append(other)
        return self

    def __ror__(self, other):
        self._actions.appendleft(other)
        return self

    def apply(self):
        return reduce(
            lambda prev, action: action.setup(**prev).apply(),
            self,
            {}
        )

    def make_message(self):
        return util.make_pipe_message(
            self._author,
            *[action.get_message_struct() for action in self._actions]
        )


class ActionSequence(ActionCollection):

    def __and__(self, other):
        if isinstance(other, ActionPipe):
            self._actions.extend(other)
        else:
            self._actions.append(other)
        return self

    def __rand__(self, other):
        self._actions.appendleft(other)
        return self

    def apply(self):
        return reduce(
            lambda _, action: action.apply(),
            self,
        )

    def make_message(self):
        return util.make_sequence_message(
            self._author,
            *[action.get_message_struct() for action in self._actions]
        )
