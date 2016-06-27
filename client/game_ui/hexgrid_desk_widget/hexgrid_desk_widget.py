# -*- coding: utf-8 -*-
import kivy
from kivy.uix import (
    layout
)
import kivy.uix.boxlayout as blayout

from kivy.lang import Builder
import kivy.uix.widget as widget
from kivy.uix import (
    relativelayout,
)
from kivy.properties import (
    ListProperty,
    ObjectProperty,
    NumericProperty,
    BooleanProperty,
)
from kivy.graphics import Mesh, Color, Translate
from math import cos, sin, pi, sqrt
import random as rnd
__author__ = 'ecialo'
H_COEF = sqrt(3)/2

Builder.load_file('./hexgrid_desk_widget.kv')


class HexCellWidget(relativelayout.RelativeLayout):

    mesh_vertices = ListProperty([])
    mesh_texture = ObjectProperty(None)
    hex_size = NumericProperty(40)
    is_selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        pos = self.grid_to_widget(kwargs['pos'])
        kwargs['pos'] = pos
        super(HexCellWidget, self).__init__(**kwargs)
        self.update_vertices()
        self.mesh_texture = kwargs['texture'].texture
        # self
        # with self.canvas:
        #     Mesh(
        #         vertices=self.mesh_vertices,
        #         indices=range(6),
        #         texture=self.mesh_texture,
        #         mode='triangle_fan'
        #     )
        #     Color(1, 0, 0, 1)
        #     Mesh(
        #         vertices=self.mesh_vertices,
        #         indices=range(6),
        #         mode='line_loop'
        #     )

    def update_vertices(self):
        vertices = []
        # indices = []
        step = 6
        istep = (pi * 2) / float(step)
        # xx, yy = self.pos
        for i in xrange(step):
            x = cos(istep * i) * self.hex_size
            y = sin(istep * i) * self.hex_size
            vertices.extend([x, y, 0.5 + cos(istep * i)/2, 0.5 + sin(istep * i)/2])
            # indices.append(i)
        # print id(self.mesh_vertices)
        self.mesh_vertices = vertices

    def grid_to_widget(self, pos):
        size = self.hex_size
        col, row = pos
        x = size * 3/2 * col
        y = size * sqrt(3) * (row - 0.5 * (col & 1))
        # x, y = 300 + rnd.randint(-10, 10)*10, 300 + rnd.randint(-10, 10)*10
        # print x, y
        return x, y

    def on_touch_down(self, touch):
        ret = False
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if self.collide_point(*touch.pos):
            self.is_selected = not self.is_selected
            ret = True
        touch.pop()
        return ret

    def collide_point(self, x, y):
        return sqrt(x*x + y*y) <= sqrt(3)/2*self.hex_size


class HexgridDeskWidget(relativelayout.RelativeLayout):

    cell_indices = range(6)
    cell_size = 40

    def __init__(self, **kwargs):
        super(HexgridDeskWidget, self).__init__(**kwargs)
        hexgrid = kwargs['hexgrid']
        # self.hex_size = 100
        # self.texture = kwargs['texture']
        self.hexgrid = hexgrid
        w, h = len(hexgrid), len(hexgrid[0])
        self._grid = [
            [HexCellWidget(pos=(i, j), texture=hexgrid[i][j].texture, is_selected=hexgrid[i][j].is_selected) for j in xrange(h)] for i in xrange(w)]
        for column in self._grid:
            for cell in column:
                self.add_widget(cell)
                # cell.update_vertices()
                print cell.mesh_vertices[:2:]
        #         print id(cell.mesh_vertices)
        for child in self.children:
            print child.pos
        # print [map(id, col) for col in self._grid]
        # with self.canvas:

    # def on_touch_down(self, touch):
    #     touch.push()
    #     touch.apply_transform_2d(self.to_local)
    #
    #     size = self.cell_size
    #     x, y = touch.pos
    #     q = x * 2.0/3.0 / float(size)
    #     r = (-x / 3.0 + sqrt(3.0)/3.0 * y) / float(size)
    #     # print x, y
    #     print x, y, q, r
    #     good = (0 < q < 11) and (0 < r < 11)
    #     if good:
    #         # cell = self._grid[int(q)][int(r)]
    #         cell = self._grid[int(r)][int(q)]
    #         cell.is_selected = not cell.is_selected
    #     touch.pop()
    #     return good
        # function pixel_to_hex(x, y):
        # return hex_round(Hex(q, r))

    # def collide_point(self, x, y):
    #     pass


if __name__ == '__main__':
    # from core.desk.common_desks import hexgrid_desk as hgd
    # from client.tools import bind_widget
    from kivy.app import App
    from kivy.core.image import Image as CoreImage
    from kivy.uix.image import Image
    texture = CoreImage('/home/ecialo/grass.png')

    class CellMock(object):

        def __init__(self, i, j, texture_, is_selected=False):
            self.i = i
            self.j = j
            self.texture = texture_
            self.is_selected = is_selected

    # grid = [[CellMock(0, 0, texture)]]
    h, w = 11, 11
    grid = [[CellMock(i, j, texture, i == 0 and j == 0) for j in xrange(h)] for i in xrange(w)]

    class TestApp(App):

        def build(self):
            wid = widget.Widget()
            # return wid
            # desk = hgd.HexgridDesk((20, 20))
            # desk_widget = desk.make_widget()
            # cell = HexCellWidget(texture=texture, pos=(300, 300))
            grid_ = HexgridDeskWidget(hexgrid=grid, pos=(40, 40))
            wid.add_widget(grid_)
            return wid
            # return desk_widget

    TestApp().run()
