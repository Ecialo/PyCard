# -*- coding: utf-8 -*-
import collections
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

    def __init__(self, **kwargs):
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

    def substitute_enviroment(self, enviroment):
        substituted_args = {}
        for argname, argval in self._args:
            category, name = argval.split("_", 1)
            category = int(category)
            substituted_args[argname] = enviroment[(category, name)]
        self.setup(**substituted_args)

    def apply(self):
        return {}

    def __ror__(self, other):
        return ActionPipe([other, self])

    def __rand__(self, other):
        return ActionSequence([other, self])

    def make_message(self):
        pass


class ActionCollection(Action):

    def __init__(self, actions=None):
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
