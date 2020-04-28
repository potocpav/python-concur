#!/usr/bin/env python3

"""Assortment of various widgets for testing purposes."""


import concur as c
from PIL import Image
import glfw


def app():
    im1 = c.Image(Image.open("examples/lenna.png"))
    im2 = c.Image(Image.open("examples/lenna.png"))

    while True:
        k, v = yield from c.orr([
            c.button("Hello,"),
            c.button("world!"),
            c.orr_same_line([
                c.text("Hello,"),
                c.nothing(),
                c.text_tooltip("Text tooltip", c.text("world!")),
                c.text_tooltip("Orr tooltip", c.orr([
                    c.text_tooltip("Button tooltip", c.button("Button1")),
                    c.button("Button2"),
                    ])),
                c.orr([
                    c.button("Button3"),
                    c.button("Button4"),
                    ]),
                c.text("Finish line."),
                ]),
            c.draggable("Drag", c.orr([c.button("Draggable Button"), c.forever(c.button, "Another")])),
            c.input_text("Hello", "world!", 123),
            c.collapsing_header("Image", c.orr([
                c.tooltip(c.orr([c.text("Hello!"), c.image("", im1, width=300, height=200), c.event(("Key", "Tooltip value"))]), c.image("Im1", im1, width=30, height=20)),
                c.image("Im2", im2, width=30, height=20),
                ])),
            c.input_text("Hello", "world!", 123),
            c.key_press("Key", glfw.KEY_SPACE),
            ])
        if k == "Im1":
            im1 = v
        if k == "Im2":
            im2 = v
        print(k, v)
        yield

if __name__ == "__main__":
    c.main("Counter", app(), 500, 500)
