import concur as c


@c.testing.test_widget
def test_orr_same_line(tester):
    res = yield from c.orr([
        c.orr_same_line([c.button("Apples"), tester.mark("X", c.button("Oranges"))]),
        tester.click_marked("X"),
        ])
    assert res == ("Oranges", None)


@c.testing.test_widget
def test_collapsing_header(tester):
    def ctrl():
        yield from tester.click_marked("H")
        yield from tester.click_marked("B")
    res = yield from c.orr([
        tester.mark("H", c.collapsing_header("Header",
            tester.mark("B", c.button("Button")), open=False)),
        ctrl(),
        ])
    assert res == ("Button", None)


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
def test_color_button(tester):
    res = yield from c.orr([
        tester.click_next(),
        c.color_button("This", (1, 0, 0, 1)),
        ])
    assert res == ("This", None)
    yield
    res = yield from c.orr([
        tester.click_next(),
        c.color_button("That", 'red', tag="Tag"),
        ])
    assert res == ("Tag", None)


@c.testing.test_widget
def test_radio_button(tester):
    res = yield from c.orr([
        tester.click_next(),
        c.radio_button("This", True),
        ])
    assert res == ("This", None)
    yield
    res = yield from c.orr([
        tester.click_next(),
        c.radio_button("That", False, tag="Tag"),
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


@c.testing.test_widget
def test_text_colored(tester):
    yield from c.orr([
        c.text_colored("This", 'blue'),
        c.text_colored("This", (1, 0, 0)),
        tester.pause(),
        ])
    yield


# @c.testing.test_widget
# def test_input_text(tester):
#     import glfw
#     def ctrl():
#         yield from tester.click_marked("T")
#         yield from tester.write_char(50)
#         yield from tester.pause()
#         yield from tester.write_char(20)
#         yield from tester.pause()
#         yield from c.nothing()
#     def widget():
#         text = ""
#         while True:
#             _, text = yield from c.input_text("Write something", text)
#             if text == "something":
#                 return text
#             yield
#     res = yield from c.orr([
#         tester.mark("T", widget()),
#         ctrl(),
#         ])
#
#     assert res == "something"


# @c.testing.test_widget
# def test_widgets(tester):
#     yield from _test_button(tester)
#     yield
#     yield from _test_checkbox(tester)
