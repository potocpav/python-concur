""" Widget which can be dragged around. """


import imgui


def draggable(name, tag=None):
    io = imgui.get_io()
    while True:
        imgui.button(name)
        if imgui.is_item_active():
            return tag if tag is not None else text, io.mouse_delta
        yield
