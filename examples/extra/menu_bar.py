#!/usr/bin/env python3

import concur as c


def app():
    while True:
        key, value = yield from c.orr([
            c.main_menu_bar(c.orr([
                c.menu("File", c.orr([
                    c.menu_item("New", "Ctrl+N"),
                    c.menu_item("Open...", "Ctrl+O"),
                    c.separator(),
                    c.menu_item("Quit", "Ctrl+Q"),
                    ])),
                ])),
            c.text("Try Ctrl+Q."),
            c.key_press("Quit", ord('Q'), ctrl=True),
            ])
        print(key, value)
        if key == "Quit":
            return
        yield


if __name__ == "__main__":
    c.main("Main Menu Bar", app(), 500, 500, menu_bar=True)
