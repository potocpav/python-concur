
import concur as c


class TimeControls(object):
    def __init__(self, start, end):
        self.frame_id = 0.0
        self.start = 0
        self.end = end - 1

def time_controls(state):
    tag, value = yield from c.window("Time Controls",
        [ c.slider_int("Frame ID", state.frame_id, state.start, state.end, tag="seek")
        , c.slider_float("Local Seek", 0, -1.5, 1.5, tag="drag")
        , c.orr_same_line(
            [ c.button("Next")
            , c.button("Prev")
            ])
        ])

    last_frame_id = state.frame_id
    if tag == "seek":
        state.frame_id = value
    elif tag == "drag":
        state.frame_id += 10 ** value - 10 ** (-value)
    elif tag == "Next":
        state.frame_id += 1
    elif tag == "Prev":
        state.frame_id -= 1
    else:
        raise ValueError(f"Unknown event tag: {tag}")

    state.frame_id = min(state.end, max(state.start, state.frame_id))
    if int(last_frame_id) != int(state.frame_id):
        event = int(state.frame_id)
    else:
        event = None
    return state, event
