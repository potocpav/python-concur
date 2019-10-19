Core API
==========

All the following functions are exposed in the ``concur`` module. It is meant to be imported qualified: ::

  import concur as c


Widget Composition
------------------

Results of widget composition are widgets themselves, so these functions can be used in a tree-like fashion.

.. automodule:: concur
   :members: orr, multi_orr, orr_same_line, forever, optional
   :undoc-members:

Widget Wrapping
---------------

Helper functions for making widgets out of ImGui elements.

.. automodule:: concur
   :members: lift, interactive_elem
   :undoc-members:


UI Widgets
-----------

By convention, all widgets take a string identifier as the first parameter, and return the ``(identifier, value)`` pair. This is done to increase convenience, as Python syntax for mapping values is a bit busy.

Most widgets are just thin wrappers over `widgets in PyImGui`_. It is mostly trivial to add new widgets. New widgets can be added by writing generators, or by using helper functions :func:`interactive_elem` or :func:`lift`.

.. _widgets in PyImGui: https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html

.. automodule:: concur
  :members: window, child, button, radio_button, input_text, text, text_colored, show_test_window, separator, spacing, checkbox, drag_float, slider_int, slider_float
  :undoc-members:


Special Widgets
-----------------

These widgets don't do any drawing and serve purely for control flow, or user interaction.

.. automodule:: concur
  :members: nothing, key_pressed, block, same_line
