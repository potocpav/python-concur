
from imgui import push_id, pop_id
import queue


def forever(elem_gen, *args, **kwargs):
    """ Repeat an element forever.

    Function generating the element must be passed as the first argument;
    remaining arguments are passed to said function.
    """
    elem = elem_gen(*args, **kwargs)
    while True:
        try:
            next(elem)
        except StopIteration:
            elem = elem_gen(*args, **kwargs)
        yield


def orr(elems):
    """ Chain elements in space. """
    stop = False
    value = None
    while True:
        for i, elem in enumerate(elems):
            try:
                push_id(i)
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


def lift(f):
    while True:
        f()
        yield


def tag(tag_name, elem):
    while True:
        try:
            next(elem)
            yield
        except StopIteration as e:
            return tag_name, e.value


def stateful(elem, initial_state):
    state = initial_state
    while True:
        state = yield from elem(state)
        yield



def drag_float(value):
    value = yield from c.orr([c.drag_float("Value", value), c.text("value: " + str(value))])
    return value


class block(object):
    """ Create a widget that returns on future result. Useful for async computations.

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
        else:
            return

    def __del__(self):
        self.future.cancel()


def remote_widget(future):
    """ Separate the effect of the widget from its result """
    q = queue.SimpleQueue()

    def action():
        while True:
            if future.done():
                q.put(future.result())
            yield

    def value():
        while True:
            try:
                return q.get_nowait()
            except queue.Empty:
                yield

    return action(), value()


def fork_action(future, rest):
    """ A common pattern - running a long running action and keeping the GUI responsive.

    Because the action can't be restarted on every gui event, we must *fork* it off in the beginning.
    """
    action, value = remote_widget(future)
    orr([action, rest(value)])
