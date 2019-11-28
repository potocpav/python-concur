""" Zoomable, pannable widget with arbitrary content. """

""" Scrollable, zoomable image widget with overlay support. """


import copy
import numpy as np

import imgui
from concur.widgets import child


def pan_zoom(name, state, width=None, height=None, content_gen=None):
    """ Create the Pan & Zoom widget.

    This widget is a pannable, zoomable view of a thing given by `content_gen`. To ease integration with other widget,
    this widget returns events in a special format: `(name, state, child_event)`. State or child_event may be `None`
    in case `state` didn't change, or `child_event` didn't fire. `name` is the name supplied to this function

    `content_gen` is a function that takes the `concur.extra_widgets.pan_zoom.TF` object, and returns a Concur
    widget. It is up to the widget to do the necessary transformations using the `TF` object.
    """
    while True:
        if width is None:
            w = imgui.get_content_region_available()[0]
        if height is None:
            h = imgui.get_content_region_available()[1]
        w = max(1, w)
        h = max(1, h)

        zoom_x = w / (state.right  - state.left)
        zoom_y = h / (state.bottom - state.top)

        left, right = state.left, state.right
        top, bottom = state.top, state.bottom
        if state.keep_aspect:
            aspect = float(state.keep_aspect)
            assert zoom_x > 0 and zoom_y > 0, "Flipped axes are not supported if `keep_aspect` is not False"
            assert state.keep_aspect > 0, "Negative aspect ratio is not supported."
            if zoom_x > zoom_y * aspect:
                zoom_x = zoom_y * aspect
                center_x = (state.left + state.right) / 2
                left  = center_x - w / zoom_x / 2
                right = center_x + w / zoom_x / 2
            if zoom_y > zoom_x / aspect:
                zoom_y = zoom_x / aspect
                center_y = (state.top + state.bottom) / 2
                top    = center_y - h / zoom_y / 2
                bottom = center_y + h / zoom_y / 2

        origin = imgui.get_cursor_screen_pos()

        imgui.begin_child("Pan-zoom container", w, h, False, flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE) # needs to be before is_window_hovered

        # Interaction
        st = copy.deepcopy(state)
        dragging_1, dragging_2 = imgui.is_mouse_dragging(1, 1), imgui.is_mouse_dragging(2, 1)
        is_dragging = (dragging_1 or dragging_2) and st.is_hovered
        drag_delta = imgui.get_mouse_drag_delta(1 if dragging_1 else 2, 1)
        delta = drag_delta[0] - st.last_drag_delta[0], drag_delta[1] - st.last_drag_delta[1]
        st.last_drag_delta = drag_delta

        io = imgui.get_io()
        if not is_dragging:
            st.is_hovered = imgui.is_window_hovered()

        # Pan
        if is_dragging and (delta[0] or delta[1]):
            if st.fix_axis != 'x':
                st.left -= delta[0] / zoom_x
                st.right -= delta[0] / zoom_x
            if st.fix_axis != 'y':
                st.top -= delta[1] / zoom_y
                st.bottom -= delta[1] / zoom_y

        # Zoom
        if st.is_hovered and io.mouse_wheel:
            factor = 1.3 ** io.mouse_wheel

            if st.fix_axis != 'x':
                mx_rel = (io.mouse_pos[0] - origin[0]) / w * 2 - 1
                mx = mx_rel * (right - left) / (st.right - st.left) / 2 + 0.5
                wi = st.right - st.left
                st.left  = st.left    + wi * mx     - wi / factor * mx
                st.right = st.right   - wi * (1-mx) + wi / factor * (1-mx)

            if st.fix_axis != 'y':
                my_rel = (io.mouse_pos[1] - origin[1]) / h * 2 - 1
                my = my_rel * (bottom - top) / (st.bottom - st.top) / 2 + 0.5
                hi = st.bottom - st.top
                st.top  = st.top      + hi * my     - hi / factor * my
                st.bottom = st.bottom - hi * (1-my) + hi / factor * (1-my)


        view_s = [origin[0], origin[1], origin[0] + w, origin[1] + h]
        view_c = [left, top, right, bottom]

        s2c = np.array( # Screen to Content
            [ [1 / zoom_x, 0, left - origin[0] / zoom_x]
            , [0, 1 / zoom_y, top  - origin[1] / zoom_y]
            ])

        c2s = np.array( # Content to Screen
            [ [zoom_x, 0, origin[0] - left * zoom_x]
            , [0, zoom_y, origin[1] - top  * zoom_y]
            ])

        content_value = None
        try:
            if content_gen is not None:
                next(content_gen(TF(c2s, s2c, view_c, view_s, st.is_hovered)))
        except StopIteration as e:
            content_value = e.value
        finally:
            imgui.end_child()
        changed = st != state
        if changed or content_value is not None:
            return name, (st if changed else None, content_value)
        else:
            yield


class PanZoom(object):
    """ Pan & zoom state. """
    def __init__(self, top_left, bottom_right, keep_aspect=True, fix_axis=None):
        """
        Arguments:
            top_left:     Coordinates of the top left corner of the displayed content area.
            bottom_right: oordinates of the bottom right corner of the displayed content area.
            keep_aspect:  Keep aspect ratio (x/y) equal to a given constant and zoom proportionally.
            fix_axis:     Do not zoom in a given axis (`'x'`, or `'y'`).
        """
        assert not keep_aspect or not fix_axis, "Can't fix axis and keep_aspect at the same time."

        self.reset_view(top_left, bottom_right)
        self.last_drag_delta = 0, 0
        self.is_hovered = False # Include cursor outside, but dragging

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

    Both screen-space and image-space are in pixels with top-left corner equal to (0, 0).
    Transformations are expressed as NumPy matrices in homogenous coordinates with two rows and three columns (shape: (2, 3)).

    For example, a point `[px, py]` can be transformed to screen-space by left multiplication:

    ```python
    q = np.matmul(c2s, [px, py, 1])
    ```

    Mostly, the necessary conversions are performed by overlay widgets.

    Attributes:
        c2s:      Content-to-screen transformation matrix.
        s2c:      Screen-to-content transformation matrix.
        view_s:   Screen-space viewport coordinates as a list [left, top, right, bottom].
        view_c:   Image-space viewport coordinates as a list [left, top, right, bottom].
        hovered:  `True` if the image widget is hovered over. Useful for some interactive elements,
                  such as draggable widgets.
    """
    def __init__(self, c2s, s2c, view_c, view_s, hovered):
        self.c2s = c2s
        self.s2c = s2c
        self.view_c = view_c
        self.view_s = view_s
        self.hovered = hovered
