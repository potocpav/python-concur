#!/usr/bin/env python3

import concur as c
import counters, hello_world, timers, todo, keypress


def app():
    return c.orr([c.window(module.__name__, [module.app()]) for module in
        [ counters, hello_world, timers, todo, keypress]])


if __name__ == "__main__":
    c.integrations.main("All Examples", app(), 500, 500)
