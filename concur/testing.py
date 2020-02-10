""" Routines for automated testing. """

import os
import imgui
import numpy as np # for floating point ranges
from functools import partial
from concur.integrations.puppet import PuppetRenderer, main
from concur.draw import polyline
from concur.core import orr, optional


def test(widget_gen, slow=False, draw_cursor=True, width=512, height=512, *args, **argv):
    return main("Automatic Tester",
        lambda puppet_renderer: widget_gen(draw_cursor, Testing(puppet_renderer, slow)),
        width, height,
        *args, **argv)


def test_widget(f):
    """ Function decorator for testing functions.

    See `concur.testing.test_widget` for usage examples.
    """
    def widget_gen(draw_cursor, tester):
        io = imgui.get_io()
        io.mouse_draw_cursor = draw_cursor
        yield from f(tester)
    def g(*args, **argv):
        draw_cursor = 'draw_cursor' in argv and argv['draw_cursor']
        return test(widget_gen, *args, **argv)
    return g


class Testing(object):
    """ Must be used in conjunction with the `concur.integrations.puppet` backend. """
    def __init__(self, puppet_renderer, slow):
        assert isinstance(puppet_renderer, PuppetRenderer)
        self.puppet = puppet_renderer
        self.slow = 'SLOW_TEST' in os.environ and os.environ['SLOW_TEST'] == '1'
        self.marked = {}

    def click(self, button=0):
        "Click a given mouse button"
        self.puppet.mouse_dn(button)
        if self.slow:
            for i in range(10):
                yield
        yield
        self.puppet.mouse_up(button)

    def click_next(self):
        "Click the next widget"
        x, y = imgui.get_cursor_screen_pos()
        yield from self.move_cursor(x+5, y+5)
        yield from self.pause()
        yield from self.click()
        # Give the widget time to react
        yield
        yield

    def mark(self, name, widget):
        """ Display a widget, but mark it with a name so it can be interacted with at a later point
        using methods such as click_marked. """
        while True:
            self.marked[name] = imgui.get_cursor_screen_pos()
            try:
                next(widget)
            except StopIteration as e:
                return e.value
            yield

    def click_marked(self, name, x=5, y=5):
        "Click the given previously-marked widget. Optionally, specify the click offset x, y coords."
        if name not in self.marked:
            raise ValueError(f"Name '{name}' was not previously marked.")
        x0, y0 = self.marked[name]
        yield from self.move_cursor(x0 + x, y0 + y)
        yield from self.pause()
        yield from self.click()

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

    def set_mouse_pos(self, x, y):
        "Set mouse position instantly."
        self.puppet.set_mouse_pos(x, y)

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

    def pause(self, nframes=0):
        """Pause for a specified number of frames.

        If nframs <= 0, the pause length depends on the
        environment variable TEST_SLOW.
        """
        if nframes <= 0:
            if self.slow:
                for _ in range(30):
                    yield
            yield
        else:
            for _ in range(nframes):
                yield
