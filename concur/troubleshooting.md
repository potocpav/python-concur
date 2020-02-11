# Troubleshooting

Here's a list of common issues and their solutions:

**Widget flicker**

Between any two `yield from _` statements that can return, there must be exactly one `yield` statement. If there is none, elements may get duplicated in a frame after triggering an action. If there is more than one `yield` statemet, elements may momentarily disappear.

Most of the time, it is enough to slap a `yield` at the end of each loop ([example](https://github.com/potocpav/python-concur/blob/master/examples/counters.py#L19)). I don't think this bit of syntactic inconvenience can be solved without introducing other quirks.

**Event congestion**

On each frame, at most one action can get triggered from an `concur.core.orr` block. Actions from first sub-widgets are prioritized, and any actions from further sub-widgets will get thrown out. This is a problem when there are rapidly-firing widgets, such as video playback.

Push the widgets with lower priority down the widget lists, or swap the congesting `orr` function for `multi_orr`. `concur.core.multi_orr` returns a list of all fired events, which trades correctness for some boilerplate. Typically, the top-level widget list is `multi_orr`, while the lower levels can be `orr`.

**Asynchronous computations**

In [other ](https://github.com/ajnsit/concur-js)[versions ](https://github.com/purescript-concur/purescript-concur-react)[of Concur](https://github.com/ajnsit/concur), all widgets are triggered asynchronously. This may not be practical in Python, due to a limitation of async generators: they can't `return`, they only `yield`. Synchronous generators are used instead, which means that all widget code is run in the main thread. Asynchronous code must be explicitly run in a background thread, which is easily achieved by passing a future into the `concur.core.Block` function. See the [timers example](https://github.com/potocpav/python-concur/blob/master/examples/timers.py) for details.
