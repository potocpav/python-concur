#!/usr/bin/env python3

import concur as c
import numpy as np
from time import monotonic as t

def graph(tf):
    ts = np.linspace(t(), t() + 1/2, 100)
    pts = np.stack([np.sin(ts * 4), np.cos(ts * 5)]).T
    return c.draw.polyline(pts, 'blue', tf=tf)

def app():
    view = c.Frame((-1.5, 1.5), (1.5, -1.5))
    while True:
        key, value = yield from c.orr([
            c.frame("Frame", view, graph),
            c.event(("Tick", None)), # refresh every frame
            ])
        if key == "Frame":
            view = value
        yield

if __name__ == "__main__":
    c.main("Plot", app(), 400, 288)
