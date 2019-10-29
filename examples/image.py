#!/usr/bin/env python3

import concur as c
from PIL import Image


def overlay(tf):
    return c.orr(
        [ c.draw.line(20, 20, 20, 200, (1,1,0,1), 2, tf=tf)
        , c.draw.rect(40, 20, 100, 200, (1,1,0,1), 2, 5, tf=tf)
        , c.draw.circle(70, 110, 20, (1,1,0,1), 2, 16, tf=tf)
        , c.draw.text(120, 20, (1,1,1,1), "Overlay text", tf=tf)
        ])


def app():
    view = c.extras.ViewState(Image.open("examples/lenna.png"))
    while True:
        tag, value = yield from c.orr(
            [ c.text("Drag using right mouse button,\nscroll using mouse wheel.")
            , c.extras.image("Image", view, content_gen=overlay)
            ])
        view = value
        yield


if __name__ == "__main__":
    c.integrations.main("Image Viewer", app(), 500, 500)
