""" Passive geometric shape widgets to be drawn as image overlay, or on their own.

As these widgets are passive, they don't need a name. For active overlay, use normal widgets such as buttons.
"""


import numpy as np
import imgui


def line(x0, y0, x1, y1, color, thickness=1, tf=None):
    """ Line connecting two points.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = np.matmul(tf.i2s, [x0, y0, 1]), np.matmul(tf.i2s, [x1, y1, 1])
        draw_list = imgui.get_window_draw_list()
        draw_list.add_line(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), thickness)
        yield


def rect(x0, y0, x1, y1, color, thickness=1, rounding=0, tf=None):
    """ Straight non-filled rectangle specified by its two corners.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            [x0, y0], [x1, y1] = np.matmul(tf.i2s, [x0, y0, 1]), np.matmul(tf.i2s, [x1, y1, 1])
        draw_list = imgui.get_window_draw_list()
        draw_list.add_rect(x0, y0, x1, y1, imgui.get_color_u32_rgba(*color), rounding, 15 if rounding else 0, thickness)
        yield


def circle(cx, cy, radius, color, thickness=1, num_segments=16, tf=None):
    """ Circle specified by its center and radius.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            assert np.allclose(tf.i2s[0,0], tf.i2s[1,1])
            [cx, cy], radius = np.matmul(tf.i2s, [cx, cy, 1]), radius * tf.i2s[0,0]
        draw_list = imgui.get_window_draw_list()
        draw_list.add_circle(cx, cy, radius, imgui.get_color_u32_rgba(*color), num_segments=num_segments, thickness=thickness)
        yield


def text(x, y, color, string, tf=None):
    """ Text, using the default font and font size.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            x, y = np.matmul(tf.i2s, [x, y, 1])
        draw_list = imgui.get_window_draw_list()
        draw_list.add_text(x, y, imgui.get_color_u32_rgba(*color), string)
        yield
