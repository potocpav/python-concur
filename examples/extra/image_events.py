#!/usr/bin/env python3

import concur as c
from   copy import deepcopy
import numpy as np
from   PIL import Image


def overlay(lines, tf, event_gen=c.nothing):
    key, value = yield from c.orr([
        c.draw.polylines(np.array(lines), 'yellow', thickness=4, tf=tf),
        event_gen(),
        ])
    if key == "Drag":
        lines[-1][1] += value
    elif key == "Down":
        lines.append([value, value.copy()])
    return "Draw", lines


def app():
    view = c.Image(Image.open("examples/lenna.png"))
    lines = []
    while True:
        tag, value = yield from c.orr([
            c.text("Create lines by dragging with the left mouse button."),
            c.image("Image", view, content_gen=c.partial(overlay, deepcopy(lines)),
                drag_tag="Drag", down_tag="Down"),
            ])
        if tag == "Image":
            view = value
        elif tag == "Draw":
            lines = value
        yield


if __name__ == "__main__":
    c.main(app(), "Image Events")
