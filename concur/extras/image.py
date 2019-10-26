""" Scrollable, zoomable image widget with overlay support. """
from functools import partial
import copy

import numpy as np
import imgui
from OpenGL.GL import *
from concur.integrations import replace_texture, texture


def _image_begin(state, width=None, height=None):
    """ A zoomable, draggable image widget.

    Three coordinate systems are in use in the widget:

     - screen space: measured in screen pixels, origin is in the top left corner
         of the widget.
     - image space: measured in texture pixels, origin is in the top left corner
         of the image.
     - GL space: origin is the same as for image space, but the scaling is
         different: (1,1) marks image's bottom right corner.
    """
    if width is None:
        width = imgui.get_content_region_available()[0]
    if height is None:
        height = imgui.get_content_region_available()[1]
    width = max(1, width)
    height = max(1, height)

    state = copy.deepcopy(state)

    draw_list = imgui.get_window_draw_list()
    pos = imgui.get_cursor_screen_pos()
    io = imgui.get_io()
    changed = False

    def screen_to_gl(pos, tex, view, center, zoom, x):
        tex_ratio = tex[0] / tex[1]
        view_ratio = view[0] / view[1]
        return max(1, view_ratio / tex_ratio) / zoom * ((x[0] - pos[0]) / view[0] - 0.5) + center[0], \
               max(1, tex_ratio / view_ratio) / zoom * ((x[1] - pos[1]) / view[1] - 0.5) + center[1]

    def gl_to_screen(pos, tex, view, center, zoom, x):
        tex_ratio = tex[0] / tex[1]
        view_ratio = view[0] / view[1]
        return ((x[0] - center[0]) * zoom / max(1, view_ratio / tex_ratio) + 0.5) * view[0] + pos.x, \
               ((x[1] - center[1]) * zoom / max(1, tex_ratio / view_ratio) + 0.5) * view[1] + pos.y

    scr_to_gl = partial(screen_to_gl, pos, (state.tex_w, state.tex_h), (width, height), state.center, state.zoom)
    gl_to_scr = partial(gl_to_screen, pos, (state.tex_w, state.tex_h), (width, height), state.center, state.zoom)

    tex_ratio = state.tex_w / state.tex_h
    view_ratio = width / height
    pixel = max(width / state.tex_w, height / state.tex_h) * state.zoom
    unit_x = min(width, height * tex_ratio) * state.zoom
    unit_y = min(height, width / tex_ratio) * state.zoom

    is_hovered = io.mouse_pos[0] < width + pos[0] and io.mouse_pos[0] > pos[0] and io.mouse_pos[1] < height + pos[1] and io.mouse_pos[1] > pos[1]

    if (imgui.is_mouse_clicked(1) or imgui.is_mouse_clicked(2)) and is_hovered:
        changed |= not state.is_dragging
        state.is_dragging = True
    if not (imgui.is_mouse_down(1) or imgui.is_mouse_down(2)):
        changed |= state.is_dragging
        state.is_dragging = False

    if state.is_dragging:
        state.center = state.center[0] - io.mouse_delta[0] / unit_x, state.center[1] - io.mouse_delta[1] / unit_y
        changed |= True

    if is_hovered:
        mx, my = scr_to_gl(io.mouse_pos)
        factor = 1.3 ** io.mouse_wheel
        state.zoom *= factor
        state.center = state.center[0] + (mx - state.center[0]) * (1 - 1 / factor), \
                 state.center[1] + (my - state.center[1]) * (1 - 1 / factor)
        changed |= io.mouse_wheel != 0

    uva = scr_to_gl(pos)
    uvb = scr_to_gl((pos[0] + width, pos[1] + height))

    if state.tex_id is not None:
        draw_list.add_image(state.tex_id, (pos.x, pos.y), (pos.x + width, pos.y + height), uva, uvb);

    imgui.push_clip_rect(*pos, pos[0] + width, pos[1] + height, True)

    return \
        changed, \
        state, \
        lambda x: gl_to_scr((x[0] / state.tex_w, x[1] / state.tex_h)), \
        lambda x: [a*b for a, b in zip(scr_to_gl(x), [state.tex_w, state.tex_h])], \
        is_hovered


def _image_end():
    imgui.pop_clip_rect()


class TF(object):
    """ Transformation object, relating screen space to image space, both in pixels. """
    def __init__(self, i2s, s2i, hovered):
        self.i2s = i2s
        self.s2i = s2i
        self.hovered = hovered


def image(name, state, width=None, height=None, content_gen=None):
    """ The image widget.

    `state` is an instance of `concur.extras.image.ViewState`. Width and
    height are optional; if not specified, the widget stretches to fill
    the parent element. Returns a modified `ViewState` object on user interaction.

    `content_gen` is a function that takes as an argument a transformation
    object `concur.extras.image.TF`, and returns a widget that will be displayed as image
    overlay. Any events fired by the overlay widget are passed through unchanged.

    The transformation object can be used to display overlay on the image, positioned
    and scaled appropriately. It can be used explicitly, or passed as the `tf` argument to any
    Geometrical objects. See the [image example](https://github.com/potocpav/python-concur/blob/master/examples/image.py) for example usage.
    """
    while True:
        changed, state, im_to_screen, screen_to_im, hovered = \
            _image_begin(state, width, height)

        if content_gen is not None:
            try:
                tf = TF(im_to_screen, screen_to_im, hovered)
                next(content_gen(tf))
            except StopIteration as e:
                _image_end()
                return e.value

        _image_end()
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
