#!/usr/bin/env python3

import concur as c
import concur.integrations.glfw as window
import imgui
import glfw


def key_press(key_index, repeat=True, tag=None):
    while True:
        if imgui.is_key_pressed(key_index, repeat):
            return tag
        yield

def app():
    while True:
        key = yield from c.orr([key_press(glfw.KEY_K)])
        yield
        print(key)


if __name__ == "__main__":
    window.main(app(), "Hello World", 500, 500)
