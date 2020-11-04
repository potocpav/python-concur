#!/usr/bin/env python3

import concur as c

class DemoState(object):
    def __init__(self):
        pass

def demo_window(state):
    while True:
        tag, value = yield from c.window("Concur Demo", c.orr([
            c.text("Concur says hello. (TODO: version)"),
            c.collapsing_header("Help", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Configuration", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Window options", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Widgets", c.orr([
                c.tree_node("Basic", c.orr([
                    c.button("Button"),
                    ]), False),
                ]), False),
            c.collapsing_header("Layout & Scrolling", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Popups & Modal windows", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Columns", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Filtering", c.orr([
                c.text("Not implemented."),
                ]), False),
            c.collapsing_header("Inputs, Navigation & Focus", c.orr([
                c.text("Not implemented."),
                ]), False),
            ]))
        yield


def hello_world():
    show_demo_window = True
    demo_state = DemoState()
    show_another_window = False
    float = 0.0
    counter = 0
    while True:
        tag, value = yield from c.orr([
            c.window("Hello, world!", c.orr([
                c.text("This is some useful text."),
                c.checkbox("Demo Window", show_demo_window),
                c.checkbox("Another Window", show_another_window),
                c.slider_float("Float", float, 0, 1),
                # Not implemented: background color chooser
                c.orr_same_line([c.button("Button"), c.text(f"counter = {counter}")]),
                # Not implemented: FPS counter
                ])),
            c.optional(show_another_window, lambda: c.window("Another Window", c.orr([
                c.text("Hello from another window!"),
                c.button("Close Me"),
                ]))),
            c.optional(show_demo_window, c.partial(demo_window, demo_state)),
            ])
        if tag == "Demo Window":
            show_demo_window = value
        elif tag == "Another Window":
            show_another_window = value
        elif tag == "Float":
            float = value
        elif tag == "Button":
            counter += 1

        elif tag == "Close Me":
            show_another_window = False
        yield


if __name__ == "__main__":
    c.main(hello_world(), "Concur Demo Application", 1200, 800)
