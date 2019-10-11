
import imgui

from concur.core import orr, lift


def window(title, elems):
    stop = False
    while True:
        imgui.push_id(title)
        imgui.begin(title)
        try:
            next(orr(elems))
        except StopIteration:
            return
        finally:
            imgui.end()
            imgui.pop_id()
        yield


def orr_same_line(elems):
    def intersperse(delimiter, seq):
        """ https://stackoverflow.com/questions/5655708/python-most-elegant-way-to-intersperse-a-list-with-an-element """
        from itertools import chain, repeat
        return list(chain.from_iterable(zip(repeat(delimiter), seq)))[1:]

    v = yield from orr(intersperse(same_line(), elems))
    return v


def button(text, value=None):
    while not imgui.button(text):
        yield
    return value or text


def input_text(value, buffer_length):
    while True:
        changed, new_value = imgui.input_text("input_text", value, buffer_length)
        if changed:
            return new_value
        else:
            yield


def interactive_elem(elem, *args, **kwargs):
    while True:
        changed, value = elem(*args, **kwargs)
        if changed:
            return value
        else:
            yield


def text(s):
    return lift(lambda: imgui.text(s))

def show_test_window():
    return lift(lambda: imgui.show_test_window())

def separator():
    return lift(lambda: imgui.separator())

def same_line():
    return lift(lambda: imgui.same_line())

def checkbox(*args, **kwargs):
    return interactive_elem(imgui.checkbox, *args, **kwargs)

def drag_float(*args, **kwargs):
    return interactive_elem(imgui.drag_float, *args, **kwargs)
