# -*- coding: utf-8 -*-
__author__ = 'ecialo'


def bind_widget(widget):

    def bind(component_cls):

        class ComponentWithWidget(component_cls):

            def make_widget(self, **kwargs):
                return widget(self, **kwargs)

        ComponentWithWidget.__name__ = component_cls.__name__

        return ComponentWithWidget

    return bind