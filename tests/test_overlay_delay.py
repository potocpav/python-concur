import concur as c
import numpy as np


# FIXME: turn into a real test by capturing screen and checking for colored pixels on desync
@c.testing.test_widget
def disabled_test_overlay_delay(tester):
    canvas = np.zeros([1000, 1000], 'u1')
    # canvas[50:60, 50:60] = 255
    canvas.dtype
    im = c.Image(canvas)
    t = 0
    x, y = 0, 0
    while True:
        res = yield from c.orr(
            [ c.image("", im, content_gen=lambda tf: c.draw.circle(x, y, 50, (0, 255, 0, 255), tf=tf))
            , c.event(None)
            ])
        if res == "Stop":
            break
        print(res)
        t += 0.02
        x = int(500 + 400 * np.sin(t))
        y = int(500 + 400 * np.cos(t))
        canvas[...] = 0
        canvas[y-50:y+50, x-50:x+50] = 255
        im.change_image(canvas)
        yield

if __name__ == '__main__':
    disabled_test_overlay_delay()
