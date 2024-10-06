""" Routines for automated testing.

The current automation/testing setup is work-in-progress, and the interface may change radically
in future versions. There are some usability issues that I am not entirely happy with.

See the [tests directory](https://github.com/potocpav/python-concur/tree/master/tests) for usage examples.
"""


import os
import imgui
import numpy as np  # for floating point ranges
from functools import partial
from concur.integrations.puppet import PuppetRenderer, main
from concur.draw import polyline
from concur.core import orr, optional
import concur.widgets


__pdoc__ = dict(test=False)


def test(widget_gen, slow=None, draw_cursor=True, width=512, height=512, *args, **argv):
    return main(
        lambda puppet_renderer: widget_gen(draw_cursor, Testing(puppet_renderer, slow)),
        "Automatic Tester",
        width, height,
        *args, **argv)


def test_widget(f):
    """ Function decorator for testing functions.

    Dead simple usage example, which just displays a button for a moment is:

    ```python
    @c.testing.test_widget
    def test_example(tester):
        yield from c.orr([c.button("Test Button"), tester.pause()])

    if __name__ == '__main__':
        test_example()
    ```

    This can be invoked either directly (`python test_example.py`), or using PyTest (`pytest -k test_example`).
    To slow the test down, set the environmental variable `SLOW_TEST=1`:
    ```bash
    SLOW_TEST=1 python test_example.py
    # or
    SLOW_TEST=1 pytest -k test_example
    ```

    The decorated testing function takes a single argument `tester`, which contains a `Testing` class instance.
    This class provides convenient functions for user input automation, wrapping the raw user interaction
    primitives from `concur.integrations.puppet.PuppetRenderer`.
    """
    def widget_gen(draw_cursor, tester):
        io = imgui.get_io()
        io.mouse_draw_cursor = draw_cursor
        # FIXME: Nesting everything inside a window here can lead to nested windows, if `f` contains a window as well.
        yield from window(f(tester))

    def g(*args, **argv):
        draw_cursor = 'draw_cursor' in argv and argv['draw_cursor']
        return test(widget_gen, *args, **argv)

    return g


def benchmark_widget(f_gen):
    """ Benchmark a widget (experimental).

    See tests/test_draw.py for example usage.
    """
    f = f_gen()

    def widget(_):
        for _ in range(240):
            next(f)
            yield

    def g(benchmark):
        benchmark.pedantic(main, (widget, "Perf Tester", 512, 512), dict(fps=None), rounds=1)

    return g


def window(widget):
    # NOTE: for events to register, all widgets must be inside a window.
    # This is not the case with the ImGui Docking branch. There, windows don't need to be created in tests.
    return concur.widgets.window("Window", widget, position=(5, 5), size=(500, 500))


class Testing(object):
    """ Must be used in conjunction with the `concur.integrations.puppet` backend.

    To setup all the plumbing effortlessly, use the `test_widget` decorator.

    All the methods in this class are widgets, and they can be composed as usual using
    `concur.core.orr`, `yield from`, and friends.
    """
    def __init__(self, puppet_renderer, slow=None):
        assert isinstance(puppet_renderer, PuppetRenderer)
        self.puppet = puppet_renderer
        if slow is None:
            self.slow = 'SLOW_TEST' in os.environ and os.environ['SLOW_TEST'] == '1'
        else:
            self.slow = slow
        self.marked = {}

    def click(self, button=0):
        "Click a given mouse button."
        self.puppet.mouse_dn(button)
        if self.slow:
            for i in range(10):
                yield
        yield
        self.puppet.mouse_up(button)

    def click_next(self):
        "Click the next widget."
        x, y = imgui.get_cursor_screen_pos()
        yield from self.move_cursor(x + 5, y + 5)
        yield from self.pause()
        yield from self.click()
        # Give the widget time to react
        yield
        yield

    def mark(self, name, widget):
        """ Display a widget, but mark it with a name so it can be interacted with at a later point
        using methods such as `click_marked`. """
        while True:
            self.marked[name] = imgui.get_cursor_screen_pos()
            try:
                next(widget)
            except StopIteration as e:
                return e.value
            yield

    def click_marked(self, name, x=5, y=5):
        "Click the given `marked` widget. Optionally, specify the click offset `x, y` coords."
        if name not in self.marked:
            raise ValueError(f"Name '{name}' was not previously marked.")
        x0, y0 = self.marked[name]
        yield from self.move_cursor(x0 + x, y0 + y)
        yield from self.pause()
        yield from self.click()
        # Give the widget time to react
        yield
        yield

    def move_cursor(self, x, y):
        "Move cursor to a given position."
        io = imgui.get_io()
        ox, oy = io.mouse_pos
        yield
        if self.slow:
            for f in np.linspace(0, 1, 30):
                self.puppet.set_mouse_pos(x * f + ox * (1 - f), y * f + oy * (1 - f))
                yield
        else:
            self.puppet.set_mouse_pos(x, y)
            yield

    def scroll_up(self):
        "Scroll up."
        self.puppet.scroll_up()
        yield

    def scroll_dn(self):
        "Scroll down."
        self.puppet.scroll_dn()
        yield

    def mouse_up(self, button=0):
        "Release the given mouse button."
        self.puppet.mouse_up(button)
        yield

    def mouse_dn(self, button=0):
        "Push the given mouse button."
        self.puppet.mouse_dn(button)
        yield

    def write_char(self, ch):
        "Write a given character."
        self.puppet.write_char(ch)
        yield

    def pause(self, nframes=0):
        """Pause for a specified number of frames.

        If `nframes` <= 0, the pause length depends on the
        environment variable `TEST_SLOW`.
        """
        if nframes <= 0:
            if self.slow:
                for _ in range(30):
                    yield
            yield
        else:
            for _ in range(nframes):
                yield
