
import sys
import os
import concur as c


examples_path = os.path.join(sys.path[0], "..", "examples")
sys.path.append(examples_path)
import all


@c.testing.test_widget
def test_all_examples(tester):
    yield from c.orr([all.app(), tester.pause()])


def test_glfw():
    def pause():
        yield
        yield
    c.main("GLFW Test", c.orr([all.app(), pause()]), 800, 600)
