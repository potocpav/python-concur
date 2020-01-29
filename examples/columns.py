#!/usr/bin/env python3

import concur as c


def app():
    return c.columns(
        [ [c.text("Hello,"), c.button("Click me")]
        , [c.text("columns!"), c.button("Or me")]
        ], "start", True)


if __name__ == "__main__":
    c.integrations.main("Columns", app(), 500, 500)