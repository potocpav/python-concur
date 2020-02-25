#!/usr/bin/env python3

import concur as c
import time

def computation():
    def draw(i, tf):
        return c.orr([
            c.draw.circle(0, 0, 1, (1,0,0,1), tf=tf),
            c.draw.text(f"iter: {i}", 0, 0, (0,0,0,1), tf=tf)
            ])

    for i in range(2000000):
        yield c.partial(draw, i)
    print("Computation done.")

# c.quick_plot(computation())

def computation():
    def draw(i):
        return c.orr([
            c.button(f"i: {i}"),
            ])

    for i in range(20000):
        time.sleep(0.2)
        yield draw(i)
    print("Computation done.")

c.quick_window(computation())
