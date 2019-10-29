""" Passive geometric shape widgets to be drawn as image overlay, or on their own.

All these widgets have the following in common:

* They are passive, so they don't need names. For active overlay, use normal widgets such as buttons.
* `color` is specified as RGBA tuple with values between 0 and 1. For example, `(0.5, 0.5, 1, 1)` is light blue.
* `tf` is the `concur.extras.image.TF` object specifying transformations from screen-space to image-space and back.
  If no transformation is supplied, the element is drawn in screen space units.
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


def polyline(points, color, closed=False, thickness=1, tf=None):
    """ Polygonal line or a closed polygon.

    For color, use a RGBA tuple with values between 0 and 1.
    """
    while(True):
        if tf is not None:
            points = [list(np.matmul(tf.i2s, [x, y, 1])) for x, y in points]
        draw_list = imgui.get_window_draw_list()
        draw_list.add_polyline(points, imgui.get_color_u32_rgba(*color), closed, thickness)
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
