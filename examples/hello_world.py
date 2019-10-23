#!/usr/bin/env python3

import concur as c


def app():
    while True:
        yield from c.button("Hello!")
        yield
        yield from c.orr([c.text("Hello, world!"), c.button("Restart?")])
        yield


if __name__ == "__main__":
    c.integrations.main("Hello World", app(), 500, 500)
