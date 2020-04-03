#!/usr/bin/env python3

"""Show the highly experimental `quick_window` and `quick_plot` entry-points"""

import concur as c
import time

def computation():
    def draw(i, tf):
        return c.orr([
            c.draw.circle(0, 0, 1, 'red', tf=tf),
            c.draw.text(f"iter: {i}", 0, 0, 'black', tf=tf),
            ])

    for i in range(2000000):
        yield c.partial(draw, i)
    print("Computation done.")

# c.quick_plot(computation())

def computation():
    def draw(i):
        return c.orr([
            c.text(f"i: {i}"),
            ])

    for i in range(20000):
        time.sleep(0.2)
        yield draw(i)
    print("Computation done.")

c.quick_window(computation(), 500, 500)
