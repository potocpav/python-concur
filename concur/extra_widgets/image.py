""" Scrollable, zoomable image widget with overlay support. """


from functools import partial
import copy

import numpy as np
import imgui
from OpenGL.GL import *
from concur.integrations import replace_texture, texture
from concur.widgets import child


def _image_begin(state, width, height):
    """ A zoomable, draggable image widget.

    Three coordinate systems are in use in the widget:

     - screen space: measured in screen pixels, origin is in the top left corner
         of the widget.
     - image space: measured in texture pixels, origin is in the top left corner
         of the image.
     - GL space: origin is the same as for image space, but the scaling is
         different: (1,1) marks image's bottom right corner.
    """
    state = copy.deepcopy(state)

    draw_list = imgui.get_window_draw_list()
    pos = imgui.get_cursor_screen_pos()
    io = imgui.get_io()
    changed = False

    tex_ratio = state.tex_w / state.tex_h
    view_ratio = width / height
    fact_x = max(1, view_ratio / tex_ratio) / state.zoom
    fact_y = max(1, tex_ratio / view_ratio) / state.zoom

    scr_to_gl = np.array(
        [ [fact_x / width,  0, state.center[0] - fact_x * (pos[0] / width + 0.5)]
        , [0, fact_y / height, state.center[1] - fact_y * (pos[1] / height + 0.5)]
        ])

    gl_to_scr = np.array(
        [ [width / fact_x,  0, (-state.center[0] / fact_x + 0.5) * width + pos[0]]
        , [0, height / fact_y, (-state.center[1] / fact_y + 0.5) * height + pos[1]]
        ])


    is_hovered = io.mouse_pos[0] < width + pos[0] and io.mouse_pos[0] > pos[0] and io.mouse_pos[1] < height + pos[1] and io.mouse_pos[1] > pos[1]

    if (imgui.is_mouse_clicked(1) or imgui.is_mouse_clicked(2)) and is_hovered:
        changed |= not state.is_dragging
        state.is_dragging = True
    if not (imgui.is_mouse_down(1) or imgui.is_mouse_down(2)):
        changed |= state.is_dragging
        state.is_dragging = False

    if state.is_dragging:
        unit_x = min(width, height * tex_ratio) * state.zoom
        unit_y = min(height, width / tex_ratio) * state.zoom
        state.center = state.center[0] - io.mouse_delta[0] / unit_x, state.center[1] - io.mouse_delta[1] / unit_y
        changed |= True

    if is_hovered:
        mx, my = np.matmul(scr_to_gl, [*io.mouse_pos, 1])
        factor = 1.3 ** io.mouse_wheel
        state.zoom *= factor
        state.center = state.center[0] + (mx - state.center[0]) * (1 - 1 / factor), \
                 state.center[1] + (my - state.center[1]) * (1 - 1 / factor)
        changed |= io.mouse_wheel != 0

    uva = np.matmul(scr_to_gl,  [*pos, 1])
    uvb = np.matmul(scr_to_gl,  [pos[0] + width, pos[1] + height, 1])

    # print(tuple(uva), uvb)

    if state.tex_id is not None:
        draw_list.add_image(state.tex_id, (pos.x, pos.y), (pos.x + width, pos.y + height), tuple(uva), tuple(uvb));

    # imgui.push_clip_rect(*pos, pos[0] + width, pos[1] + height, True)

    return \
        changed, \
        state, \
        gl_to_scr / [state.tex_w, state.tex_h, 1], \
        scr_to_gl * [[state.tex_w], [state.tex_h]], \
        is_hovered


def _image_end():
    pass
    # imgui.pop_clip_rect()


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
        hovered: `True` if the image widget is hovered over. Useful for some interactive elements,
            such as draggable widgets.
    """
    def __init__(self, i2s, s2i, hovered):
        self.i2s = i2s
        self.s2i = s2i
        self.hovered = hovered


def image(name, state, width=None, height=None, content_gen=None):
    """ The image widget.

    `state` is an instance of `concur.extra_widgets.image.ViewState`. Width and
    height are optional; if not specified, the widget stretches to fill
    the parent element. Returns a modified `ViewState` object on user interaction.

    `content_gen` is a function that takes as an argument a transformation
    object `concur.extra_widgets.image.TF`, and returns a widget that will be displayed as image
    overlay. Any events fired by the overlay widget are passed through unchanged.

    The transformation object can be used to display overlay on the image, positioned
    and scaled appropriately. It can be used explicitly, or passed as the `tf` argument to any
    Geometrical objects. See the [image example](https://github.com/potocpav/python-concur/blob/master/examples/image.py) for example usage.
    """
    while True:
        if width is None:
            w = imgui.get_content_region_available()[0]
        if height is None:
            h = imgui.get_content_region_available()[1]
        w = max(1, w)
        h = max(1, h)

        imgui.begin_child("Image container", w, h, False, flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)
        changed, state, im_to_screen, screen_to_im, hovered = \
            _image_begin(state, w, h)

        try:
            if content_gen is not None:
                tf = TF(im_to_screen, screen_to_im, hovered)
                next(content_gen(tf))
        except StopIteration as e:
            return e.value
        finally:
            _image_end()
            imgui.end_child()
        if changed:
            return name, state
        else:
            yield


class ViewState(object):
    """ Image state, contaiining pan and zoom information, and texture data. """
    def __init__(self, image=None, center=(0.5, 0.5), zoom=1):
        """ Initialize view state.

        `image` must be something convertible to `numpy.array`: greyscale or RGB, channel is
        in the last dimension.
        """
        import numpy as np
        self.default_center, self.default_zoom = center, zoom
        self.center, self.zoom = center, zoom
        self.is_dragging = False
        if image is None:
            self.tex_id = texture(np.zeros((1,1,3)))
            self.tex_w, self.tex_h = 1, 1
        else:
            self.tex_id = None
            self.change_image(image)

    def change_image(self, image):
        """ Change the image for a different one. `image` must be something convertible to
        `numpy.array`: greyscale or RGB, channel is in the last dimension.
        """
        image = np.array(image)
        self.tex_id = replace_texture(image, self.tex_id)
        self.tex_w, self.tex_h = image.shape[1], image.shape[0]

    def reset_view(self):
        """ Reset view so that the whole image fits into the widget. """
        self.center, self.zoom = self.default_center, self.default_zoom
