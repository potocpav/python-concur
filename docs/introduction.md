
# Introduction

UI components in Concur are represented by generators, henceforth called **widgets**. Internally, widgets do three things:

* Call ImGui commands to draw stuff to screen
* When the drawing is done, `yield` and pass control flow upstream
* On user interaction, they `return result`, where result is a value representing user action and/or widget state.

A simple button widget can be implemented as follows:

```python
def button(text):
    while True:
        is_pressed = imgui.button(text): # Draw the button
        if is_pressed:
            return 123  # Return an arbitrary value
        yield           # Drawing is done.
```

The resulting widget can be displayed using `yield from`, optionally collecting its return value.

```python
value = yield from button("Click me")
assert value == 123
```

This shows the most interesting property of Concur: **widgets exist only until they are interacted with.** This enables trivial composition in time by simply chaining the statements. There must be a `yield` between the buttons to properly clear the screen.

```python
yield from button("One Button")
yield
yield from button("Another Button")
```

This creates one button, and after it is clicked, another button is created. If the code above isn't in a loop or in another widget (see below), there is nothing more to do after clicking the second button and the application is closed.

Composition in space (that is, rendering multiple widgets at once) is done using the :func:`concur.orr` combinator. The result of the composition is yet another widget:

```python
pair = concur.orr([button("First"), button("Second")])
yield from pair # display `pair` as a normal widget
```

The result of :func:`concur.orr`  is returned as soon as any child widget returns, passing the return value along. How can we tell which button was pressed? We can't, they must simply return different values. By convention, primitive widgets return a tuple `(identifier, value)` to be easily identifiable when inside `orr`. For example, built-in buttons can be composed like this:

```python
tag, value = concur.orr([concur.button("First"), concur.button("Second")])
if tag == "First":
    print("first!")
if tag == "Second":
    print("second!")
```

Note that containers (such as a window) are widgets too, with the same semantics. They take as an argument a list of other widgets that will be drawn inside.

Once the whole user interface is represented as as single widget, it can be displayed using the :func:`concur.integrations.main` function.

That's it for now. Play around with it. You will discover that these handful of concepts go a *long* way, and can be used to create even large UIs in a straightforward and clear manner. As a starting point, you can use the [examples](https://github.com/potocpav/python-concur/tree/master/examples).
