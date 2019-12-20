#!/usr/bin/env python3

import concur as c
from PIL import Image
import numpy as np


x = np.linspace(0, 10, 100000, dtype=np.float32)
y = np.sin(x) * np.sin(x * 5 * np.cos(x))
pts = np.stack([x, y]).T


def graph(tf):
    return c.draw.polyline(
        pts,
        (0,0,0,1), thickness=1,
        tf=tf)


def app():
    image = Image.open("examples/lenna.png")
    view = c.plot.Frame((0, 2), (10, -2), keep_aspect=False, fix_axis=None)
    while True:
        tag, value = yield from c.orr(
            [ c.text("Drag using right mouse button,\nscroll using mouse wheel.")
            , c.plot.frame("Frame", view, graph)
            ])
        if tag == "Frame":
            view = value
        elif tag == "Rotate":
            image = image.transpose(Image.ROTATE_270)
            view.change_image(image)
        yield


if __name__ == "__main__":
    c.integrations.main("Plot", app(), 500, 500)
