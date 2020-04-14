""" Zoomable, pannable widget with arbitrary content.

This widget is rarely used directly by user code. Most of the time, it's more convenient to use
higher-level widgets `concur.extra_widgets.image.image`, or `concur.extra_widgets.frame.frame`.
"""


import copy
import numpy as np

import imgui
from concur.widgets import child, invisible_button
from concur.core import orr, forever, optional, map as cmap
from concur.extra_widgets.draggable import draggable


def pan_zoom(name, state, width=None, height=None, content_gen=None, drag_tag=None, down_tag=None, hover_tag=None):
    """ Create the Pan & Zoom widget, serving as a container for a thing given by `content_gen`.

    This widget is mostly not used directly. Instead, a special-purpose wrapper can be used,
    such as `concur.extra_widgets.image.image`, or `concur.extra_widgets.frame.frame`.

    Arguments:
        name: widget name. Also serves as an event identifier
        state: `PanZoom` object representing state.
        width: widget width in pixels. If `None`, it fills the available space.
        height: widget height in pixels. If `None`, it fills the available space.
        content_gen: Widget generator to display inside the pan-zoom widget. All events are passed
            through as a return tuple member. This is a function that takes the
            `concur.extra_widgets.pan_zoom.TF` object, and returns a Concur
            widget. It is up to the widget to do the necessary transformations
            using the `TF` object.
        drag_tag: The event tag for LMB drag events. If `None`, no drag events are fired.
        down_tag: The event tag for LMB down events. If `None`, no down events are fired.
            Useful in combination with `drag_tag` to indicate when the dragging started.
        hover_tag: The event tag for mouse hover when no mouse buttons are down.
            If `None`, no hover events are fired. Events are fired only when the mouse is moving.

    Returns:
        To ease integration with other widgets, this widget returns events in a special format:
        `(name, state, event)`. `state` or `event` may be `None` in case `state` didn't change,
        or there is no `event`.

        If `drag_tag`, or `down_tag` arguments are used, these are fired in the `event` member of the return tuple.
    """
    assert content_gen is not None
    tf, content = None, None
    while True:
        assert not state.keep_aspect or not state.fix_axis, \
            "Can't fix axis and keep_aspect at the same time."
        # Dynamically rescale width and height if they weren't specified
        if width is None:
            w = imgui.get_content_region_available()[0]
        else:
            w = width
        if height is None:
            h = imgui.get_content_region_available()[1]
        else:
            h = height
        frame_w = max(1, w - state.margins[0] + state.margins[2])
        frame_h = max(1, h - state.margins[1] + state.margins[3])
        w = max(1, w)
        h = max(1, h)

        zoom_x = frame_w / (state.right  - state.left)
        zoom_y = frame_h / (state.bottom - state.top)

        left, right = state.left, state.right
        top, bottom = state.top, state.bottom
        if state.keep_aspect:
            aspect = float(state.keep_aspect)
            assert state.keep_aspect > 0, "Negative aspect ratio is not supported."
            if abs(zoom_x) > abs(zoom_y) * aspect:
                zoom_x = np.sign(zoom_x) * abs(zoom_y) * aspect
                center_x = (left + right) / 2
                left  = center_x - frame_w / zoom_x / 2
                right = center_x + frame_w / zoom_x / 2
            if abs(zoom_y) > abs(zoom_x) / aspect:
                zoom_y = np.sign(zoom_y) * abs(zoom_x) / aspect
                center_y = (top + bottom) / 2
                top    = center_y - frame_h / zoom_y / 2
                bottom = center_y + frame_h / zoom_y / 2

        origin = imgui.get_cursor_screen_pos()

        imgui.begin_child("Pan-zoom", w, h, False, flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE) # needs to be before is_window_hovered

        # Interaction
        st = copy.deepcopy(state)
        io = imgui.get_io()
        is_window_hovered = imgui.is_window_hovered()

        if (imgui.is_mouse_clicked(1) or imgui.is_mouse_clicked(2)) and is_window_hovered:
            st.is_rmb_dragged = True
        if not (io.mouse_down[1] or io.mouse_down[2]):
            st.is_rmb_dragged = False

        delta = io.mouse_delta

        # Pan
        if st.is_rmb_dragged and (delta[0] or delta[1]):
            if st.fix_axis != 'x':
                st.left -= delta[0] / zoom_x
                st.right -= delta[0] / zoom_x
            if st.fix_axis != 'y':
                st.top -= delta[1] / zoom_y
                st.bottom -= delta[1] / zoom_y

        # Zoom
        if (imgui.is_window_hovered() or st.is_rmb_dragged) and io.mouse_wheel:
            factor = 1.3 ** io.mouse_wheel

            if st.fix_axis != 'x':
                mx_rel = (io.mouse_pos[0] - origin[0] - state.margins[0]) / frame_w * 2 - 1
                mx = mx_rel * (right - left) / (st.right - st.left) / 2 + 0.5
                wi = st.right - st.left
                st.left  = st.left    + wi * mx     - wi / factor * mx
                st.right = st.right   - wi * (1-mx) + wi / factor * (1-mx)

            if st.fix_axis != 'y':
                my_rel = (io.mouse_pos[1] - origin[1] - state.margins[1]) / frame_h * 2 - 1
                my = my_rel * (bottom - top) / (st.bottom - st.top) / 2 + 0.5
                hi = st.bottom - st.top
                st.top    = st.top    + hi * my     - hi / factor * my
                st.bottom = st.bottom - hi * (1-my) + hi / factor * (1-my)

        # Get screen-space bounds disregarding the margins
        left_s = left - st.margins[0] / zoom_x
        top_s =   top - st.margins[1] / zoom_y
        right_s = right - st.margins[2] / zoom_x
        bottom_s = bottom - st.margins[3] / zoom_y


        s2c = np.array([ # Screen to Content
            [1 / zoom_x, 0, left_s - origin[0] / zoom_x],
            [0, 1 / zoom_y, top_s  - origin[1] / zoom_y]])

        c2s = np.array([ # Content to Screen
            [zoom_x, 0, origin[0] - left_s * zoom_x],
            [0, zoom_y, origin[1] - top_s  * zoom_y]])

        view_s = [origin[0], origin[1], origin[0] + w, origin[1] + h]
        view_c = [left_s, top_s, right_s, bottom_s]

        content_value = None
        # coord_to_content = lambda x:
        try:
            new_tf = TF(c2s, s2c, view_c, view_s)
            if tf is None or tf != new_tf:
                tf = new_tf
                w, h = tf.view_s[2] - tf.view_s[0], tf.view_s[3] - tf.view_s[1]
                content = orr([
                    content_gen(tf),
                    cmap(lambda k: (k[0], [tf.s2c[0,0] * k[1].x, tf.s2c[1,1] * k[1].y]),
                        optional(drag_tag is not None,
                            draggable, drag_tag, forever(invisible_button, "", w, h)
                            )
                        ),
                    ])
            next(content)
        except StopIteration as e:
            content_value = e.value
        finally:
            imgui.end_child()
        changed = st != state

        if down_tag and not st.is_rmb_dragged and imgui.is_mouse_clicked() and is_window_hovered:
            return name, (None, (down_tag, tf.inv_transform(np.array([[*io.mouse_pos]]))[0]))
        if changed or content_value is not None:
            return name, (st if changed else None, content_value)
        if hover_tag and not st.is_rmb_dragged and not any(imgui.is_mouse_clicked(i) for i in [0,1,2]) and is_window_hovered and (delta[0] or delta[1]):
            return name, (None, (hover_tag, tf.inv_transform(np.array([[*io.mouse_pos]]))[0]))
        yield


class PanZoom(object):
    """ Pan & zoom state. """
    def __init__(self, top_left, bottom_right, keep_aspect=True, fix_axis=None, margins=[0, 0, 0, 0]):
        """
        Arguments:
            top_left:     Coordinates of the top left corner of the displayed content area.
            bottom_right: Coordinates of the bottom right corner of the displayed content area.
            keep_aspect:  Keep aspect ratio (x/y) equal to a given constant and zoom proportionally.
                          if keep_aspect==True, it is equivalent to keep_aspect==1.
            fix_axis:     Do not zoom in a given axis (`'x'`, `'y'`, or `None`).
            margins:      Margins (left, top, right, bottom) of the view area in pixels.
                          If the view area should be inset by 5 px on each side, then use
                          margins=[5,5,-5,-5].
        """
        self.reset_view(top_left, bottom_right)
         # Include cases where cursor is outside the element, but was inside when the drag started.
         # Exclude cases where cursor is inside the element, but was outside when the drag started.
        self.is_rmb_dragged = False
        self.is_lmb_dragged = False
        self.margins = margins

        self.keep_aspect = keep_aspect
        self.fix_axis = fix_axis

    def reset_view(self, top_left=None, bottom_right=None):
        """ Reset view to default values. """
        if top_left is not None:
            self.default_left = top_left[0]
            self.default_top = top_left[1]
        if bottom_right is not None:
            self.default_right = bottom_right[0]
            self.default_bottom = bottom_right[1]
        self.top = self.default_top
        self.bottom = self.default_bottom
        self.left = self.default_left
        self.right = self.default_right

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class TF(object):
    """ Transformation object containing information necessary for converting between screen-space and image-space.

    Screen-space coordinates are in pixels with top-left window corner equal to (0, 0). Image space is
    arbitrary, given by the respective PanZoom widget state. Transformations are expressed as NumPy
    matrices in homogenous coordinates with two rows and three columns (shape: `(2, 3)`).

    For example, a point `[px, py]` can be transformed to screen-space by left multiplication:

    ```python
    q = np.matmul(c2s, [px, py, 1])
    ```

    Mostly, the necessary conversions are performed by overlay widgets in `concur.draw`.
    It may be useful to transform stuff by hand in cases when default behavior is not sufficient,
    such as specifying the line width in image coordinates.

    Attributes:
        c2s:      Content-to-screen transformation matrix.
        s2c:      Screen-to-content transformation matrix.
        view_s:   Screen-space viewport coordinates as a list [left, top, right, bottom].
        view_c:   Image-space viewport coordinates as a list [left, top, right, bottom].
    """
    def __init__(self, c2s, s2c, view_c, view_s):
        self.c2s = c2s
        self.s2c = s2c
        self.view_c = view_c
        self.view_s = view_s

    def __eq__(self, other):
        return \
            np.array_equal(self.c2s, other.c2s) and \
            np.array_equal(self.s2c, other.s2c) and \
            self.view_c == other.view_c and \
            self.view_s == other.view_s and \
            True

    def transform(self, points):
        """Transform a given NumPy array of `n` points of shape `(n, 2)` from content-space to screen-space."""
        return np.tensordot(np.hstack([points, np.ones((points.shape[0], 1))]), self.c2s, (1, 1))

    def inv_transform(self, points):
        """Transform a given NumPy array of `n` points of shape `(n, 2)` from screen-space to content-space."""
        return np.tensordot(np.hstack([points, np.ones((points.shape[0], 1))]), self.s2c, (1, 1))
