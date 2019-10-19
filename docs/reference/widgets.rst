
Widgets
=======

Most widgets are just thin wrappers over `widgets in PyImGui`_. It is mostly
trivial to add new widgets.

By convention, all widgets take a string identifier as the first parameter, and return the ``(identifier, value)`` pair. This is done to increase convenience, as Python syntax for mapping values is a bit busy.

TODO: move the next stuff elsewhere

Some widgets don't do any drawing and serve purely for control flow, or user interaction. For example, :func:`concur.block` abstracts over future execution, and :func:`concur.key_pressed` handles application-wide hotkeys.

.. _widgets in PyImGui: https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html


.. automodule:: concur
   :members: window, child, button, radio_button, input_text, text, text_colored, show_test_window, separator, spacing, same_line, checkbox, drag_float, slider_int, slider_float, key_pressed
   :undoc-members:
