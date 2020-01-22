""" Experimental widget for image sequence or video seeking. """


import concur as c


class TimeControls(object):
    """ State for the `concur.extra_widgets.time_controls.time_controls` widget. """
    def __init__(self, start, end, frame_id, hotkey=None):
        """ Initialize. """
        self.frame_id = frame_id
        self.start = start
        self.end = end - 1
        self.playing = False
        self.stride = 10
        self.hotkey = hotkey

def time_controls(state):
    """ Experimental widget for image sequence or video seeking.

    Takes `concur.extra_widgets.time_controls.TimeControls` as an argument. Returns a pair `(state, frame_id)`, where `state`
    is the modified `TimeControls` struct, and `frame_id` is an integer signalling a new position in the video frame,
    or `None` if user didn't seek.
    """
    def clock():
        return "tick", None
        yield

    tag, value = yield from c.window("Time Controls", c.orr(
        [ c.slider_int("Frame ID", state.frame_id, state.start, state.end, tag="seek")
        , c.slider_float("Local Seek", 0, -1.5, 1.5, tag="drag")
        , c.slider_int("Stride", state.stride, 1, 20, tag="stride")
        , c.orr_same_line(
            [ c.button("Next")
            , c.button("Prev")
            , c.button("Pause" if state.playing else "Play", tag="PlayPause")
            ])
        ]
         + ([] if not state.playing else [clock()]))
        )

    last_frame_id = state.frame_id
    if tag == "seek":
        state.frame_id = value
    elif tag == "drag":
        state.frame_id += 10 ** value - 10 ** (-value)
    elif tag == "stride":
        state.stride = value
    elif tag == "Next":
        state.frame_id += 1
    elif tag == "Prev":
        state.frame_id -= 1
    elif tag == "PlayPause":
        state.playing = not state.playing
    elif tag == "space":
        state.playing = not state.playing
    elif tag == "tick":
        state.frame_id += state.stride
    else:
        raise ValueError(f"Unknown event tag: {tag}")


    state.frame_id = min(state.end, max(state.start, state.frame_id))
    if int(last_frame_id) != int(state.frame_id):
        event = int(state.frame_id)
    else:
        event = None
    return state, event
