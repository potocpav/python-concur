#!/usr/bin/env python3

import concur as c
from PIL import Image
import numpy as np

def graph(tex_id, tex_w, tex_h, tf):
    x = np.linspace(0, 512, 10000, dtype=np.float32)
    y = np.sin(np.log2(np.abs(x)) * 10) * np.cos(np.log2(np.abs(x)) / 2) * 256 + 256
    pts = np.stack([x, y]).T

    return c.orr(
        [ c.draw.image(tex_id, tex_w, tex_h, tf=tf)
        , c.draw.polyline(pts, (1,1,0,1), thickness=1, tf=tf)
        , c.draw.rect(0, 0, 512, 512, (1,1,1,1), tf=tf)
        ])


def app():
    view = c.plot.Frame((0, 0), (512, 512), keep_aspect=True)
    arr = np.array(Image.open("examples/lenna.png"))
    tex = c.texture(arr)

    while True:
        tag, value = yield from c.orr(
            [ c.window("Graph", c.plot.frame("Frame", view, c.partial(graph, tex, arr.shape[0], arr.shape[1])))
            , c.window("Controls", c.button("Reset View"))
            ])
        if tag == "Frame":
            view = value
        elif tag == "Reset View":
            view.reset_view()
        yield


if __name__ == "__main__":
    c.integrations.main("Plot", app(), 800, 500)
