#!/usr/bin/env python3

import concur as c
import counters, hello_world, image, plot, style, timers, todo


def app():
    return c.orr([c.window(module.__name__, module.app()) for module in
        [counters, hello_world, image, plot, style, timers, todo]])


if __name__ == "__main__":
    c.main("All Examples", app(), 800, 600)
