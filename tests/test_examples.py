
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
def test_menu_bar(tester):
    import extra.menu_bar as example
    yield from c.orr([example.app(), tester.pause()])
