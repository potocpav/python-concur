
from imgui import push_id, pop_id


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


class Tagged(object):
    def __init__(self, tag, value):
        self.tag, self.value = tag, value

    def __repr__(self):
        return f"{self.tag} {self.value}"


def tag(tag_name, elem):
    while True:
        try:
            next(elem)
            yield
        except StopIteration as e:
            return Tagged(tag_name, e.value)


def stateful(elem, initial_state):
    state = initial_state
    while True:
        state = yield from elem(state)
        yield



def drag_float(value):
    value = yield from c.orr([c.drag_float("Value", value), c.text("value: " + str(value))])
    return value


# TODO: cancel unneeded futures, probably by converting this into a class with a destructor
def block(future):
    """ Create a widget that returns on future result. Useful for async computations. """
    while True:
        if future.done():
            return future.result()
        else:
            yield
