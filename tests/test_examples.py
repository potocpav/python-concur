
import sys
import os
import concur as c


examples_path = os.path.join(sys.path[0], "..", "examples")
sys.path.append(examples_path)


@c.testing.test_widget
def test_all_examples(tester):
    import all as example
    yield from c.orr([example.app(), tester.pause()])


@c.testing.test_widget
def test_columns(tester):
    import extra.columns as example
    yield from c.orr([example.app(), tester.pause()])

@c.testing.test_widget
def test_image_events(tester):
    import extra.image_events as example
    yield from c.orr([example.app(), tester.pause()])

@c.testing.test_widget
def test_menu_bar(tester):
    import extra.menu_bar as example
    yield from c.orr([example.app(), tester.pause()])

@c.testing.test_widget
def test_plot_image(tester):
    import extra.plot_image as example
    yield from c.orr([example.app(), tester.pause()])

@c.testing.test_widget
def test_polyline(tester):
    import extra.polyline as example
    yield from c.orr([example.app(), tester.pause()])

# This test is broken
# @c.testing.test_widget
# def test_quick_plot(tester):
#     import extra.quick_plot as example
#     yield from c.orr([example.app(), tester.pause()])

@c.testing.test_widget
def test_widgets(tester):
    import extra.widgets as example
    yield from c.orr([example.app(), tester.pause()])
