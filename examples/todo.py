#!/usr/bin/env python3

import concur as c
import imgui


def item(text, active):
    return c.orr_same_line([c.button("-"), c.checkbox(text, active, tag="toggle")])


def app():
    todos = [("Write a Todo app", True), ("Take out garbage", False)]
    disp = [True, False]
    edited = ""

    while True:
        action, value = yield from c.orr(
            [ c.orr_same_line([c.button("All"), c.button("Active"), c.button("Completed")])
            , c.orr([c.tag(i, item(s, a)) for i, (s, a) in enumerate(todos) if a in disp])
            , c.orr_same_line([c.button("+"), c.input_text("New Item", edited, 30)])
            ])
        # print(action, value)
        if action == "New Item":
            edited = value
        elif action == "+" and edited:
            todos.append((edited, False))
            edited = ""
        elif action in ["All", "Active", "Completed"]:
            disp = dict(All=[True, False], Active=[False], Completed=[True])[action]
        elif isinstance(action, int):
            if value[0] == '-':
                del todos[action]
            elif value[0] == 'toggle':
                todos[action] = todos[action][0], value[1]
        yield


if __name__ == "__main__":
    c.integrations.main("Todo List", app(), 500, 500)
