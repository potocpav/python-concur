""" A collection of widgets based off of ImGui.

By convention, most widgets take a string identifier as the first parameter, and return the `(identifier, value)` pair.
This is done for convenience, as Python syntax for mapping values is a bit busy. If you want to return a different
identifier to what is displayed on screen, use the `tag` keyword argument which is available for all widgets where
it makes sense.

Most widgets are just thin wrappers over [widgets in PyImGui](https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html).
If any widget from ImGui is not listed here, it is mostly trivial to add it. New widgets can be created by writing
generators by hand, or by using helper functions `concur.core.interactive_elem` or `concur.core.lift`.

Some widgets (`transform`, `key_press`, etc.) don't do any drawing and serve purely for control flow, or user interaction.

All of the functions in this module are re-exported in the root module for convenience.
"""

__pdoc__ = dict(same_line=False)


import numpy as np  # for `transform`
from typing import Iterable, Any, Tuple
import imgui

from concur.core import orr, lift, Widget, interactive_elem
from concur.colors import color_to_rgba_tuple


def orr_same_line(widgets):
    """ Use instead of `concur.core.orr` to layout child widgets horizontally instead of vertically. """
    def intersperse(delimiter, seq):
        """ https://stackoverflow.com/questions/5655708/python-most-elegant-way-to-intersperse-a-list-with-an-element """
        from itertools import chain, repeat
        return list(chain.from_iterable(zip(repeat(delimiter), seq)))[1:]

    def group(widget):
        return orr([lift(imgui.begin_group), widget, lift(imgui.end_group)])

    return orr(intersperse(same_line(), [group(w) for w in widgets]))


def window(title: str,
           widget: Widget,
           position: Tuple[int, int] = None,
           size: Tuple[int, int] = None,
           flags: int = 0) -> Widget:
    """ Create a window with a given `widget` inside.

    Contents are drawn only if the window is opened. Window title must be unique. Windows must not be nested.
    """
    while True:
        if position is not None:
            imgui.set_next_window_position(*position)
        if size is not None:
            imgui.set_next_window_size(*size)
        else:
            imgui.set_next_window_size(400, 300, imgui.FIRST_USE_EVER)
        expanded, opened = imgui.begin(title, flags=flags)
        try:
            if expanded and opened:
                next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end()
        yield


def child(name, widget, width, height, border=False, flags=0):
    r""" Create a sized box with a `widget` inside.

    If the contents overflow, scrollbars will be created by default.
    Sizing of the child widget allows for three modes, depending on the sign of parameters `width` and `height`:

    * ==0 - use the remaining window size
    * \>0 - fixed size in pixels
    * <0 - use remaining window size minus abs(size) in pixels

    Args:
        name: Child name. This has no effect, and will be removed in the future.
        widget: Widget to display inside the box.
        width: Box width.
        height: Box height.
        border: Toggle border visibility.
        flags: Advanced customization flags. See the
            [list of available flags](https://pyimgui.readthedocs.io/en/latest/guide/window-flags.html#window-flag-options).
    """
    while True:
        imgui.begin_child(name, width, height, border, flags)
        try:
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_child()
        yield


def collapsing_header(text, widget, open=True):
    """Display a collapsible section header. It can be open or closed by default (parameter `open`).
    """
    while True:
        expanded, visible = imgui.collapsing_header(text, flags=open and imgui.TREE_NODE_DEFAULT_OPEN)
        try:
            if expanded:
                next(widget)
        except StopIteration as e:
            return e.value
        yield


def tree_node(text, widget, open=True):
    """Display a collapsible tree node. It can be open or closed by default (parameter `open`).

    Tree node content has left offset, unlike `collapsing_header`.
    """
    while True:
        expanded = imgui.tree_node(text, flags=open and imgui.TREE_NODE_DEFAULT_OPEN)
        try:
            if expanded:
                next(widget)
        except StopIteration as e:
            return e.value
        finally:
            if expanded:
                imgui.tree_pop()
        yield


def button(label, tag=None):
    """ Button. Returns `(label, None)` on click, or `(tag, None)` if tag is specified. """
    while not imgui.button(label):
        yield
    return tag if tag is not None else label, None


def image_button(name, texture_id, width, height, uv0=(0, 0), uv1=(1, 1), tint_color='white', border_color='black', frame_padding=-1):
    """ Image button. Returns `(name, None)` on click.

    Args:
        texture_id: OpenGL texture ID
        size: image display size two-tuple
        uv0: UV coordinates for 1st corner (lower-left for OpenGL)
        uv1: UV coordinates for 2nd corner (upper-right for OpenGL)
        tint_color: Image tint color
        border_color: Image border color
        frame_padding: Frame padding (0: no padding, <0 default padding)
    """
    while not imgui.image_button(texture_id, width, height, uv0=uv0, uv1=uv1, tint_color=color_to_rgba_tuple(tint_color), border_color=color_to_rgba_tuple(border_color), frame_padding=frame_padding):
        yield
    return name, None


def invisible_button(label, width, height, tag=None):
    """ Invisible button with a given width and height.

    Can be interacted with as a normal button, including clicking and dragging.

    Returns `(label, None)` on click, or `(tag, None)` if tag is specified.
    """
    while not imgui.invisible_button(label, width, height):
        yield
    return tag if tag is not None else label, None


def color_button(label, color, tag=None):
    """ Colored button. Color can be specified in multiple ways listed in
    [concur.draw].

    Returns `(label, None)` on click, or `(tag, None)` if tag is specified.
    """
    r, g, b, a = color_to_rgba_tuple(color)
    while not imgui.color_button(label, r, g, b, a):
        yield
    return tag if tag is not None else label, None


def radio_button(label, active, tag=None):
    """ Radio button. Returns `(label, None)` on click, or `(tag, None)` if tag is specified. """
    while not imgui.radio_button(label, active):
        yield
    return (tag if tag is not None else label), None


def dummy(width, height):
    """ Add a dummy element of a given `width` and `height`.

    Useful for custom-sized vertical and horizontal spacings.
    """
    return lift(imgui.dummy, width, height)


def input_text(name, value, buffer_length=255, tag=None, flags=0):
    """ Text input.

    Flags are [defined by PyImGui](https://pyimgui.readthedocs.io/en/latest/guide/inputtext-flags.html#inputtext-flag-options).
    `buffer_length` doesn't affect widget size on screen, it limits the maximum character count only.
    """
    while True:
        changed, new_value = imgui.input_text(name, value, buffer_length, flags)
        if changed:
            return (name if tag is None else tag), new_value
        else:
            yield


def input_text_multiline(name, value, buffer_length=4000, width=0, height=0, flags=0, tag=None):
    """ Multiline text input.

    Flags are [defined by PyImGui](https://pyimgui.readthedocs.io/en/latest/guide/inputtext-flags.html#inputtext-flag-options).
    """
    while True:
        changed, new_value = imgui.input_text_multiline(name, value, buffer_length, width, height, flags)
        if changed:
            return (name if tag is None else tag), new_value
        else:
            yield


def key_press(name, key_index, ctrl=False, shift=False, alt=False, super=False, repeat=True):
    """ Invisible widget that waits for a given key to be pressed.

    No widget must be active at the time to prevent triggering hotkeys by editing text fields.
    Key codes are specified by glfw, e.g. `glfw.KEY_A`, or `glfw.KEY_SPACE`.
    Upper-case ASCII codes also work, such as ord('A').
    """
    io = imgui.get_io()
    while True:
        if imgui.is_key_pressed(key_index, repeat):
            if not imgui.is_any_item_active() and \
                    ctrl == io.key_ctrl and \
                    shift == io.key_shift and \
                    alt == io.key_alt and \
                    super == io.key_super:
                return name, None

        yield


def mouse_click(name, button=0):
    """ Invisible widget that waits for a given mouse button to be clicked (default: LMB).

    This function is triggered only when no widgets are interacted with using mouse.
    Event is returned in the format `(name, (x, y))`, where `(x, y)` are the coordinates
    of the clicked position.
    """
    io = imgui.get_io()
    while True:
        if not imgui.is_any_item_active() and imgui.is_mouse_clicked(button):
            return name, io.mouse_pos
        yield


def text_tooltip(text, widget):
    """Display a text tooltip on hover"""
    while True:
        try:
            imgui.begin_group()
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_group()
        if imgui.is_item_hovered():
            imgui.set_tooltip(text)
        yield


def tooltip(tooltip_widget, widget):
    """ Display a widget tooltip on hover. May contain arbitrary elements, such as images. """
    while True:
        try:
            imgui.begin_group()
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_group()

        if imgui.is_item_hovered():
            try:
                imgui.begin_tooltip()
                next(tooltip_widget)
            except StopIteration as e:
                return e.value
            finally:
                imgui.end_tooltip()
        yield


def main_menu_bar(widget):
    """ Create a main menu bar.

    This requires setting `menu_bar=True` in the `concur.integrations.glfw.main` method.
    Otherwise, space wouldn't be reserved for the menu bar, and it would lay on top of
    window contents.

    Main menu bar must be created outside any windows.

    See [examples/extra/menu_bar.py](https://github.com/potocpav/python-concur/tree/master/examples/extra/menu_bar.py)
    for an usage example.
    """
    while True:
        assert imgui.begin_main_menu_bar(), "Main menu bar must be created outside a window."
        try:
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.end_main_menu_bar()
        yield


def menu(label, widget, enabled=True):
    """ Create an expandable menu in the `main_menu_bar`.

    Widgets commonly used in menus are `menu_item`, and `separator`.
    """
    while True:
        expanded = imgui.begin_menu(label, enabled)
        try:
            if expanded:
                next(widget)
        except StopIteration as e:
            return e.value
        finally:
            if expanded:
                imgui.end_menu()
        yield


def menu_item(label, shortcut=None, selected=False, enabled=True, *args, **kwargs):
    """ Create a menu item.

    Menu items should be nested inside `menu`.

    Item shortcuts are displayed for convenience, but are not processed in any way.
    They are easily handled by `key_press` outside the menu code If `key_press` was
    inside the menu, it would not be active when the menu is not expanded.
    Items may have a check-box (`selected`), and may or may not be `enabled`.
    """
    return interactive_elem(imgui.menu_item, label, shortcut, selected, enabled, *args, **kwargs)


def separator():
    """ Horizontal separator. """
    return lift(imgui.separator)


def spacing():
    """ Extra vertical space. """
    return lift(imgui.spacing)


def same_line():
    """ Call between widgets to layout them horizontally.

    This is Consider using `concur.widgets.orr_same_line` instead as it is more robust.
    """
    return lift(imgui.same_line)


def font(font_, widget):
    """ Render `widget` with a given font.

    The easiest way to create `font_` is probably to call this before the call to
    `concur.integrations.glfw.main`:

    ```python
    imgui.create_context()
    font = imgui.get_io().fonts.add_font_from_file_ttf("font_file.ttf", 16)
    ```

    See the [font guide in PyImGui](https://pyimgui.readthedocs.io/en/latest/guide/using-fonts.html)
    for more details.
    """
    while True:
        imgui.push_font(font_)
        try:
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.pop_font()
        yield


def text(s):
    """ Passive text display widget. """
    return lift(imgui.text, s)


def text_wrapped(s):
    """ Word wrapping text display widget. Recommended for long chunks of text. """
    def f():
        imgui.push_text_wrap_pos()
        imgui.text(s)
        imgui.pop_text_wrap_pos()
    return lift(f)


def text_colored(s, color):
    """ Passive colored text display widget. """
    r, g, b, a = color_to_rgba_tuple(color)
    return lift(imgui.text_colored, s, r, g, b, a)


def selectable(label, selected, *args, **kwargs):
    """ Selectable line.

    This widget marks the whole line as selectable. To add widgets to `selectable`,
    simply append them using `orr_same_line`:

    ```python
    c.orr_same_line([
        c.selectable("Selectable", False),
        c.text("Extra text"),
        ])
    ```
     """
    return interactive_elem(imgui.selectable, label, selected, *args, **kwargs)


def checkbox(label, checked, *args, **kwargs):
    """ Two-state checkbox. """
    return interactive_elem(imgui.checkbox, label, checked, *args, **kwargs)


def drag_float(label, value, *args, **kwargs):
    """ Float selection widget without a slider. """
    return interactive_elem(imgui.drag_float, label, value, *args, **kwargs)


def drag_float2(label, values, *args, **kwargs):
    """ Float selection widget without a slider for selecting two `values`. """
    value0, value1 = values
    return interactive_elem(imgui.drag_float2, label, value0, value1, *args, **kwargs)


def drag_float3(label, values, *args, **kwargs):
    """ Float selection widget without a slider for selecting three `values`. """
    value0, value1, value2 = values
    return interactive_elem(imgui.drag_float3, label, value0, value1, value2, *args, **kwargs)


def drag_float4(label, values, *args, **kwargs):
    """ Float selection widget without a slider for selecting four `values`. """
    value0, value1, value2, value3 = values
    return interactive_elem(imgui.drag_float4, label, value0, value1, value2, value3, *args, **kwargs)


def drag_int(label, value, *args, **kwargs):
    """ Integer selection widget without a slider. """
    return interactive_elem(imgui.drag_int, label, value, *args, **kwargs)


def drag_int2(label, values, *args, **kwargs):
    """ Integer selection widget without a slider for selecting two `values`. """
    value0, value1 = values
    return interactive_elem(imgui.drag_int2, label, value0, value1, *args, **kwargs)


def drag_int3(label, values, *args, **kwargs):
    """ Integer selection widget without a slider for selecting three `values`. """
    value0, value1, value2 = values
    return interactive_elem(imgui.drag_int3, label, value0, value1, value2, *args, **kwargs)


def drag_int4(label, values, *args, **kwargs):
    """ Integer selection widget without a slider for selecting four `values`. """
    value0, value1, value2, value3 = values
    return interactive_elem(imgui.drag_int4, label, value0, value1, value2, value3, *args, **kwargs)


def input_float(label, value, *args, **kwargs):
    """ Float input widget. """
    return interactive_elem(imgui.input_float, label, value, *args, **kwargs)


def slider_int(label, value, min_value, max_value, *args, **kwargs):
    """ Int selection slider. """
    return interactive_elem(imgui.slider_int, label, value, min_value, max_value, *args, **kwargs)


def slider_float(label, value, min_value, max_value, *args, **kwargs):
    """ Float selection slider. """
    return interactive_elem(imgui.slider_float, label, value, min_value, max_value, *args, **kwargs)


def test_window():
    """ ImGui test window with a multitude of widgets. """
    return lift(imgui.show_test_window)


def columns(elems, identifier=None, border=True, widths=[]):
    """ Table, using the imgui columns API.

    `elems` is a 2D array of widgets
    `widths` is a optional vector of column widths in pixels. May contain
    None values.
    """
    n_columns = len(elems[0])
    for e in elems:
        assert len(e) == n_columns
    accum = []
    accum.append(lift(imgui.columns, n_columns, identifier, border))
    for i, w in enumerate(widths):
        if w is not None:
            accum.append(lift(imgui.set_column_width, i, w))
    for row in elems:
        for widget in row:
            accum.append(widget)
            accum.append(lift(imgui.next_column))
    accum.append(lift(imgui.columns, 1))
    return orr(accum)


def transform(x, y, widget, tf=None):
    # TODO: move somewhere else
    """ Use `concur.extra_widgets.pan_zoom.TF` and a specified position `x, y` to transform a widget.

    Only widget position will be affected (not scaling), and it will be positioned so that its upper left corner
    is at `[x, y]`.
    """
    old_pos = imgui.get_cursor_screen_pos()
    if tf is not None:
        x, y = np.matmul(tf.c2s, [x, y, 1])
    while True:
        try:
            imgui.set_cursor_screen_pos((x, y))
            next(widget)
        except StopIteration as e:
            return e.value
        finally:
            imgui.set_cursor_screen_pos(old_pos)
        yield
