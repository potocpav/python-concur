# Troubleshooting

Here's a list of known issues and their solutions:

**Widget flicker**

Between any two `yield from _` statements that can return, there must be a `yield` statement. Otherwise, elements may get duplicated in a frame after triggering an action. On the other hand, if there are too many `yield` statemets, elements may momentarily disappear.

I don't think this bit of syntactic inconvenience can be solved without introducing other quirks.

**Event congestion**

On each frame, at most one action can get triggered from an `orr` block. Actions from first sub-widgets are prioritized, and any actions from further sub-widgets will get thrown out. This is a problem when there are rapidly-firing widgets, such as video playback. Swap the congesting `orr` function for `multi_orr` which returns a list of all fired events.

**Asynchronous computations**

In other versions of Concur, all widgets are triggered asynchronously. This may not be practical in Python, due to a limitation of async generators: they can't `return`, they only `yield`. Synchronous generators are used instead, which means that all widget code is run in the main thread. Asynchronous code must be explicitly run in a background thread, which is easily achieved by passing a future into the `block` function. See the [timers example](https://github.com/potocpav/python-concur/blob/master/examples/timers.py) for details.
