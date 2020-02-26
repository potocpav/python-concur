#!/usr/bin/env python3

import concur as c
import numpy as np

def graph(tf):
    x = np.linspace(-1, 1, 1000)
    y = np.sin(np.log2(np.abs(x)) * 10) * np.cos(np.log2(np.abs(x)) / 2)
    return c.draw.polyline(np.stack([x, y]).T, 'black', tf=tf)


def app():
    view = c.Frame((-1, 2), (1, -2), keep_aspect=False, fix_axis='y')
    while True:
        _, view = yield from c.frame("Frame", view, graph)
        yield


if __name__ == "__main__":
    c.main("Plot", app(), 800, 500)
