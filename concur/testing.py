""" Routines for automated testing.

Must be used in conjunction with the `concur.integrations.puppet` backend.
"""

import imgui
from concur.integrations.puppet import PuppetRenderer, main


def test(widget_gen, slow=False):
    main("Automatic Tester",
        lambda puppet_renderer: widget_gen(Testing(puppet_renderer, slow)),
        500,
        500)


class Testing(object):
    def __init__(self, puppet_renderer, slow):
        assert isinstance(puppet_renderer, PuppetRenderer)
        self.puppet = puppet_renderer
        self.slow = slow

    def click(self, button=0):
        self.puppet.click(button)

    def click_next(self):
        yield from self.slowdown()
        yield
        origin = imgui.get_cursor_screen_pos()
        self.puppet.set_mouse_pos(*origin)
        yield from self.slowdown()
        yield
        self.puppet.click()
        while True:
            yield

    def slowdown(self):
        if self.slow:
            for i in range(30):
                yield
