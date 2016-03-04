# -*- coding: utf-8 -*-
import collections
from .. import utility as util
from .. import predef
__author__ = 'Ecialo'


def modification(func):
    func.apply = func
    return func


@modification
def set_flag(flag):
    flag.set()


ArgPack = collections.namedtuple('ArgPack', ['category', 'name'])


def action_pipe(target_action_pairs):
    """
    Превращает набор пар цель, действие/модификация в сложное действие
    """
    # TODO сделать приём как коллекций, так и произвольного числа пар
    prev = None
    for target, action in reversed(target_action_pairs):
        if target:
            prev = action(target, prev)
        else:
            prev = action
    return prev


class Action(object):
    """
    Ищет у хозяина свою цель target и применяет к ней действие
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
        for arg, value in kwargs.iteritems():
            if hasattr(self, arg):
                self.__setattr__(arg, value)
                self._args[arg] = value
        return self

    def substitute_enviroment(self, enviroment):    # TODO научиться отличать то что нужно подставлять от того, что нет
        substituted_args = {}
        self._author = enviroment[(predef.PLAYER, self._author)]
        self.game = enviroment
        for argname, argval in self._args.iteritems():
            if isinstance(argval, basestring) and argval.startswith(predef.SUBSTITUTION_SYMBOL):
                category, name = argval.lstrip(predef.SUBSTITUTION_SYMBOL).split("_", 1)
                category = category
                substituted_args[argname] = enviroment[(category, name)]
        self.setup(**substituted_args)

    @property
    def author(self):
        return self._author

    def apply(self):
        return {}

    def __ror__(self, other):
        return ActionPipe(self._author, [other, self])

    def __rand__(self, other):
        return ActionSequence(self._author, [other, self])

    def make_message(self):
        messageable_args = {
            argname: ((predef.SUBSTITUTION_SYMBOL + argval.path) if isinstance(argval, util.Component) else argval)
            for argname, argval in self._args.iteritems()
        }
        return util.make_message(self._author, self.name, **messageable_args)

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

    def make_message(self):
        pass


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
            lambda prev, action: prev.update(action.apply()),
            self,
            {}
        )
