""" Functions providing core functionality, widget creation, manipulation, and composition.

All of the functions in this module are re-exported in the root module for convenience.
"""

__pdoc__ = dict(remote_widget=False, fork_action=False, RemoteAction=False)


import queue
from typing import Generator, Any, Iterable, List, Callable, Tuple
from asyncio import Future
from imgui import push_id, pop_id


Widget = Any # It isn't possible to type Widget correctly using mypy. Prove me wrong.


def orr(widgets: Iterable[Widget]) -> Widget:
    """ Chain elements in space, returning the first event fired.

    This is the principal way to compose widgets in Concur. Windows, for example, typically contain multiple
    widgets composed into one by `orr`:

    ```python
    c.window("Buttons", c.orr([
        c.button("Button 1"),
        c.button("Button 2"),
        ]))
    ```

    Widgets are laid out vertically. For horizontal layout, use `concur.widgets.orr_same_line`."""
    stop = False
    value = None
    while True:
        for i, elem in enumerate(widgets):
            try:
                push_id(str(i))
                next(elem)
            except StopIteration as e:
                if not stop:
                    stop = True
                    value = e.value
            finally:
                pop_id()
        if stop:
            return value
        else:
            yield


def multi_orr(widgets: Iterable[Widget]) -> Widget:
    """ Chain elements in space, returning all the events fired as a list.

    This is an alternative to `concur.core.orr` which doesn't throw away events, but is somewhat
    less convenient to compose. Care must be taken not to update the same state variable twice
    as a reaction to two different concurrent events. The first update may get overwritten.

    Mostly, the transition from `orr` to `multi_orr` is trivial. Replace this:
    ```python
    key, value = c.orr([...])
    # update
    if key == <this>:
        ...
    elif key == <that>:
        ...
    ```
    with this:
    ```python
    events = c.multi_orr([...])
    for key, value in events:
        # update
        if key == <this>:
            ...
        elif key == <that>:
            ...
    ```
    """
    events: List = []
    while events == []:
        for i, elem in enumerate(widgets):
            try:
                push_id(str(i))
                next(elem)
            except StopIteration as e:
                events.append(e.value)
            finally:
                pop_id()
        if events == []:
            yield
    return events


def forever(widget_gen: Callable[..., Widget], *args, **kwargs) -> Widget:
    """ Repeat a widget forever.

    Function generating the widget must be passed as the first argument;
    remaining arguments are passed to said function.

    This can be used to easily suppress any widget events, like this:
    ```python
    c.forever(c.button, "Not Clickable")
    ```
    """
    widget = widget_gen(*args, **kwargs)
    while True:
        try:
            next(widget)
        except StopIteration:
            widget = widget_gen(*args, **kwargs)
        yield



def lift(f: Callable[..., Any], *args, **argv) -> Widget:
    """ Lift a function into a never-ending widget.

    Useful for wrapping ImGui calls and passive widgets. For example, to create a text widget:
    ```python
    c.lift(imgui.text, "some text")
    ```
    """
    while True:
        f(*args, **argv)
        yield


def interactive_elem(elem, name, *args, **kwargs):
    """ Function useful for wrapping a wide range of ImGui widgets.

    Elements which take `name` as the first argument and return
    a pair `(changed, value)` can be wrapped using this function.
    It is used to wrap many imgui widgets in `concur.widgets`.
    """
    if 'tag' in kwargs:
        tag = kwargs['tag']
        del kwargs['tag']
    else:
        tag = name
    while True:
        changed, value = elem(name, *args, **kwargs)
        if changed:
            return tag, value
        else:
            yield


def nothing():
    """ Widget that does nothing forever. """
    while True: yield


def event(ev):
    """ Widget that immediately returns `ev`. """
    return ev
    yield


def optional(exists: bool, widget_gen: Callable[..., Widget], *args, **kwargs):
    """ Optionally display a widget. """
    return widget_gen(*args, **kwargs) if exists else nothing()


def tag(tag_name: Any, elem: Widget) -> Widget:
    """ Transform any returned value `v` of `elem` into a tuple `tag_name, v`. """
    return tag_name, (yield from elem)


def tag_value(tag_name: Any, elem: Widget) -> Widget:
    """ Transform any returned value `(t, v)` of `elem` into a tuple `t, (tag_name, v)`.

    Useful for identifying elements in lists and tables."""
    t, v = yield from elem
    return t, (tag_name, v)


def map(f: Any, elem: Widget) -> Widget:
    """ Transform any returned value `v` of `elem` into `f(v)`. """
    v = yield from elem
    return f(v)


def stateful(elem: Callable[[Any], Widget], initial_state: Any) -> Widget:
    """Thread state from the widget into itself, creating a stateful never-ending widget.

    Explicit state threading is mostly better than using this function, due to the added
    flexibility and due to the fact than excessive use of higher-order functions is not
    very Pythonic.
    """
    state = initial_state
    while True:
        state = yield from elem(state)
        yield


class Block(object):
    """ Create a widget that returns on [Future](https://docs.python.org/3.9/library/asyncio-future.html#asyncio.Future) result.

    This is useful for easily doing async computations. For an usage example, see the
    [timers example](https://github.com/potocpav/python-concur/blob/master/examples/timers.py).

    This widget is constructed manually using a class, because the future must be
    canceled in the destructor. Destructor isn't available in generator functions.

    """
    def __init__(self, future):
        self.future = future

    def __iter__(self):
        return self

    def __next__(self):
        if self.future.done():
            raise StopIteration(self.future.result())

    def __del__(self):
        self.future.cancel()


def listen(que):
    """ Listen for messages in a given queue. """
    while True:
        try:
            return que.get_nowait()
        except queue.Empty:
            yield


class RemoteAction(object):
    def __init__(self, future, que):
        self.que = que
        self.future = future
        self.sent = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.future is not None and not self.sent and self.future.done():
            self.que.put(self.future.result())
            self.sent = True

    def __del__(self):
        if self.future is not None:
            self.future.cancel()


def remote_widget(future):
    """ Separate the effect of the widget from its result """
    q = queue.Queue()

    def value():
        while True:
            try:
                v = q.get_nowait()
                return v
            except queue.Empty:
                yield

    return RemoteAction(future, q), value


def fork_action(future, rest_gen):
    """ A common pattern - running a long running action (`future`) and keeping the GUI (`rest`) responsive.

    Because the action can't be restarted on every gui event, we must *fork* it off in the beginning.
    It is typically easier to expicitly create a future than to use this function.
    """
    action, value_gen = remote_widget(future)
    return orr([action, rest_gen(value_gen)])
