import concur as c
from PIL import Image
import copy

import imgui
import numpy as np


@c.testing.test_widget
def test_viewport_movement(tester):
    def control():
        yield from tester.move_cursor(100, 200)
        yield from tester.scroll_up()
        yield from tester.pause()
        yield from tester.scroll_dn()
        # initial state
        yield from tester.pause()
        yield from tester.mouse_dn(1)
        yield from tester.move_cursor(200, 250)
        yield from tester.move_cursor(200, 200)
        yield from tester.mouse_up(1)
        yield from tester.move_cursor(300, 200)
        yield from tester.mouse_dn(2)
        yield from tester.move_cursor(250, 150)
        yield from tester.move_cursor(200, 200)
        yield from tester.mouse_up(2)
        # initial state
        # yield from c.nothing()

    def ui():
        im = c.Image(Image.open("examples/lenna.png"))
        i = 0
        im_old = copy.deepcopy(im)

        while True:
            i += 1
            tag, im = yield from c.image("This", im)

            if i == 2:
                print(im.pan_zoom.__dict__, im_old.pan_zoom.__dict__)
                assert np.isclose(im.pan_zoom.top, im_old.pan_zoom.top)
                assert np.isclose(im.pan_zoom.left, im_old.pan_zoom.left)
                assert np.isclose(im.pan_zoom.right, im_old.pan_zoom.right)
                assert np.isclose(im.pan_zoom.bottom, im_old.pan_zoom.bottom)
            yield

    yield from c.orr([control(), ui()])
