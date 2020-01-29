
import sys
import os
import concur as c

examples_path = os.path.join(sys.path[0], "..", "examples")
sys.path.append(examples_path)
import all

@c.testing.test_widget
def app(tester):
    return c.orr([all.app(), tester.pause()])

if __name__ == "__main__":
    im = app(width=800, height=560, return_sshot=True)
    im.save('test.png')
