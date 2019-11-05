""" Zoomable, pannable widget with arbitrary content. """

""" Scrollable, zoomable image widget with overlay support. """


import copy
import numpy as np

import imgui
from concur.widgets import child


def pan_zoom(name, state, width=None, height=None, content_gen=None):
    """ Create the Pan & Zoom widget.

    This widget is a pannable, zoomable view of a thing given by `content_gen`.

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

        # Interaction
        state = copy.deepcopy(state)
        changed = False
        io = imgui.get_io()
        is_hovered = origin[0] < io.mouse_pos[0] < w + origin[0] \
                 and origin[1] < io.mouse_pos[1] < h + origin[1]

        # Detect if the image is being dragged by the mouse
        if (imgui.is_mouse_clicked(1) or imgui.is_mouse_clicked(2)) and is_hovered:
            changed |= not state.is_dragging
            state.is_dragging = True
        if not (imgui.is_mouse_down(1) or imgui.is_mouse_down(2)):
            changed |= state.is_dragging
            state.is_dragging = False

        # Pan
        if state.is_dragging and (io.mouse_delta[0] or io.mouse_delta[1]):
            if state.fix_axis is not 'x':
                state.left -= io.mouse_delta[0] / zoom_x
                state.right -= io.mouse_delta[0] / zoom_x
                changed |= True
            if state.fix_axis is not 'y':
                state.top -= io.mouse_delta[1] / zoom_y
                state.bottom -= io.mouse_delta[1] / zoom_y
                changed |= True

        # Zoom
        if is_hovered and io.mouse_wheel:
            factor = 1.3 ** io.mouse_wheel

            if state.fix_axis is not 'x':
                mx_rel = (io.mouse_pos[0] - origin[0]) / w * 2 - 1
                mx = mx_rel * (right - left) / (state.right - state.left) / 2 + 0.5
                wi = state.right - state.left
                state.left  = state.left    + wi * mx     - wi / factor * mx
                state.right = state.right   - wi * (1-mx) + wi / factor * (1-mx)
                changed |= True

            if state.fix_axis is not 'y':
                my_rel = (io.mouse_pos[1] - origin[1]) / h * 2 - 1
                my = my_rel * (bottom - top) / (state.bottom - state.top) / 2 + 0.5
                hi = state.bottom - state.top
                state.top  = state.top      + hi * my     - hi / factor * my
                state.bottom = state.bottom - hi * (1-my) + hi / factor * (1-my)
                changed |= True


        view_s = [origin[0], origin[1], origin[0] + w, origin[1] + h]
        view_i = [left, top, right, bottom]

        s2c = np.array( # Screen to Content
            [ [1 / zoom_x, 0, left - origin[0] / zoom_x]
            , [0, 1 / zoom_y, top  - origin[1] / zoom_y]
            ])

        i2s = np.array( # Content to Screen
            [ [zoom_x, 0, origin[0] - left * zoom_x]
            , [0, zoom_y, origin[1] - top  * zoom_y]
            ])

        imgui.begin_child("Pan-zoom container", w, h, False, flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)

        try:
            if content_gen is not None:
                next(content_gen(TF(i2s, s2c, view_i, view_s, is_hovered)))
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_child()
        if changed:
            return name, state
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
        self.is_dragging = False

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


class TF(object):
    """ Transformation object containing information necessary for converting between screen-space and image-space.

    Both screen-space and image-space are in pixels with top-left corner equal to (0, 0).
    Transformations are expressed as NumPy matrices in homogenous coordinates with two rows and three columns (shape: (2, 3)).

    For example, a point `[px, py]` can be transformed to screen-space by left multiplication:

    ```python
    q = np.matmul(i2s, [px, py, 1])
    ```

    Mostly, the necessary conversions are performed by overlay widgets.

    Attributes:
        i2s: Image-to-screen transformation matrix.
        s2i: Screen-to-image transformation matrix.
        view: Screen-space viewport coordinates as a list [left, top, right, bottom].
        hovered: `True` if the image widget is hovered over. Useful for some interactive elements,
            such as draggable widgets.
    """
    def __init__(self, i2s, s2i, view_i, view_s, hovered):
        self.i2s = i2s
        self.s2i = s2i
        self.view_i = view_i
        self.view_s = view_s
        self.hovered = hovered
