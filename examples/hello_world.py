#!/usr/bin/env python3

import concur as c
import imgui


def app():
    # make_next_win_fullscreen = c.lift(lambda: imgui.set_next_window_size(*imgui.get_io().display_size))
    return c.orr([
        c.window("Title", c.orr([
            c.button("Close"),
            ])),
        ])


if __name__ == "__main__":
    c.main(app(), "Hello World")
