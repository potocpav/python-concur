#!/usr/bin/env python3

import concur as c
import concur.integrations.glfw as window

import time
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor()


def timer():
    while True:
        yield from c.orr([c.text(""), c.button("Start timer")])
        yield
        future = executor.submit(lambda: time.sleep(3))
        yield from c.orr([c.text("waiting for 3s..."), c.button("Cancel"), c.block(future)])
        yield


def app():
    return c.orr([timer() for _ in range(5)])


if __name__ == "__main__":
    window.main(app(), "Timers", 500, 500)
