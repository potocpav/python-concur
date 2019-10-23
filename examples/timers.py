#!/usr/bin/env python3

import time
from concurrent.futures import ThreadPoolExecutor

import concur as c
import concur.integrations as window


executor = ThreadPoolExecutor()


def timer():
    while True:
        yield from c.orr([c.text(""), c.button("Start timer")])
        yield
        future = executor.submit(lambda: time.sleep(3))
        yield from c.orr([c.text("waiting for 3s..."), c.button("Cancel"), c.Block(future)])
        yield


def app():
    return c.orr([timer() for _ in range(5)])


if __name__ == "__main__":
    window.main("Timers", app(), 500, 500)
