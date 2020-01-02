""" Routines for automated testing.

Must be used in conjunction with the `concur.integrations.puppet` backend.
"""

import imgui
from concur.integrations.puppet import PuppetRenderer, main
from concur.draw import polyline
from concur.core import orr


def test(widget_gen, slow=False):
    main("Automatic Tester",
        lambda puppet_renderer: widget_gen(Testing(puppet_renderer, slow)),
        500,
        500)


def show_cursor():
    io = imgui.get_io()
    while True:
        x, y = io.mouse_pos
        next(polyline([(x, y), (x, y+20), (x+10, y+15)], (1,1,1,1), True, 2))
        yield

class Testing(object):
    def __init__(self, puppet_renderer, slow):
        assert isinstance(puppet_renderer, PuppetRenderer)
        self.puppet = puppet_renderer
        self.slow = slow

    def click(self, button=0):
        self.puppet.click(button)

    def click_next(self):
        def body():
            yield from self.pause()
            x, y = imgui.get_cursor_screen_pos()
            self.puppet.set_mouse_pos(x+5, y+5)
            yield from self.pause()
            self.puppet.click()
            while True:
                yield
        return orr([show_cursor(), body()])

    def pause(self):
        if self.slow:
            for i in range(30):
                yield
        yield
