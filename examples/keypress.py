#!/usr/bin/env python3

import concur as c
import glfw


def app():
    count = 0
    while True:
        yield from c.orr([c.key_pressed("K", glfw.KEY_K), c.text(f"Key 'K' pressed {count} times")])
        yield
        count += 1


if __name__ == "__main__":
    c.integrations.main("Keypress", app(), 500, 500)
