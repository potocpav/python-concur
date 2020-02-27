""" Passive geometric shape widgets to be drawn as `concur.extra_widgets.image.image` or `concur.extra_widgets.frame.frame` overlay, or on their own.

All these widgets have the following in common:

* They are passive, so they don't need names. For active overlay, use normal widgets, such as buttons, wrapped inside `concur.widgets.transform`.
* They don't do automatic layout. Instead the exact position is specified by hand.
* Color can be specified in several ways:
    * RGBA tuple with values between 0 and 1. For example, `(0.5, 0.5, 1, 1)` is light blue.
    * RGB tuple with values between 0 and 1. The result is opaque.
    * String specifying a color from the [xkcd color set](https://xkcd.com/color/rgb/), for example, `'red'`.
    * `(str, float)` pair, where the first element specifies color, and the second element specifies alpha.
    * A single `int`, specifying ABGR color. For example, `0xffaa0000` is dark blue.
* `tf` is the `concur.extra_widgets.pan_zoom.TF` object specifying transformations from screen-space to image-space and back.
  If no transformation is supplied, the element is drawn in screen space units.

Theses widgets are not re-exported in the root module, and are normally used as `c.draw.line(...)`, etc.
They can be composed normally using the `concur.core.orr` function.
"""

import numpy as np
import imgui
from concur.colors import color_to_rgba
from concur.core import nothing

__pdoc__ = dict(prepare_polyline_points=False)


def line(x0, y0, x1, y1, color, thickness=1, tf=None):
    """ Line connecting two points. """
    if tf is not None:
        [x0, y0], [x1, y1] = tf.transform(np.array([[x0, y0], [x1, y1]]))
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_line(x0, y0, x1, y1, col, thickness)
        yield


def rect(x0, y0, x1, y1, color, thickness=1, rounding=0, tf=None):
    """ Straight non-filled rectangle specified by its two corners. """
    if tf is not None:
        [x0, y0], [x1, y1] = tf.transform(np.array([[x0, y0], [x1, y1]]))
    # Avoid issues with disappearing lines on very large rectangles
    x0, x1 = np.clip([x0, x1], -8192, 8192)
    y0, y1 = np.clip([y0, y1], -8192, 8192)
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_rect(x0, y0, x1, y1, col, rounding, 15 if rounding else 0, thickness)
        yield


def rects(rects, color, thickness=1, tf=None):
    """ Multiple straight non-filled rectangles specified by their two corners.

    `rects` is a NumPy array of shape `(n, 4)`, where `n` is the number of rectangles.
    """
    if len(rects) == 0:
        while True:
            yield
    if tf is not None:
        rects = tf.transform(rects.reshape(-1, 2)).reshape(rects.shape)
    # Avoid issues with disappearing lines on very large rectangles
    rects = np.clip(rects, -8192, 8192)
    polys = np.empty((len(rects), 4, 2), dtype=rects.dtype)
    polys[:,0] = rects[:,:2]
    polys[:,1,0] = rects[:,0]
    polys[:,1,1] = rects[:,3]
    polys[:,2] = rects[:,2:]
    polys[:,3,0] = rects[:,2]
    polys[:,3,1] = rects[:,1]
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_polylines(polys, col, True, thickness)
        yield


def rect_filled(x0, y0, x1, y1, color, rounding=0, tf=None):
    """ Straight non-filled rectangle specified by its two corners. """
    if tf is not None:
        [x0, y0], [x1, y1] = tf.transform(np.array([[x0, y0], [x1, y1]]))
    # Avoid issues with disappearing lines on very large rectangles
    x0, x1 = np.clip([x0, x1], -8192, 8192)
    y0, y1 = np.clip([y0, y1], -8192, 8192)
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_rect_filled(x0, y0, x1, y1, col, rounding, 15 if rounding else 0)
        yield


def circle(cx, cy, radius, color, thickness=1, num_segments=16, tf=None):
    """ Circle specified by its center and radius. """
    if tf is not None:
        assert np.allclose(np.abs(tf.c2s[0,0]), np.abs(tf.c2s[1,1])), \
            "`tf` must be aspect ratio preserving to draw circles. Use `ellipse` instead, if it isn't the case."
        [cx, cy], radius = np.matmul(tf.c2s, [cx, cy, 1]), radius * tf.c2s[0,0]
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_circle(cx, cy, radius, col, num_segments=num_segments, thickness=thickness)
        yield


def prepare_polyline_points(points, tf):
    if len(points) == 0:
        return []
    if not isinstance(points, np.ndarray):
        points = np.array(points)
    if tf is not None:
        points = tf.transform(points)
    return points


def polyline(points, color, closed=False, thickness=1, tf=None):
    """ Polygonal line or a closed polygon.

    `points` is a list of (x, y) tuples, or a NumPy array of equivalent shape.
    """
    points = prepare_polyline_points(points, tf)
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_polyline(points, col, closed, thickness)
        yield


def polygon(points, color, tf=None):
    """ Filled polygon. Points must form a convex area.

    `points` is a list of (x, y) tuples, or a NumPy array of equivalent shape.
    """
    points = prepare_polyline_points(points, tf)
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_convex_poly_filled(points, col)
        yield


def polylines(points, color, closed=False, thickness=1, tf=None):
    """ Multiple polygonal lines with the same length and parameters.

    Calling this function is more efficient than calling `polyline` multiple times, because all the data is given
    to the C++ back-end in one Python call, and because transformation is vectorized.

    `points` is a NumPy array with shape `(n, m, 2)`, where `n` is the number of polylines, and `m` is the number of points
    in each polyline.
    """
    if tf is not None:
        points = tf.transform(points.reshape(-1, 2)).reshape(points.shape)
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_polylines(points, col, closed, thickness)
        yield


def polygons(points, color, tf=None):
    """ Multiple filled polygons with the same length and color.

    Calling this function is more efficient than calling `polygon` multiple times, because all the data is given
    to the C++ back-end in one Python call, and because transformation is vectorized.

    `points` is a NumPy array with shape `(n, m, 2)`, where `n` is the number of polygons, and `m` is the number of points
    in each polyline.
    """
    if tf is not None:
        points = tf.transform(points.reshape(-1, 2)).reshape(points.shape)
    draw_list = imgui.get_window_draw_list()
    col = color_to_rgba(color)
    while True:
        draw_list.add_convex_polys_filled(points, col)
        yield


def text(string, x, y, color, tf=None):
    """ Text, using the default font and font size.

    This is a raw drawing function. Use `concur.widgets.text` instead if you want a text widget.
    """
    if tf is not None:
        x, y = np.matmul(tf.c2s, [x, y, 1])
    col = color_to_rgba(color)
    while True:
        # Text was hanging the application if too far away
        if -8192 < x < 8192 and -8192 < y < 8192:
            draw_list = imgui.get_window_draw_list()
            draw_list.add_text(x, y, col, string)
        yield


def image(tex_id, w, h, tf):
    """ Draw an image with the given width and height.

    This is a raw drawing function. Use `concur.extra_widgets.image.image` instead if you want an image widget.
    """
    x0, y0, x1, y1 = 0, 0, w, h
    if tf is not None:
        [x0, y0], [x1, y1] = tf.transform(np.array([[x0, y0], [x1, y1]]))
    draw_list = imgui.get_window_draw_list()
    l, t, r, b = tf.view_s
    a_s = tf.view_s[:2]
    b_s = tf.view_s[2:]
    a_i = tf.view_c[0] / w, tf.view_c[1] / h
    b_i = tf.view_c[2] / w, tf.view_c[3] / h
    while True:
        draw_list.add_image(tex_id, tuple(a_s), tuple(b_s), tuple(a_i), tuple(b_i))
        yield


def ellipse(mean, cov, sd, color, thickness=1, num_segments=16, tf=None):
    "Ellipse defined by a mean, covariance matrix, and SD."
    [e1, e2], vs = np.linalg.eig(cov)
    assert e1 > 0 and e2 > 0, "cov must be positive-semidefinite"
    v1, v2 = vs.T
    t = np.linspace(0, np.pi*2, num_segments, endpoint=False).reshape(-1, 1)
    el = v1 * np.sin(t) * np.sqrt(e1) * sd + v2 * np.cos(t) * np.sqrt(e2) * sd
    return polyline(el + mean, color, True, thickness, tf=tf)


def ellipses(means, covs, sd, color, thickness=1, num_segments=16, tf=None):
    """Multiple ellipses defined by a means, covariance matrices, and SD.

    The call is very similar to `ellipse`, but `mean` and `cov` are vectorized: there is one more dimension (zeroth) for both.
    For `n` ellipses, the shape of `mean` is `(n, 2)`, and the shape of `cov` is `(n, 2, 2)`.
    """
    if len(means) == 0 and len(covs) == 0:
        return nothing()
    assert len(means) == len(covs)
    assert len(means.shape) == 2 and means.shape[1] == 2
    assert len(covs.shape) == 3 and covs.shape[1] == 2 and covs.shape[2] == 2
    es, vs = np.linalg.eig(covs)
    assert np.all(es > 0), "covariance matrices must be positive-semidefinite"
    v1 = vs[...,0].reshape(-1, 1, 2)
    v2 = vs[...,1].reshape(-1, 1, 2)
    e1 = es[:,0].reshape(-1, 1, 1)
    e2 = es[:,1].reshape(-1, 1, 1)
    t = np.linspace(0, np.pi*2, num_segments, endpoint=False).reshape(-1, 1)
    el = v1 * np.sin(t) * np.sqrt(e1) * sd + v2 * np.cos(t) * np.sqrt(e2) * sd
    return polylines(el + means.reshape(-1, 1, 2), color, True, thickness, tf=tf)


def scatter(pts, color, marker, marker_size=10, thickness=1, tf=None):
    """Draw a scatter plot with given marker settings.

    If multiple settings are desired (such as two distinct point colors), call
    this function more than once with different parameters.

    Some markers are more performant than others, depending on the amount of
    generated geometry.

    Arguments:
      pts: NumPy array with shape `(n, 2)`, where `n` is the point count.
      color: Color to draw the markers.
      marker: Marker type. See the table below.
      marker_size: Size of the markers in pixels.
      thickness: Line width for non-filled markers
    ------
    marker | description
    ------ | ---
    `"."`  | filled square
    `"x"`  | cross
    `"+"`  | plus sign
    `"o"`  | non-filled circle
    """
    if tf is not None:
        pts = tf.transform(pts)

    if marker == '.':
        r = marker_size / 2
        polys = np.empty((len(pts), 4, 2))
        polys[:, 0, :] = pts + [-r, -r]
        polys[:, 1, :] = pts + [ r, -r]
        polys[:, 2, :] = pts + [ r,  r]
        polys[:, 3, :] = pts + [-r,  r]
        return polygons(polys, color)
    elif marker == '+':
        r = marker_size / 2
        polys = np.empty((len(pts) * 2, 2, 2))
        polys[0::2, 0, :] = pts - [r, 0]
        polys[0::2, 1, :] = pts + [r, 0]
        polys[1::2, 0, :] = pts - [0, r]
        polys[1::2, 1, :] = pts + [0, r]
        return polylines(polys, color, False, thickness)
    elif marker in ['X', 'x', '×']:
        r = marker_size / np.sqrt(8)
        polys = np.empty((len(pts) * 2, 2, 2))
        polys[0::2, 0, :] = pts - [r, r]
        polys[0::2, 1, :] = pts + [r, r]
        polys[1::2, 0, :] = pts - [-r, r]
        polys[1::2, 1, :] = pts + [-r, r]
        return polylines(polys, color, False, thickness)
    elif marker in ['O', 'o']:
        r = marker_size / 2
        n_verts = 7
        t = np.linspace(0, np.pi * 2, n_verts, endpoint=False)
        polys = np.empty((len(pts), n_verts, 2))
        polys[...,0] = np.sin(t) * r
        polys[...,1] = np.cos(t) * r
        polys += pts.reshape(-1, 1, 2)
        return polylines(polys, color, True, thickness)
    else:
        raise ValueError('Invalid marker')
