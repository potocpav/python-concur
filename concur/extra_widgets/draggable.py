""" Widget which can be dragged around. """


import imgui


def draggable(name, widget, tag=None):
    """Add draggable functionality to a widget. Emits (dx, dy) when dragged.

    The underlying widget works as usual.

    Returned values are equal to the drag amount from the previous frame.
    """
    io = imgui.get_io()
    while True:
        try:
            imgui.begin_group()
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_group()
        if imgui.is_item_active() and (io.mouse_delta[0] or io.mouse_delta[1]):
            return tag if tag is not None else name, io.mouse_delta
        yield
