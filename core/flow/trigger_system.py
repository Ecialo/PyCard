# -*- coding: utf-8 -*-
from collections import defaultdict
__author__ = 'ecialo'


class Trigger(object):

    def __init__(self, on_action, action, conditions):
        self.on_action = on_action
        self._conditions = conditions
        self._action = action

    def launch_with(self, action):
        self._action.setup(action=action)
        self._action.apply()

    def check(self, action):
        return all(condition(action) for condition in self._conditions)


class TriggerSystem(object):

    def __init__(self):
        self._pre_action_triggers = defaultdict(list)
        self._post_action_triggers = defaultdict(list)

    def register_pre_action_trigger(self, trigger):
        self._pre_action_triggers[trigger.on_action].append(trigger)

    def register_post_action_trigger(self, trigger):
        self._post_action_triggers[trigger.on_action].append(trigger)

    @staticmethod
    def _find_and_launch_triggers(action, triggers):
        for trigger in triggers:
            if trigger.check(action):
                trigger.launch_with(action)

    def apply_with_triggers(self, action):
        self._find_and_launch_triggers(action, self._pre_action_triggers[action.name])
        action.apply()
        self._find_and_launch_triggers(action, self._post_action_triggers[action.name])
        return action
