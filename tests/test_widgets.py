#!/usr/bin/env python3

import concur as c
import pytest


slow = False


def test_button():
    def widget(tester):
        res = yield from c.orr(
            [ tester.click_next()
            , c.button("This")
            ])
        assert res == ("This", None)
        yield
        res = yield from c.orr(
            [ tester.click_next()
            , c.button("That", tag="Tag")
            ])
        assert res == ("Tag", None)
    c.testing.test(widget, slow)


def test_checkbox():
    def widget(tester):
        res = yield from c.orr(
            [ tester.click_next()
            , c.checkbox("This", True)
            ])
        assert res == ("This", False)
        yield
        res = yield from c.orr(
            [ tester.click_next()
            , c.checkbox("That", False, tag="Tag")
            ])
        assert res == ("Tag", True)
    c.testing.test(widget, slow)
