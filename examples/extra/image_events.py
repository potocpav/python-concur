#!/usr/bin/env python3

import concur as c
from PIL import Image


def overlay(tf, events):
    while True:
        key, value = yield from c.orr([
            c.draw.line(20, 20, 20, 200, 'yellow', 2, tf=tf),
            c.draw.rect(40, 20, 100, 200, 'yellow', 2, 5, tf=tf),
            c.draw.circle(70, 110, 20, 'yellow', 2, 16, tf=tf),
            c.draw.text("Overlay text", 120, 20, 'blue', tf=tf),
            c.draw.polyline([(50, 30), (90, 30), (70, 50)], 'yellow', True, 2, tf=tf),
            c.transform(120, 50, c.button("Rotate"), tf=tf),
            c.transform(120, 80, c.button("Rotate"), tf=tf),
            events(),
            ])
        if key == "drag":
            print("Drag")
        elif key == "hover":
            print("Hover")
        elif key == "down":
            print("Down")
        else:
            return key, value
        yield


def app():
    image = Image.open("examples/lenna.png")
    view = c.Image(image)
    while True:
        tag, value = yield from c.orr([
            c.text("Drag using right mouse button,\nscroll using mouse wheel."),
            c.image("Image", view, content_gen=overlay, drag_tag="drag", hover_tag="hover", down_tag="down"),
            ])
        if tag == "Image":
            view = value
        elif tag == "Rotate":
            image = image.transpose(Image.ROTATE_270)
            view.change_image(image)
        else:
            print("leaked", tag, value)
        yield


if __name__ == "__main__":
    c.main("Image Events", app(), 500, 500)
