import concur as c
from PIL import Image
import copy
from queue import Queue

import imgui
import numpy as np


def image_ui(q):
    i = 0
    im1 = c.Image(Image.open("examples/lenna.png"))
    im2 = copy.deepcopy(im1)
    while True:
        i += 1
        ret = yield from c.orr([c.listen(q), c.image("This", im2)])
        if ret is None:
            return im1, im2
        im2 = ret[1]
        yield


def is_viewport_close(im1, im2):
    return \
        np.isclose(im1.pan_zoom.top, im2.pan_zoom.top) and \
        np.isclose(im1.pan_zoom.left, im2.pan_zoom.left) and \
        np.isclose(im1.pan_zoom.right, im2.pan_zoom.right) and \
        np.isclose(im1.pan_zoom.bottom, im2.pan_zoom.bottom) and \
        True


@c.testing.test_widget
def test_viewport_scroll_identity(tester):
    def actions(q):
        yield from tester.move_cursor(100, 200)
        yield from tester.scroll_up()
        yield from tester.pause()
        yield from tester.scroll_dn()
        yield
        q.put(None)
        yield from c.nothing()

    q = Queue()
    im1, im2 = yield from c.orr([actions(q), image_ui(q)])
    assert is_viewport_close(im1, im2)


@c.testing.test_widget
def test_viewport_movement_identity(tester):
    def actions(q):
        yield from tester.move_cursor(100, 200)
        yield from tester.mouse_dn(1)
        yield from tester.move_cursor(200, 250)
        yield from tester.move_cursor(200, 200)
        yield from tester.mouse_up(1)
        yield from tester.move_cursor(300, 200)
        yield from tester.mouse_dn(2)
        yield from tester.move_cursor(250, 150)
        yield from tester.move_cursor(200, 200)
        yield from tester.mouse_up(2)
        yield
        q.put(None)
        yield from c.nothing()

    q = Queue()
    im1, im2 = yield from c.orr([actions(q), image_ui(q)])
    assert is_viewport_close(im1, im2)


@c.testing.test_widget
def test_viewport_movement_outside(tester):
    def actions(q):
        yield from tester.move_cursor(100, 100)
        yield from tester.mouse_dn(1)
        yield from tester.move_cursor(-100, 100)
        yield from tester.move_cursor(-100, 0)
        yield from tester.move_cursor(100, -100)
        yield from tester.move_cursor(100, 100)
        yield from tester.mouse_up(1)
        yield
        q.put(None)
        yield from c.nothing()

    q = Queue()
    im1, im2 = yield from c.orr([actions(q), image_ui(q)])
    assert is_viewport_close(im1, im2)


@c.testing.test_widget
def test_viewport_start_movement_outside(tester):
    def actions(q):
        yield from tester.move_cursor(50, 5)
        yield from tester.mouse_dn(1)
        yield from tester.move_cursor(100, 100)
        yield from tester.mouse_up(1)
        yield
        q.put(None)
        yield from c.nothing()

    q = Queue()
    im1, im2 = yield from c.orr([actions(q), image_ui(q)])
    assert is_viewport_close(im1, im2)


@c.testing.test_widget
def test_viewport_scroll_outside(tester):
    def actions1(q):
        yield from tester.move_cursor(-1, -1)
        yield from tester.scroll_up()
        yield
        q.put(None)
        yield from c.nothing()

    def actions2(q):
        yield from tester.move_cursor(100, 100)
        yield from tester.mouse_dn(1)
        yield from tester.move_cursor(-100, 100)
        yield from tester.scroll_up() # this should register and break the identity
        yield from tester.move_cursor(100, 100)
        yield from tester.mouse_up(1)
        yield
        q.put(None)
        yield from c.nothing()

    q = Queue()
    im1, im2 = yield from c.orr([actions1(q), image_ui(q)])
    assert is_viewport_close(im1, im2)
    im1, im3 = yield from c.orr([actions2(q), image_ui(q)])
    assert not is_viewport_close(im1, im3)


# FIXME: addition of window decorations into the test harness broke this test.
def test_npot_textures():
    """ Test non-power-of-two textures.

    Frequently, texture dimensions not divisible by four are corrupted. The Image
    widget should correctly wor around this by creating a larger texture.
    """
    @c.testing.test_widget
    def app(tester):
        m = np.ones((16, 32, 3), 'u1') * 0
        m[:, 7:20, 0] = 255
        im = c.Image(m)
        return c.orr([
            c.image("", c.Image(m[:,:28]), height=100),
            c.image("", c.Image(m[:,:29]), height=100),
            c.image("", c.Image(m[:,:30]), height=100),
            c.image("", c.Image(m[:,:31]), height=100),
            tester.pause(),
            ])
    im = np.array(app(return_sshot=True, draw_cursor=False))
    # assert np.all(im[...,[1,2]] < 50)
    # column_hot_counts = (im[:,:,0] == 255).sum(axis=0)
    # assert list(np.unique(column_hot_counts)) == [0, 100, 200, 300, 400]


def _test_events_generic(tester, state, widget):
    # Event-less
    yield from c.orr([
        widget("", state, content_gen=lambda tf: c.nothing()),
        tester.pause(),
        ])
    yield

    # Hover, immediate re-firing of the events by `content_gen`
    tag, _ = yield from c.orr([
        widget("", state, content_gen=lambda tf, event_gen: event_gen(), hover_tag="hover"),
        tester.move_cursor(50, 100),
        ])
    assert tag == "hover"
    yield

    # Mouse drag, no re-firing of events by `content_gen`. Drag is outside the image boundary
    def content_gen(tf, event_gen):
        dist_x = 0
        while dist_x < 200:
            key, value = yield from event_gen()
            if key == 'drag':
                print(tf.c2s)
                dist_x += value[0] * tf.c2s[0,0]
                print(dist_x)
            yield
        return "done", dist_x
    def drag():
        yield from tester.move_cursor(200, 100)
        yield
        yield from tester.mouse_dn(0)
        yield
        yield from tester.move_cursor(400, 100)
        yield
    key, value = yield from c.orr([
        widget("", state, width=300, height=300, content_gen=content_gen, drag_tag="drag"),
        drag(),
        ])
    assert key == "done" and value == 200.0
    yield
    yield from tester.mouse_up(0)
    yield

    # Mouse down precedes drag
    def content_gen(tf, event_gen):
        dragged=False
        while True:
            key, value = yield from event_gen()
            if key == 'down':
                assert not dragged
                dragged = True
            if key == 'drag':
                assert dragged
                return "done", None
            yield
    ev = yield from c.orr([
        widget("", state, width=300, height=300, content_gen=content_gen, down_tag="down", drag_tag="drag"),
        drag(),
        ])
    assert ev == ("done", None)


@c.testing.test_widget
def test_image_events(tester):
    im = c.Image(np.ones((150, 150, 3)) * 128)
    return _test_events_generic(tester, im, c.image)


@c.testing.test_widget
def test_frame_events(tester):
    frame = c.Frame((0, 0), (150, 150))
    return _test_events_generic(tester, frame, c.frame)
