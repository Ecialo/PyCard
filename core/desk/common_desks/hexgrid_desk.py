# -*- coding: utf-8 -*-
from ..desk import Desk
__author__ = 'ecialo'


class HexCell(object):

    def __init__(self, q, r):
        self.q = q
        self.r = r

    def __repr__(self):
        return "HEX({}, {})".format(self.q, self.r)

    def __str__(self):
        return self.__repr__()


class HexgridDesk(Desk):

    cell = HexCell

    def __init__(self, size=(1, 1)):
        super(HexgridDesk, self).__init__()
        self._grid = [[self.cell(q, r) for q in xrange(size[0])] for r in xrange(size[1])]

    def __repr__(self):
        repr_ = []
        for row in self._grid:
            reprow = "|".join(map(str, row))
            repr_.append(reprow)
            repr_.append("-"*len(reprow))
        return "\n".join(repr_)


if __name__ == '__main__':
    print HexgridDesk((10, 10))

