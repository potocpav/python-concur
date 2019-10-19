
from typing import Iterable, Any, Tuple
import imgui

from concur.core import orr, lift, Widget


def orr_same_line(widgets):
    """ Use instead of :func:`orr` to layout child widgets horizontally.
    """
    def intersperse(delimiter, seq):
        """ https://stackoverflow.com/questions/5655708/python-most-elegant-way-to-intersperse-a-list-with-an-element """
        from itertools import chain, repeat
        return list(chain.from_iterable(zip(repeat(delimiter), seq)))[1:]

    return orr(intersperse(same_line(), widgets))


def window(title: str,
           widgets: Iterable[Widget],
           position: Tuple[int, int] = None,
           size: Tuple[int, int] = None,
           flags: int = 0) -> Widget:
    """ Create a window with a given list of ``widgets`` inside. """
    while True:
        imgui.push_id(title)
        if position is not None:
            imgui.set_next_window_position(*position)
        if size is not None:
            imgui.set_next_window_size(*size)
        imgui.begin(title, flags=flags)
        try:
            next(orr(widgets))
        except StopIteration as e:
            return e.value
        finally:
            imgui.end()
            imgui.pop_id()
        yield


def child(name, width, height, border=False, flags=0, widgets=[]):
    """ Create a sized box with elements inside a window. """
    while True:
        imgui.push_id(name)
        imgui.begin_child(name, width, height, border, flags)
        try:
            next(orr(widgets))
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_child()
            imgui.pop_id()
        yield


def button(text, tag=None):
    """ Button. Returns ``(text, value)`` on click, or ``(tag, value)`` if tag is specified. """
    while not imgui.button(text):
        yield
    return tag if tag is not None else text, None


def radio_button(text, active, tag=None):
    """ Radio button. Returns ``(text, value)`` on click. """
    while not imgui.radio_button(text, active):
        yield
    return (tag if tag is not None else text), None


def input_text(name, value, buffer_length, tag=None):
    """ Text input. """
    while True:
        changed, new_value = imgui.input_text(name, value, buffer_length)
        if changed:
            return (name if tag is None else tag), new_value
        else:
            yield


def key_pressed(name, key_index, repeat=True):
    """ Invisible widget that waits for a given key to be pressed.

    Key codes are specified by the integration layer, e.g. ``glfw.KEY_A``.
    """
    while True:
        if imgui.is_key_pressed(key_index, repeat):
            return name, None
        yield


def text(s):
    """ Passive text display widget. """
    return lift(imgui.text)

def text_colored(s, r, g, b, a=1.):
    """ Passive colored text display widget. """
    return lift(imgui.text_colored, s, r, g, b, a)

def test_window():
    """ ImGui test window with a multitude of widgets. """
    return lift(imgui.show_test_window)

def separator():
    """ Horizontal separator. """
    return lift(imgui.separator)

def spacing():
    """ Extra horizontal space. """
    return lift(imgui.spacing)

def same_line():
    """ Call between widgets to layout them horizontally.

    Consider using :func:`orr_same_line` instead.
    """
    return lift(imgui.same_line)

def checkbox(*args, **kwargs):
    """ Two-state checkbox. """
    return interactive_elem(imgui.checkbox, *args, **kwargs)

def drag_float(label, value, *args, **kwargs):
    """ Float selection widget without a slider. """
    return interactive_elem(imgui.drag_float, label, value, *args, **kwargs)

def slider_int(label, min_value, max_value, *args, **kwargs):
    """ Int selection slider. """
    return interactive_elem(imgui.slider_int, name, min_value, max_value, *args, **kwargs)

def slider_float(label, min_value, max_value, *args, **kwargs):
    """ Float selection slider. """
    return interactive_elem(imgui.slider_float, name, min_value, max_value, *args, **kwargs)
