import concur as c


@c.testing.test_widget
def test_button(tester):
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


@c.testing.test_widget
def test_checkbox(tester):
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
