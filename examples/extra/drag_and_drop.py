#!/usr/bin/env python3

"""Demonstrate Drag and Drop."""


import concur as c


def app():
    while True:
        tag, value = yield from c.orr([
            c.text("Drag & drop example:"),
            c.drag_drop_source("Drag", 123, c.button("Hello, 123")),
            c.drag_drop_source("Drag", 456, c.text("Hello, 456")),
            c.drag_drop_target("Drag", c.button("Drop here"), value='abc'),
            c.drag_drop_target("Drag", c.button("or here"), value='def'),
            ])
        if tag == "Hello":
            print("Hello")
        elif tag == "Drag":
            print(value)
        yield


if __name__ == "__main__":
    c.main(app(), "Drag and Drop")
