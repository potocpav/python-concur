""" Widget which can be dragged around. """


import imgui


def draggable(name, tag=None):
    """Draggable button (can't be clicked). Emits (dx, dy) coordinates when dragged.

    To limit this to a button is silly, PRs welcome :)
    """
    io = imgui.get_io()
    while True:
        imgui.button(name)
        if imgui.is_item_active():
            return tag if tag is not None else name, io.mouse_delta
        yield
