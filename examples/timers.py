#!/usr/bin/env python3

import time
from concurrent.futures import ThreadPoolExecutor
import concur as c


executor = ThreadPoolExecutor()


def timer():
    yield from c.orr([c.text(""), c.button("Start timer")])
    yield
    future = executor.submit(lambda: time.sleep(3))
    yield from c.orr([c.text("waiting for 3s..."), c.button("Cancel"), c.Block(future)])


def app():
    return c.orr([c.forever(timer) for _ in range(3)])


if __name__ == "__main__":
    c.main("Timers", app(), 500, 500)
