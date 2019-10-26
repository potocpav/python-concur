""" Passive geometric shape widgets to be drawn as image overlay, or on their own.

As these widgets are passive, they don't need a name. For active overlay, use normal widgets
such as buttons.
"""


import imgui


def line(x0, y0, x1, y1, color, width=1, tf=None):
    """ Line connecting two points.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = tf.i2s([x0, y0]), tf.i2s([x1, y1])
        draw_list = imgui.get_window_draw_list()
        draw_list.add_line(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), width)
        yield


def rect(x0, y0, x1, y1, color, width=1, rounding=0, tf=None):
    """ Straight non-filled rectangle specified by its two corners.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = tf.i2s([x0, y0]), tf.i2s([x1, y1])
        draw_list = imgui.get_window_draw_list()
        draw_list.add_rect(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), rounding, 15 if rounding else 0, width)
        yield


def _poly(name, pts, im2scr=None, scr2im=None):
    point_size = 10

    spts = [im2scr(p) for p in pts]

    draw_list = imgui.get_window_draw_list()
    pos = imgui.get_cursor_screen_pos()
    io = imgui.get_io()

    for p1, p2 in zip(spts, spts[1:] + [spts[0]]):
        draw_list.add_line(p1[0], p1[1], p2[0], p2[1], imgui.get_color_u32_rgba(1, 1, 0, 1), 2)

    mx, my = io.mouse_pos[0], io.mouse_pos[1]
    changed = False
    for i, p in enumerate(spts):
        imgui.set_cursor_screen_pos((p[0] - point_size, p[1] - point_size))
        imgui.invisible_button("Point {}{}".format(i, name), point_size*2, point_size*2)
        imgui.set_cursor_screen_pos((p[0] - 30, p[1] + point_size))
        imgui.button("Point {}{}".format(i, name), 60, 20)

        if imgui.is_item_active() and imgui.is_mouse_down(0):
            color = imgui.get_color_u32_rgba(1, 1, 0, 1)
            spts[i] = (p[0] + io.mouse_delta[0], p[1] + io.mouse_delta[1])
            changed = io.mouse_delta[0] != 0 or io.mouse_delta[1] != 0
        else:
            color = imgui.get_color_u32_rgba(1, 1, 0, 1)

        draw_list.add_rect(p[0] - point_size/2, p[1] - point_size/2, p[0] + point_size/2, p[1] + point_size/2, color, thickness=2)

    imgui.set_cursor_screen_pos(pos)
    return changed, [scr2im(p) for p in spts]


def poly(state, im2scr=None, scr2im=None):
    while True:
        changed, st = _poly("p", state, im2scr, scr2im)
        if changed:
            return st
        yield
