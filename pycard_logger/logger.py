#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Попробуем для PyCard сделать отдельное логгирование
"""

import json
__author__ = 'Anton Korobkov'


class PyCardLogger(object):

    #TODO: move default path to predef
    def __init__(self, filename='log.txt'):

        if not filename:
            raise Exception('Log destination is not specified')

        self.filename = filename

    #TODO: move type names to predef
    def __call__(self, message, type='action'):
        if type == 'action':
            self.write_action(message)
        else:
            raise NotImplementedError()


    def write_action(self, msg):
        with open(self.filename, 'a') as f:
            f.write(': '.join([json.loads(msg)["params"]["author"], msg]) + '\n')



