
import concur as c

# @c.testing.test_widget
def test_window_ids(tester):
    res = yield from c.orr(
        [ c.window("W1", c.button("W1"))
        , c.window("W1", c.button("W2"))
        ])


if __name__ == "__main__":
    c.integrations.main("Test", test_window_ids(None), 800, 560)
