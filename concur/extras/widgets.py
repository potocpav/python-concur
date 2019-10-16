""" Extra widgets that probably belong to a separate library,
but are here for convenience.
"""


import imgui


def simple_image(tex_id, w, h):
    if tex_id is not None:
        pos = imgui.get_cursor_screen_pos()
        uva = 0, 0
        uvb = 1, 1
        draw_list = imgui.get_window_draw_list()
        draw_list.add_image(tex_id, (pos.x, pos.y), (pos.x + w, pos.y + h), uva, uvb);
