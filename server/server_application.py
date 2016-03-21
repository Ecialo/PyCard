# -*- coding: utf-8 -*-
""" Пробуем использовать twisted.application """

import re
import os
import sys
from twisted.application import internet, service

__author__ = 'Anton Korobkov'

# Хак чтобы все нормально импортировалось из корневой папки
def return_root_directory(dirname):
    """
    This one returns 'root path' of the project
    """
    pattern = re.compile(dirname + '.*')
    return re.sub(pattern, dirname, os.getcwd())

sys.path.append(return_root_directory('PyCard'))

from pycard_server import MultiEchoFactory

port = 8000
factory = MultiEchoFactory()

# Просто запустить сервер
application = service.Application("PyCard server")
pycard_listener = internet.TCPServer(port, factory)
pycard_listener.setServiceParent(application)



