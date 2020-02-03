#!/usr/bin/env python3

import concur as c
import imgui


def app():
    choices = [("Dark", imgui.style_colors_dark), ("Classic", imgui.style_colors_classic), ("Light", imgui.style_colors_light)]
    choice = "Dark"
    while True:
        ch, _ = yield from c.orr_same_line([c.radio_button(ch[0], choice == ch[0], tag=ch) for ch in choices])
        choice = ch[0]
        ch[1]()
        yield


if __name__ == "__main__":
    c.main("Hello World", app(), 500, 500)
