""" Routines for automated testing. """

import os
import imgui
import numpy as np # for floating point ranges
from concur.integrations.puppet import PuppetRenderer, main
from concur.draw import polyline
from concur.core import orr, optional


def test(widget_gen, slow=False, width=512, height=512, *args, **argv):
    return main("Automatic Tester",
        lambda puppet_renderer: widget_gen(Testing(puppet_renderer, slow)),
        width, height,
        *args, **argv)


def test_widget(f):
    """ Function decorator for testing functions.

    See `concur.testing.test_widget` for usage examples.
    """
    def widget(tester):
        io = imgui.get_io()
        io.mouse_draw_cursor = False
        yield from f(tester)
    def g(*args, **argv):
        return test(widget, *args, **argv)
    return g


class Testing(object):
    """ Must be used in conjunction with the `concur.integrations.puppet` backend. """
    def __init__(self, puppet_renderer, slow):
        assert isinstance(puppet_renderer, PuppetRenderer)
        self.puppet = puppet_renderer
        self.slow = 'SLOW_TEST' in os.environ and os.environ['SLOW_TEST'] == '1'

    def click(self, button=0):
        "Click a given mouse button"
        self.puppet.click(button)

    def click_next(self):
        "Click the next widget"
        x, y = imgui.get_cursor_screen_pos()
        yield from self.move_cursor(x+5, y+5)
        yield from self.pause()
        self.puppet.click()
        while True:
            yield

    def move_cursor(self, x, y):
        "Move cursor to a given position"
        io = imgui.get_io()
        ox, oy = io.mouse_pos
        yield
        if self.slow:
            for f in np.linspace(0, 1, 30):
                self.puppet.set_mouse_pos(x * f + ox * (1-f), y * f + oy * (1-f))
                yield
        else:
            self.puppet.set_mouse_pos(x, y)
            yield

    def scroll_up(self):
        "Scroll up"
        self.puppet.scroll_up()
        yield

    def scroll_dn(self):
        "Scroll down"
        self.puppet.scroll_dn()
        yield

    def mouse_up(self, button=0):
        "Mouse up"
        self.puppet.mouse_up(button)
        yield

    def mouse_dn(self, button=0):
        "Mouse down"
        self.puppet.mouse_dn(button)
        yield

    def pause(self):
        if self.slow:
            for i in range(30):
                yield
        yield
