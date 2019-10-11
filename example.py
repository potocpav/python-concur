
import imgui

import window_glfw as window
import concur as c

from concurrent.futures import ThreadPoolExecutor
import time

def choice():
    button = yield from c.orr([c.text("Choose:"), c.orr_same_line([c.button("Apple"), c.button("Orange"), c.button("Banana")])])
    yield
    yield from c.orr([c.text("Clicked " + button), c.button("Retry")])


def elm(state):
    event = yield from c.orr(
        [ c.tag('checkbox', c.checkbox("Checkbox", state['checkbox']))
        , c.tag('float', c.drag_float("Float", state['float']))
        , c.text(f"checkbox state: {state['checkbox']}, float state: {state['float']}")
        ])

    if event.tag == 'checkbox':
        state['checkbox'] = event.value
    elif event.tag == 'float':
        state['float'] = event.value
    else:
        raise ValueError
    return state

def timer_button():
    def wait():
        print('sleeping')
        time.sleep(3)
        print('slept')
    yield from c.button("Sleep for 3s")
    yield
    future = executor.submit(wait)
    yield from c.orr([c.text("Sleeping"), c.same_line(), c.button("Cancel"), c.block(future)])


executor = ThreadPoolExecutor(1)

initial_state = dict(checkbox=True, float=123.0)
view = c.window("Test Window",
    [ c.forever(choice)
    , c.separator()
    , c.stateful(elm, initial_state)
    , c.separator()
    , c.orr(
        [ c.forever(timer_button)
        , c.forever(timer_button)
        , c.forever(timer_button)
        , c.button("Cancel All")
        ])
    ])


if __name__ == "__main__":
    window.main(view)
