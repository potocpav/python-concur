
#!/usr/bin/env python3

import threading
import queue
import time

from concur.integrations.glfw import main
from concur.core import listen, tag, multi_orr
from concur.extra_widgets.frame import frame, Frame


def thread(c, q, quit_q):
    t0 = 0
    try:
        for x in c:
            t1 = time.perf_counter()
            time.sleep(0)
            if t1 - t0 > 1/60:
                try:
                    q.put_nowait(x)
                except queue.Full:
                    pass
                t0 = t1
    finally:
        quit_q.put(None)

def quick_plot_window(quit_q, q, x0):
    counter = 0
    frame_st = Frame((-1, -1), (1, 1))
    content_gen = x0
    while True:
        events = yield from multi_orr([
            tag("Quit", listen(quit_q)),
            frame("Frame", frame_st, content_gen=content_gen),
            tag("Queue", listen(q)),
            ])
        for tag_, value in events:
            if tag_ == "Queue":
                content_gen = value
            elif tag_ == "Frame":
                frame_st = value
            elif tag_ == "Quit":
                return
        yield


def quick_plot(overlay_gen):
    q = queue.Queue(1)
    quit_q = queue.Queue(1)
    t = threading.Thread(target=thread, args=(overlay_gen, q, quit_q))

    t.start()
    x0 = q.get()
    main("Quick Plot", quick_plot_window(quit_q, q, x0), 500, 500)
