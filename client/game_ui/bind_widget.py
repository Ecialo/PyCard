# -*- coding: utf-8 -*-
__author__ = 'ecialo'


def bind_widget(widget):

    def bind(component_cls):

        # class ComponentWithWidget(component_cls):

        def make_widget(self, **kwargs):
            return widget(self, **kwargs)

        component_cls.make_widget = make_widget

        # ComponentWithWidget.__name__ = component_cls.__name__ + "WithWidget"

        return component_cls

    return bind