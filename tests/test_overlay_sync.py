import concur as c
import numpy as np


@c.testing.test_widget
def app(tester):
    canvas = np.zeros([1000, 1000, 3], 'u1')
    im = c.Image(canvas)
    t = 0
    x, y = 0, 0
    for i in range(2):
        if i: yield
        res = yield from c.orr(
            [ c.image("", im, content_gen=lambda tf:
                c.draw.rect_filled(x-40, y-40, x+40, y+40, np.array([222, 111, 111, 255]) / 255, tf=tf))
            , c.event(None)
            ])
        t += 0.02
        x = int(500 + 400 * np.sin(t))
        y = int(500 + 400 * np.cos(t))
        canvas[...] = 0
        canvas[y-41:y+41, x-41:x+41] = [111, 222, 111]
        canvas[y-40:y+40, x-40:x+40] = [111, 111, 222]
        im.change_image(canvas)


def test_overlay_sync():
    "Test if the synchronization of overlay and image data is OK"
    im = np.array(app(save_screencast="vid.mkv", return_sshot=True))
    def contains(im, color):
        return np.any(np.all(im[...,:3] == color, axis=2))
    assert contains(im, [222, 111, 111]) == True
    assert contains(im, [111, 222, 111]) == True
    assert contains(im, [111, 111, 222]) == False
