# Introduction

UI components ("widgets") in Concur are Python generators. Internally, widgets do three things:

1. Call ImGui commands to draw stuff to screen
2. When the drawing is done, they `yield` and pass control flow upstream.
3. On user interaction, they `return result`, where result is a value representing user action and/or new widget state.

A simple button widget can be implemented as follows:

```python
def button(text):
    while True:
        is_pressed = imgui.button(text): # Draw the button (1.)
        if is_pressed:
            return 123                   # Return a value on click (3.)
        yield                            # Drawing is done (2.)
```

The resulting widget can be displayed using `return` or `yield from`, optionally collecting its return value.

```python
value = yield from button("Click me")
assert value == 123
```

This shows the most interesting property of Concur: **widgets only exist until they are interacted with.** To interact with a widget repeatedly, it must be re-created each time it's interacted with. This concept is _surprisingly_ powerful – it enables composition in time by simply chaining statements:

```python
yield from button("one button")
yield # clear the screen
yield from button("another button")
```

This creates "one button", and after it is clicked, "another button" is created. If the code above isn't in a loop or inside another widget (see below), there is nothing more to do after clicking the second button and the application is closed.

Composition in space (that is, rendering multiple widgets at once) is done using the `concur.core.orr` function<sup>1</sup>. The result of the composition is yet another widget:

```python
import concur as c # concur is usually imported as c

pair = c.orr([button("First"), button("Second")])
# display `pair` as a normal widget
yield from pair
```

The result is a widget `pair`, which returns as soon as any child widget returns, passing the return value along. How do we tell which button was pressed? We don't, they must simply return different values. By convention, all primitive widgets return a tuple `(identifier, value)` to be easily identifiable when inside `orr`.

For example, built-in buttons return the pair `(<name>, None)`, so they can be composed like this:

```python
tag, value = yield from c.orr([c.button("First"), c.button("Second")])
if tag == "First":
    print("first!")
if tag == "Second":
    print("second!")
```

Many other widgets return a more useful value as the second tuple element: checkbox returns `bool`, input_text returns `str`, etc.

Many widgets take another widget as an argument (image, window, etc.), which is typically displayed inside (window contents, image overlay, etc.). Note that any composition of widgets is itself a widget with the same semantics, and return values are typically passed through.

Once the whole user interface is represented as as single widget using various composition primitives, it can be displayed using the `concur.integrations.glfw.main` function.

That's it for now. Play around with it. You will discover that these handful of concepts go a *long* way, and can be used to create even large UIs in a straightforward and clear manner. As a starting point, you can use the [examples](https://github.com/potocpav/python-concur/tree/master/examples).

----

<sup>1</sup> The name `orr` is derived from the fact that the resulting widget returns if any child returns (child1 **or** child2). To signify that a list of children is expected (not a pair), **orr** is used instead of **or**. In Concur for Purescript, there is also the [`andd` operator](https://pursuit.purescript.org/packages/purescript-concur-core/0.4.1/docs/Concur.Core.Types#v:andd) which returns when all children return.
