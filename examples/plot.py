#!/usr/bin/env python3

import concur as c
from PIL import Image
import numpy as np

def graph(show_polyline, n_verts, xlim, tf):
    while True:
        x = np.linspace(*xlim, n_verts, dtype=np.float32)
        y = np.sin(np.log2(np.abs(x)) * 10) * np.cos(np.log2(np.abs(x)) / 2)
        pts = np.stack([x, y]).T

        yield from c.optional(show_polyline, c.draw.polyline,
            pts,
            (0,0,0,1), thickness=1,
            tf=tf)


def app():
    view = c.plot.Frame((-1, 2), (1, -2), keep_aspect=False, fix_axis='y')
    show_polyline = True
    n_verts = 1e4
    adaptive_bounds = False

    while True:
        polyline_opts = lambda: c.orr(
            [ c.slider_float("n_verts", n_verts, 10, 1e5, power=10, format="%.0f")
            , c.checkbox("Adaptive Bounds", adaptive_bounds)
            ])
        tag, value = yield from c.orr(
            [ c.window("Graph", c.orr(
                [ c.plot.frame("Frame", view, c.partial(
                    graph, show_polyline, n_verts,
                    (view.left, view.right) if adaptive_bounds else (-1, 1)))
                ]))
            , c.window("Controls", c.orr(
                [ c.radio_button("Keep Aspect", view.keep_aspect)
                , c.radio_button("Fix X", view.fix_axis == 'x')
                , c.radio_button("Fix Y", view.fix_axis == 'y')
                , c.button("Reset View")
                , c.separator()

                , c.checkbox("Show Polyline", show_polyline)
                , c.optional(show_polyline, polyline_opts)
                ]))
            ])
        if tag == "Frame":
            view = value
            xlim = (view.left, view.right) if adaptive_bounds else (-1, 0)
        elif tag == "Reset View":
            view.reset_view()
        elif tag == "Keep Aspect":
            view.keep_aspect = abs((view.bottom - view.top) / (view.right - view.left))
            view.fix_axis = None
        elif tag == "Fix X":
            view.keep_aspect = False
            view.fix_axis = 'x'
        elif tag == "Fix Y":
            view.keep_aspect = False
            view.fix_axis = 'y'
        elif tag == "Show Polyline":
            show_polyline = value
        elif tag == "n_verts":
            n_verts = value
        elif tag == "Adaptive Bounds":
            adaptive_bounds = value
            xlim = (view.left, view.right) if adaptive_bounds else (-1, 0)

        yield


if __name__ == "__main__":
    c.main("Plot", app(), 800, 500)
