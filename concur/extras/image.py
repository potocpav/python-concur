
from functools import partial
import copy

import imgui
from OpenGL.GL import *
from concur.integrations import replace_texture


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


def image(name, state, width=None, height=None, content_gen=None):
    while True:
        changed, state, im_to_screen, screen_to_im, hovered = \
            _image_begin(state, width, height)

        if content_gen is not None:
            try:
                next(content_gen(im_to_screen, screen_to_im, hovered))
            except StopIteration as e:
                _image_end()
                return name, ('content', e.value)

        _image_end()
        if changed:
            return name, ('view', state)
        else:
            yield


class ViewState(object):
    def __init__(self, center=(0.5, 0.5), zoom=1, is_dragging=False):
        self.default_center, self.default_zoom = center, zoom
        self.center, self.zoom, self.is_dragging = center, zoom, is_dragging
        self.tex_id = None
        self.tex_w, self.tex_h = None, None

    def change_image(self, image):
        self.tex_id = replace_texture(image, self.tex_id)
        self.tex_w, self.tex_h = image.shape[1], image.shape[0]

    def reset_view(self):
        self.center, self.zoom = self.default_center, self.default_zoom
