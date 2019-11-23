#!/usr/bin/env python3

import concur as c
import imgui
import counters, hello_world, image, style, timers, todo


def app():
    return c.orr([c.window(module.__name__, module.app()) for module in
        [ counters, hello_world, image, style, timers, todo,]])


if __name__ == "__main__":
    c.integrations.main("All Examples", app(), 800, 560)
