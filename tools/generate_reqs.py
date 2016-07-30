#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Тулза для автоматической генерации requirements.txt
и установки зависимостей
запускать от администратора
"""

from subprocess import call

__author__ = 'Anton Korobkov'

# check if 'pipreqs' exists, if not install

try:
    import pipreqs
except ImportError:
    call(["pip2.7", "install", "pipreqs"])

# generate 'requirements.txt'
call(["pipreqs", "--force", ".."])

# install dependencies
call(["pip2.7", "install", "-r", "../requirements.txt"])


