#!/usr/bin/env python3

import concur as c
import numpy as np
import time


def graph(tf):
    t = time.monotonic()
    ts = np.linspace(t, t + 1/2, 100)
    x = np.sin(ts * 4)
    y = np.cos(ts * 5)
    return c.draw.polyline(np.stack([x, y]).T, (0,0,1,1), thickness=2, tf=tf)


def app():
    view = c.plot.Frame((-1.5, 1.5), (1.5, -1.5))
    while True:
        key, value = yield from c.orr([
            c.plot.frame("Frame", view, graph),
            c.event(("Tick", None)), # refresh every frame
            ])
        if key == "Frame":
            view = value
        yield


if __name__ == "__main__":
    c.main("Plot", app(), 500, 500)
