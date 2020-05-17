#!/usr/bin/env python3

import concur as c


def item(text, active):
    return c.orr_same_line([c.button("-"), c.checkbox(text, active, tag="toggle")])


def app():
    todos = [("Write a Todo app", True), ("Take out garbage", False)]
    disp = [True, False]
    edited = ""

    while True:
        tag, value = yield from c.orr([
            c.orr_same_line([c.button("All"), c.button("Active"), c.button("Completed")]),
            c.orr([c.tag_value(i, item(s, a)) for i, (s, a) in enumerate(todos) if a in disp]),
            c.orr_same_line([c.button("+"), c.input_text("New Item", edited, 30)]),
            ])
        if tag == "New Item":
            edited = value
        elif tag == "+" and edited:
            todos.append((edited, False))
            edited = ""
        elif tag in ["All", "Active", "Completed"]:
            disp = dict(All=[True, False], Active=[False], Completed=[True])[tag]
        elif tag == "-":
            del todos[value[0]]
        elif tag == "toggle":
            todos[value[0]] = todos[value[0]][0], value[1]
        yield


if __name__ == "__main__":
    c.main(app(), "Todo List")
