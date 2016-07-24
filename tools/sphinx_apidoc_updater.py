#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Автоматически пересоздает все .rst
файлы и обновляет контент
"""

from argparse import ArgumentParser
from subprocess import call
import os

__author__ = 'Anton Korobkov'

# Дефолтный путь к докам
docpath = os.path.join(os.path.abspath('..'), 'docs')


def get_args():
    """
    Возвращает переданные аргументы
    командной строки
    предполагается что директория с доками
    лежит в корне проекта
    :return:
    """

    parser = ArgumentParser(
        description='Run to remake PyCard documentation structure'
    )

    parser.add_argument(
        '-V', '--version', type=str, help='Project version (sphinx arg)', required=False, default='0.01'
    )

    parser.add_argument(
        '-R', '--releasenum', type=str, help='Project release (sphinx arg)', required=False, default='0'
    )

    parser.add_argument(
        '-o', '--oupputdir', type=str,
        help='Directory to place the output files. If it does not exist, it is created (sphinx arg)',
        required=False, default=docpath
    )

    parser.add_argument(
        '-s', '--sourcedir', type=str, help='Project source directory', required=False,
        default=docpath.replace('/docs', '')
    )

    args = parser.parse_args()

    version, releasenum, outdir, sourse = args.version, args.releasenum, \
                                                            args.oupputdir, args.sourcedir

    return version, releasenum, outdir, sourse

def delete_rst(docs):
    """

    :param docs: Путь к директории с доками
    :return:
    """
    for filename in os.listdir(docs):
        if filename.endswith('.rst') is True:
            os.remove(os.path.join(docpath, filename))


def main():
    version, releasenum, outdir, sourse = get_args()
    delete_rst(outdir)
    call(["sphinx-apidoc", "-F", "-H", "PyCard", "-A", "PyCard team", "-V", version, "-R", releasenum, "-o", outdir,
          sourse])
    os.chdir(outdir)
    # TODO: понять, почему не собирается с первого раза
    for i in xrange(2):
        call(["make", "html"])


if __name__ == "__main__":
    main()

