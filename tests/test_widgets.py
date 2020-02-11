import concur as c

def _test_button(tester):
    res = yield from c.orr([
        tester.click_next(),
        c.button("This"),
        ])
    assert res == ("This", None)
    yield
    res = yield from c.orr([
        tester.click_next(),
        c.button("That", tag="Tag"),
        ])
    assert res == ("Tag", None)

def _test_checkbox(tester):
    res = yield from c.orr([
        tester.click_next(),
        c.checkbox("This", True),
        ])
    assert res == ("This", False)
    yield
    res = yield from c.orr([
        tester.click_next(),
        c.checkbox("That", False, tag="Tag"),
        ])
    assert res == ("Tag", True)

# def 


@c.testing.test_widget
def test_widgets(tester):
    yield from _test_button(tester)
    yield
    yield from _test_checkbox(tester)
