
import concur as c
import concur.integrations.glfw as window

import counters
import hello_world
import timers
import todo


def app():
    return c.orr([c.window(module.__name__, [module.app()]) for module in
        [ counters, hello_world, timers, todo]])


if __name__ == "__main__":
    window.main(app(), "All Examples", 500, 500)
