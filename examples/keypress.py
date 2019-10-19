#!/usr/bin/env python3

import concur as c
import concur.integrations.glfw as window
import imgui
import glfw


def app():
    while True:
        key, _ = yield from c.orr([c.key_pressed("K", glfw.KEY_K)])
        yield
        print(key)


if __name__ == "__main__":
    window.main(app(), "Hello World", 500, 500)
