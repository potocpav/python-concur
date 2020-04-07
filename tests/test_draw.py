import concur as c
import numpy as np



@c.testing.benchmark_widget
def test_polylines_perf():
    side, length = int(np.sqrt(10000)), 4
    x, y, t = np.meshgrid(np.linspace(0, 1, side), np.linspace(0, 1, side), np.linspace(0, 2 * np.pi, length, endpoint=False))
    polylines = np.stack([np.sin(t) * 1/side/2 + x, np.cos(t) * 1/side/2 + y], axis=3).reshape(-1, length, 2)
    im = c.Image()

    def content(tf):
        return c.draw.polylines(polylines, 'white', tf=tf)
    while True:
        yield from c.image("Image", im, content_gen=content)
        yield


@c.testing.test_widget
def test_scatter(tester):
    def content(tf):
        np.random.seed(0)
        return c.orr([
            c.draw.scatter(np.random.rand(100, 2), 'white', '+', thickness=1, tf=tf),
            c.draw.scatter(np.random.rand(100, 2), 'yellow', 'x', thickness=1, tf=tf),
            c.draw.scatter(np.random.rand(100, 2), 'magenta', 'o', thickness=1, tf=tf),
            c.draw.scatter(np.random.rand(100, 2), 'green', '.', marker_size=3, tf=tf),
            ])
    yield from c.orr([c.image("Image", c.Image(), content_gen=content), tester.pause()])


@c.testing.test_widget
def test_shapes(tester):
    def content(tf):
        np.random.seed(0)
        return c.orr([
            # Empty polygonal shapes of all kinds
            c.draw.polygon([], 'white', tf=tf),
            c.draw.polygon(np.array([]), 'white', tf=tf),
            c.draw.polygon(np.zeros((0, 2)), 'white', tf=tf),
            c.draw.polyline([], 'white', tf=tf),
            c.draw.polyline(np.array([]), 'white', tf=tf),
            c.draw.polyline(np.zeros((0, 2)), 'white', tf=tf),
            c.draw.polygons(np.zeros((0, 123, 2)), 'white', tf=tf),
            c.draw.polygons(np.zeros((123, 0, 2)), 'white', tf=tf),
            c.draw.polylines([], 'white', tf=tf),
            c.draw.polylines(np.zeros((0, 123, 2)), 'white', tf=tf),
            c.draw.polylines(np.zeros((123, 0, 2)), 'white', tf=tf),
            c.draw.scatter(np.array([]), 'white', 'x', tf=tf),
            c.draw.scatter(np.zeros([0]), 'white', 'x', tf=tf),
            c.draw.scatter(np.zeros([0,2]), 'white', 'x', tf=tf),

            # Normal polygonal shapes
            c.draw.polygon(np.array([(0.5,0.5), (0.7,0.5), (0.7,0.7), (0.5,0.7)]), 'white', tf=tf),
            c.draw.polygon([(0.5,0.5), (0.6,0.5), (0.6,0.6), (0.5,0.6)], 'brown', tf=tf),
            ])
    yield from c.orr([c.image("Image", c.Image(), content_gen=content), tester.pause()])
