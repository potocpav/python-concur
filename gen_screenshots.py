#!/usr/bin/env python3

import sys
import os
import concur as c
import numpy as np
from PIL import Image

examples_path = os.path.join(sys.path[0], "examples")
sys.path.append(examples_path)
import all


@c.testing.test_widget
def all_examples(tester):
    return c.orr([all.app(), tester.pause()])


@c.testing.test_widget
def hello_world(tester):
    return c.orr([c.text("Hello, world!"), tester.pause()])


@c.testing.test_widget
def counter(tester):
    def controlee():
        counter = 5
        while True:
            action, _ = yield from c.orr([
            c.text(f"Count: {counter}"),
            tester.mark("--", c.button("Decrement")),
            tester.mark("++", c.button("Increment")),
            ])
            if action == "Increment":
                counter += 1
            elif action == "Decrement":
                counter -= 1
            yield
    def controller():
        yield from tester.pause()
        yield from tester.click_marked("++", 40, 10)
        yield from tester.click_marked("--", 30, 10)
        yield from tester.click_marked("--", 30, 10)
        yield from tester.click_marked("++", 40, 10)
        yield from tester.move_cursor(100, 100)
    return c.orr([controlee(), controller()])


@c.testing.test_widget
def image(tester):
    def controlee():
        view = c.Image(Image.open("examples/lenna.png"))
        while True:
            _, view = yield from c.image("Image", view)
            yield
    def controller():
        yield from tester.pause(30)
        yield from tester.move_cursor(200, 150)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.move_cursor(210, 150)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(30)
        yield from tester.move_cursor(210, 200)

        yield from tester.mouse_dn(1)
        np.random.seed(0)
        for _ in range(5):
            yield from tester.move_cursor(np.random.randint(100, 200), np.random.randint(100, 200))
        yield from tester.move_cursor(210, 200)
        yield from tester.mouse_up(1)

        yield from tester.move_cursor(210, 150)
        yield from tester.pause(30)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.move_cursor(200, 150)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.move_cursor(100, 100)

    return c.orr([controlee(), controller()])


@c.testing.test_widget
def plot(tester):
    def controlee():
        def line(tf):
            np.random.seed(0)
            x = np.linspace(-2, 2, 10000)
            y = np.cumsum(np.random.rand(len(x)) - 0.5) / 100
            return c.draw.polyline(np.stack([x, y]).T, (0, 0, 1, 1), tf=tf)
        frame = c.Frame((-1, 1), (1, -1))
        while True:
            _, frame = yield from c.frame("Frame", frame, line)
            yield

    def controller():
        yield from tester.pause(30)
        yield from tester.move_cursor(200, 150)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.move_cursor(210, 150)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(10)
        yield from tester.scroll_up()
        yield from tester.pause(30)
        yield from tester.move_cursor(210, 200)

        yield from tester.mouse_dn(1)
        np.random.seed(0)
        for _ in range(5):
            yield from tester.move_cursor(np.random.randint(100, 200), np.random.randint(100, 200))
        yield from tester.move_cursor(210, 200)
        yield from tester.mouse_up(1)

        yield from tester.move_cursor(210, 150)
        yield from tester.pause(30)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.move_cursor(200, 150)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.pause(10)
        yield from tester.scroll_dn()
        yield from tester.move_cursor(100, 100)
    return c.orr([controlee(), controller()])


@c.testing.test_widget
def animation(tester):
    from time import monotonic as t
    def graph(tf):
        ts = np.linspace(t(), t() + 1/2, 100)
        pts = np.stack([np.sin(ts * 4), np.cos(ts * 5)]).T
        return c.draw.polyline(pts, (0,0,1,1), tf=tf)

    view = c.plot.Frame((-1.5, 1.5), (1.5, -1.5))
    t0 = t()
    while True:
        key, value = yield from c.orr([
            c.plot.frame("Frame", view, graph),
            c.event(("Tick", None)), # refresh every frame
            ])
        if key == "Frame":
            view = value
        if t() - t0 >= 2 * np.pi:
            break
        yield


if __name__ == "__main__":
    im = all_examples(width=800, height=560, return_sshot=True, draw_cursor=False)
    Image.fromarray(im[...,:3]).save('screenshot.png')

    im = hello_world(width=400, height=288, return_sshot=True, draw_cursor=False)
    Image.fromarray(im[...,:3]).save('docs/sshots/hello_world.png')

    counter(width=400, height=288, draw_cursor=True, save_screencast='docs/sshots/counter.mp4')

    image(width=400, height=288, draw_cursor=True, save_screencast='docs/sshots/image.mp4')

    plot(width=400, height=288, draw_cursor=True, save_screencast='docs/sshots/plot.mp4')

    animation(width=400, height=288, draw_cursor=False, save_screencast='docs/sshots/animation.mp4')
