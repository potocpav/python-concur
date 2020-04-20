""" Scrollable, zoomable image widget with overlay support. """


import copy

import numpy as np
import imgui
from concur.widgets import child
from concur.draw import image as raw_image
from concur.extra_widgets.pan_zoom import PanZoom, pan_zoom
from concur.core import orr, optional


def image(name, state, width=None, height=None, content_gen=None, drag_tag=None, down_tag=None, hover_tag=None):
    """ The image widget.

    `state` is an instance of `concur.extra_widgets.image.Image`. Width and
    height are optional; if not specified, the widget stretches to fill
    the parent element. Returns a modified `Image` object tagged with `name` on user interaction.

    `content_gen` is a function that takes as an argument a transformation
    object `concur.extra_widgets.pan_zoom.TF`, and returns a widget that will be displayed as image
    overlay. Any events fired by the overlay widget are passed through unchanged.

    The transformation object can be used to position and scale the overlay widget appropriately.
    It can be used explicitly, or passed as the `tf` argument to any geometrical objects
    in `concur.draw`. Widgets which don't accept the `tf` arguments, such as buttons, can be
    wrapped inside the `concur.widgets.transform` widget.
    See the [image example](https://github.com/potocpav/python-concur/blob/master/examples/image.py) for example usage.

    It is very common to use `concur.partial` to pass additional arguments to the `content_gen` function:

    ```python
    def overlay(pos, tf):
        return c.draw.circle(*pos, 10, (0,0,0,1), tf=tf)

    _, im = yield from c.image("Image", im, content_gen=c.partial(overlay, pos))
    ```
    """
    def content_gen_with_image(tf, events=None):
        if drag_tag or down_tag or hover_tag:
            kwargs = dict(tf=tf, events=events)
        else:
            kwargs = dict(tf=tf)
        return orr([
            raw_image(state.tex_id, state.tex_w, state.tex_h, tf),
            optional(content_gen is not None, content_gen, **kwargs),
        ])

    while True:
        _, (st, child_event) = yield from pan_zoom(name, state.pan_zoom, width, height,
            content_gen=content_gen_with_image,
            drag_tag=drag_tag, down_tag=down_tag, hover_tag=hover_tag)
        if st is not None:
            new_state = copy.deepcopy(state)
            new_state.pan_zoom = st
            return name, new_state
        else:
            return child_event
        yield


class Image(object):
    """ Image state containing pan and zoom information, and texture data. """
    def __init__(self, image=None):
        """ `image ` must be something convertible to `numpy.array`: greyscale, RGB, or RGBA.
        Channel is in the last dimension.
        """
        # TODO: remove this hack with last_{w,h}; create a more principled way of changing content size
        self.last_w, self.last_h = None, None
        self.tex_id = None
        self.garbage_tex_id = None
        self.pan_zoom = PanZoom((0, 0), (1, 1))
        self.tex_uv_b = 1, 1
        self.change_image(image)

    def change_image(self, image):
        """ Change the image for a different one. `image ` must be None, or something convertible to
        `numpy.array` in greyscale, RGB, or RGBA format. Channel is in the last dimension.
        If None, a black placeholder image is displayed.

        `change_image` must be called at most once per each frame for one Image.
        For performance, it is beneficial to use NumPy textures:

        * with dimensions divisible by four,
        * with type `numpy.uint8`,
        * with three or four channels (RGB, RGBA),
        * in C order.

        Otherwise, the array will be copied & converted.
        """
        from concur.integrations.opengl import texture, rm_texture
        if self.garbage_tex_id is not None:
            rm_texture(self.garbage_tex_id)
            self.garbage_tex_id = None
        self.garbage_tex_id = self.tex_id # Hold onto the old texture ID for (at least) one frame
        if image is None:
            self.tex_id = texture(np.zeros((1,1,3)))
            self.tex_w, self.tex_h = 1, 1
        else:
            if not isinstance(image, np.ndarray):
                image = np.array(image) # support PyTorch tensors and PIL images

            assert len(image.shape) in [2, 3]
            w, h = image.shape[1], image.shape[0]
            if w % 4 or h % 4:
                # Expand weirdly shaped images
                nw, nh = w + (-w) % 4, h + (-h) % 4
                new_image = np.ones((nh, nw, image.shape[2]) if len(image.shape) == 3 else (nw, nh)) * 255
                new_image[:h, :w] = image
                self.tex_id = texture(new_image)
                self.tex_uv_b = w / nw, h / nh
            else:
                self.tex_id = texture(image)
                self.tex_uv_b = 1, 1

            self.tex_w, self.tex_h = w, h

            if self.last_w != self.tex_w or self.last_h != self.tex_h:
                self.last_w, self.last_h = self.tex_w, self.tex_h
                self.pan_zoom.reset_view((0,0), (self.tex_w, self.tex_h))

    def reset_view(self):
        """ Reset view so that the whole image fits into the widget. """
        return self.pan_zoom.reset_view()
