# -*- coding: utf-8 -*-
import inspect
__author__ = 'ecialo'


# def property_hack(getter):
#
#     def new_getter(self, item):
#         v = getter(self, item)
#         event_name = "on_" + item
#         # if (
#         #         hasattr(self, "_widget")
#         #         and not item.startswith("_")
#         #         and hasattr(self._widget, item)
#         #         and inspect.ismethod(v)
#         # ):
#         #     return getattr(self._widget, item)
#         # else:
#         #     return v
#         if (
#                 hasattr(self, "_widget")
#                 and not item.startswith("_")
#                 and hasattr(self._widget, event_name)
#                 and inspect.ismethod(v)
#         ):
#             print "\n\n\n123\n\n\n"
#             self._widget.dispatch(event_name)
#         return v
#
#     return new_getter


def property_hook(method):

    event_name = "on_" + method.__name__

    def hooked(self, *args, **kwargs):
        method(self, *args, **kwargs)
        if (
                hasattr(self, "_widget")
                and hasattr(self._widget, event_name)
        ):
            self._widget.dispatch(event_name, *args, **kwargs)

    return hooked


def bind_widget(widget):

    def bind(component_cls):
        # Всё что ниже конченная жесть.
        # Я очень надеюсь, что мы придумаем что-нибудь поумнее для связи с виджетами.
        def make_widget(self, **kwargs):
            if not hasattr(self, '_widget') or not self._widget:
                self._widget = widget(self, **kwargs)
            return self._widget

        component_cls.make_widget = make_widget
        for method_name in component_cls.hooks:
            setattr(
                component_cls,
                method_name,
                property_hook(getattr(
                    component_cls,
                    method_name
                ))
            )

        # ComponentWithWidget.__name__ = component_cls.__name__ + "WithWidget"

        return component_cls

    return bind
