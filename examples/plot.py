#!/usr/bin/env python3

import concur as c
from PIL import Image
import numpy as np


def foo(tf):
    return c.draw.polyline([(x,np.sin(x) * np.sin(x * 5 * np.cos(x))) for x in np.linspace(0, 10, 1000)], (0,0,0,1), tf=tf)


def app():
    image = Image.open("examples/lenna.png")
    view = c.plot.Frame((-1, 1.5), (10.5, -1.5), keep_aspect=False)
    while True:
        tag, value = yield from c.orr(
            [ c.text("Drag using right mouse button,\nscroll using mouse wheel.")
            , c.plot.frame(view, foo)
            ])
        if tag == "Frame":
            view = value
        elif tag == "Rotate":
            image = image.transpose(Image.ROTATE_270)
            view.change_image(image)
        yield


if __name__ == "__main__":
    c.integrations.main("Plot", app(), 500, 500)
