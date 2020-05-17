#!/usr/bin/env python3

"""Show line rendering issues in ImGui."""


import concur as c
import imgui


def graph(tf):
    return c.draw.polyline([(-1, 0), (0, 0), (0, -0.3), (0.3, 0), (1, 0.1), (-1, 0.5), (-1, 0.2)], ('black', 0.5), closed=True, thickness=20, tf=tf)


def app():
    view = c.Frame((-1, -1), (1, 1), keep_aspect=True)
    style = imgui.get_style()
    style.anti_aliased_lines = False

    while True:
        tag, value = yield from c.orr([
            c.window("Graph", c.frame("Frame", view, content_gen=graph)),
            c.window("Controls", c.checkbox("Antialiasing", style.anti_aliased_lines)),
            ])
        if tag == "Frame":
            view = value
        elif tag == "Antialiasing":
            style.anti_aliased_lines = value
        yield


if __name__ == "__main__":
    c.main(app(), "Plot")
