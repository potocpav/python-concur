

from functools import partial
import imgui
import numpy as np

from concur.extra_widgets.pan_zoom import PanZoom, pan_zoom
import concur.draw as draw
from concur.core import lift, orr, optional, map


# NOTE: the plotting functions require a forked version of ImGui:
# https://github.com/potocpav/pyimgui

margins = [50, 10, -10, -20]


class Frame(PanZoom):
    def __init__(self, top_left, bottom_right, keep_aspect=True, fix_axis=None):
        super().__init__(top_left, bottom_right, keep_aspect=keep_aspect, fix_axis=fix_axis, margins=margins)


def _frame(content_gen, tf):

    min_tick_spacing=50
    viewport_s = [r + o for r, o in zip(tf.view_s, margins)]
    viewport_c = np.concatenate([np.matmul(tf.s2c, [*viewport_s[:2], 1])[:2], np.matmul(tf.s2c, [*viewport_s[2:], 1])[:2]])
    bg = draw.rect_filled(*tf.view_s, (1,1,1,1))
    if viewport_s[2] <= viewport_s[0] or viewport_s[3] <= viewport_s[1]:
        return bg

    def ticks(a, b, max_n_ticks):
        a, b = min(a, b), max(a, b)
        w = b - a
        min_sep = w / max_n_ticks
        candidates = np.array([10 ** np.floor(np.log10(min_sep)) * f for f in [1, 2, 5, 10]])
        sep = candidates[candidates > min_sep]
        if len(sep) == 0:
            return []
        else:
            sep = sep[0]
            return np.arange(np.ceil(a / sep) * sep, b + 1e-10, sep)

    hticks_c = ticks(viewport_c[3], viewport_c[1], (viewport_s[3] - viewport_s[1]) / min_tick_spacing)
    vticks_c = ticks(viewport_c[2], viewport_c[0], (viewport_s[2] - viewport_s[0]) / min_tick_spacing)
    hticks_s = np.matmul(tf.c2s, np.stack([np.zeros_like(hticks_c), hticks_c, np.ones_like(hticks_c)]))[1]
    vticks_s = np.matmul(tf.c2s, np.stack([vticks_c, np.zeros_like(vticks_c), np.ones_like(vticks_c)]))[0]

    def tick_labels(format=("{:<6.1g}", "{:>6.1g}")):
        if isinstance(format, str):
            format = (format, format)
        xtick_labels = [draw.text(ts, viewport_s[3], (0,0,0,1), format[0].format(tc)) for ts, tc in zip(vticks_s, vticks_c)]
        ytick_labels = [draw.text(viewport_s[0] - 45, ts - 7, (0,0,0,1), format[1].format(tc)) for ts, tc in zip(hticks_s, hticks_c)]
        return orr(xtick_labels + ytick_labels)

    def grid():
        hlines = [draw.line(tf.view_s[0], tick, tf.view_s[2], tick, (0,0,0,0.3)) for tick in hticks_s]
        vlines = [draw.line(tick, tf.view_s[1], tick, tf.view_s[3], (0,0,0,0.3)) for tick in vticks_s]
        return orr(hlines + vlines)

    return orr(
        [ bg
        , draw.rect(*viewport_s, (0,0,0,1))
        , tick_labels()
        , lift(imgui.push_clip_rect, *viewport_s, True)
        , optional(content_gen is not None, content_gen, tf)
        , grid()
        , lift(imgui.pop_clip_rect)
        ])


def frame(name, state, content_gen=None):
    return map(lambda v: ((v[0], v[1][0]) if v[1][0] is not None else v[1][1]),
        pan_zoom(name, state, content_gen=partial(_frame, content_gen)))
