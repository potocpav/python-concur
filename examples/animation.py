#!/usr/bin/env python3

import concur as c
import numpy as np
from time import monotonic as t


def graph(tf):
    while True:
        ts = np.linspace(t(), t() + 1/2, 100)
        pts = np.stack([np.sin(ts * 4), np.cos(ts * 5)]).T
        yield from c.orr([
            c.draw.polyline(pts, 'blue', tf=tf),
            c.event(None), # refresh every frame
            ])
        yield


def app():
    view = c.Frame((-1.5, 1.5), (1.5, -1.5))
    while True:
        _, view = yield from c.frame("Frame", view, content_gen=graph)
        yield


if __name__ == "__main__":
    c.main(app(), "Plot", 400, 288)
