#!/usr/bin/env python3

"""Show line rendering issues in ImGui."""


import concur as c
from PIL import Image
import numpy as np
import imgui


def graph(tex_id, tex_w, tex_h, tf):
    return c.orr([
        c.draw.polyline([(-1, 0), (0, 0), (0, -0.3), (0.3, 0), (1, 0.1), (-1, 0.5), (-1, 0.2)], (0,0,0,0.5),
        closed=True, thickness=20, tf=tf),
        ])


def app():
    view = c.plot.Frame((-1, -1), (1, 1), keep_aspect=True)
    arr = np.array(Image.open("examples/lenna.png"))
    tex = c.texture(arr)
    style = imgui.get_style()
    style.anti_aliased_lines = False

    while True:
        tag, value = yield from c.orr([
            c.window("Graph", c.plot.frame("Frame", view, c.partial(graph, tex, arr.shape[0], arr.shape[1]))),
            c.window("Controls", c.checkbox("Antialiasing", style.anti_aliased_lines)),
            ])
        if tag == "Frame":
            view = value
        elif tag == "Antialiasing":
            style.anti_aliased_lines = value
        yield


if __name__ == "__main__":
    c.main("Plot", app(), 800, 500)
