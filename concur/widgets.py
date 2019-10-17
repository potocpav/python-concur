
import imgui

from concur.core import orr, lift


def orr_same_line(elems):
    """ Use instead of :func:`orr` to layout child widgets horizontally.

    Intersperses :func:`same_line` between each pair of consecutive widgets in ``elems``.
    """
    def intersperse(delimiter, seq):
        """ https://stackoverflow.com/questions/5655708/python-most-elegant-way-to-intersperse-a-list-with-an-element """
        from itertools import chain, repeat
        return list(chain.from_iterable(zip(repeat(delimiter), seq)))[1:]

    return orr(intersperse(same_line(), elems))


def window(title, elems, position=None, size=None, flags=0):
    while True:
        imgui.push_id(title)
        if position is not None:
            imgui.set_next_window_position(*position)
        if size is not None:
            imgui.set_next_window_size(*size)
        imgui.begin(title, flags=flags)
        try:
            next(orr(elems))
        except StopIteration as e:
            return e.value
        finally:
            imgui.end()
            imgui.pop_id()
        yield


def child(name, width, height, border=False, flags=0, elems=[]):
    while True:
        imgui.push_id(name)
        imgui.begin_child(name, width, height, border, flags)
        try:
            next(orr(elems))
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

def radio_button(text, active, value=None):
    """ Radio button. Returns ``(text, value)`` on click. """
    while not imgui.radio_button(text, active):
        yield
    return value if value is not None else text


def input_text(name, value, buffer_length):
    while True:
        changed, new_value = imgui.input_text(name, value, buffer_length)
        if changed:
            return name, new_value
        else:
            yield


def interactive_elem(elem, name, *args, **kwargs):
    if 'tag' in kwargs:
        tag = kwargs['tag']
        del kwargs['tag']
    else:
        tag = name
    while True:
        changed, value = elem(name, *args, **kwargs)
        if changed:
            return (tag, value)
        else:
            yield


def text(s):
    return lift(lambda: imgui.text(s))

def text_colored(s, r, g, b, a=1.):
    return lift(imgui.text_colored, s, r, g, b, a)

def show_test_window():
    return lift(lambda: imgui.show_test_window())

def separator():
    return lift(lambda: imgui.separator())

def spacing():
    return lift(lambda: imgui.spacing())

def same_line():
    """ Call between widgets to layout them horizontally. """
    return lift(lambda: imgui.same_line())

def checkbox(*args, **kwargs):
    return interactive_elem(imgui.checkbox, *args, **kwargs)

def drag_float(*args, **kwargs):
    return interactive_elem(imgui.drag_float, *args, **kwargs)

def slider_int(*args, **kwargs):
    return interactive_elem(imgui.slider_int, *args, **kwargs)

def slider_float(*args, **kwargs):
    return interactive_elem(imgui.slider_float, *args, **kwargs)
