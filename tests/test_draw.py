import concur as c
import numpy as np



@c.testing.benchmark_widget
def test_polylines_perf():
    side, length = int(np.sqrt(10000)), 4
    x, y, t = np.meshgrid(np.linspace(0, 1, side), np.linspace(0, 1, side), np.linspace(0, 2 * np.pi, length, endpoint=False))
    polylines = np.stack([np.sin(t) * 1/side/2 + x, np.cos(t) * 1/side/2 + y], axis=3).reshape(-1, length, 2)
    im = c.Image()

    def content(tf):
        return c.draw.polylines(polylines, (1,1,1,1), tf=tf)
    while True:
        yield from c.image("Image", im, content_gen=content)
        yield
