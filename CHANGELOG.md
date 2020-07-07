
## v0.10.0 (planned)

**Breaking Changes**

Remove the `name` argument from `c.child`

## v0.9.3

* `concur.core.replace_tag`, `concur.core.replace_value` added. These make it convenient to transform events without lambdas. Lambdas don't work properly inside loops/comprehensions in Python.

## v0.9.2

* `concur.widgets.dummy` implemented
* `concur.widgets.input_text` flags argument added. This enables creating a password input field, among other use-cases.
* Make the `imageio` dependency non-mandatory.

## v0.9.1

* Update ImGui to the newest version in the `docking` branch
* Improve some docstrings

## v0.9.0

Mainly interactive invocation and documentation improvements.

**Breaking Changes**

* `c.main` argument order switched up to [this](https://potocpav.github.io/python-concur-docs/master/integrations/glfw.html). Widget is now first, then the window name (newly optional), then width and height (also newly optional). This simplifies the Hello, world application and other simple examples considerably.

**Fixes**

* Destroy contexts on `main` exit correctly. This enables multiple `main` invocations with fresh ImGui state.
* Better cleanup on exceptions. Sigkill in IPython doesn't hang the window.

## v0.8.0

**Breaking Changes**

* `concur.extra_widgets.frame` has new arguments `width`, `height` consistent with `concur.extra_widgets.image`.
* PanZoom-derived widgets now handle hover, down, and drag events in a different way. Instead of being yielded, they are
passed to the `content_gen` as a widget. This makes it possible to react to the events in `content_gen`, which is better for
modularization, and it is newly possible to use the information in `tf` as a part of the reaction. The cost is more complicated
`content_gen` signature. Better solution might be possible. Affected widgets:
  * `concur.extra_widgets.pan_zoom`
  * `concur.extra_widgets.image`
  * `concur.extra_widgets.frame`
* PanZoom-derived widgets are now passed a keyword argument `tf`, instead of a positional argument. This will break code which used other names for the transformation info. Affected widgets:
  * `concur.extra_widgets.pan_zoom`
  * `concur.extra_widgets.image`
  * `concur.extra_widgets.frame`
* `concur.draw.image` argument list was reworked. It now takes additional mandatory arguments `x` and `y`, and non-mandotory arguments `uv_a`, `uv_b`.

**Additions**

* `concur.widgets.font`: render a widget with a specific font

**Fixes**

* `concur.extra_widgets.image` now correctly handles images with dimensions not divisible by 4. Previously, those may get severely distorted.
* `concur.extra_widgets.image` now has transparent background even for images without alpha channel.
* `concur.widgets.key_press`: fix a a crash on glfw.KEY_SPACE keypress.
* Make the system clipboard work by upgrading PyImGui to v1.3.1.
* Add a call to `refresh_font_texture` to GLFW initialization. This enables user to [specify a font](https://pyimgui.readthedocs.io/en/latest/guide/using-fonts.html) and have it integrated, and is hopefully harmless in all other cases.
* Fix a crash on certain greyscale NPOT images
* Fix UI ghosts appearing because the buffer was not cleared.

### v0.7.1

* [x] New windows are now fixed size on creation, if they aren't in imgui.ini. Previously, they were fit to contents, which works OK only when the contents do not fit to window. In the common case of a window containing only an image widget, the window would have been created outright tiny. This could lead to user not even noticing it.
* [x] Add:
  * widget `tree_node`
  * widget `input_text_multiline`
  * widget `text_wrapped`
  * scatter square markers (`'s'`)

## v0.7.0

**Breaking Changes**

* Change colored widgets `text_colored` and `color_button` to use the same color spec as the draw functions.
* Rename `key_pressed` to `key_press`
* Remove `TF.hovered`. Left mouse click & drag is now handled by the `pan_zoom` object.
* Add left mouse interaction support to `image` and `frame`. New arguments `drag_tag` and `down_tag`, and `hover_tag`.
  - `pan_zoom.is_hovered` is no longer present.
  - `image` event handling was substantially reworked. Starting the drag outside image window no longer triggers panning.
* `key_press` now respects local keyboard layout

**Other changes**

* add `TF.inv_transform` to tranasform from screen-space to content-space
* Make `scatter` also work with empty one-dimensional arrays
* Add an `invisible_button`, and an `image_button`
* Add `selectable` text
* Enable empty polylines
* Add `drag_int2`, `drag_int3`, and `drag_int4` widgets
* Add modifier key support to `key_press`
* Add `main_menu_bar`, `menu`, and `menu_item`


### v0.6.4

* Fix a bug where long polylines were sometimes corrupted (use-after-free).

### v0.6.3

* Move the documentation and homepage to a [separate repository](https://github.com/potocpav/python-concur-docs)

### v0.6.2

* Implement the square marker `'.'` for scatter plot.
* Implement `draw.polygon` and `draw.polygons` - filled convex polygons.

### v0.6.1

* Add `concur.widgets.mouse_click` widget, which returns mouse position on click
* Add `c.quick_*` functions for quick asynchronous plotting without worrying about the threading and event details
* Add a `fps` argument to `c.main`
    - this is breaking if screencast arguments were used positionally.
* Flexible [color specification](https://potocpav.github.io/python-concur-docs/master/draw.html) including [xkcd strings](https://xkcd.com/color/rgb/). Colors like `(0,1,1)`, `'dark red'`, `('blue', 0.5)`, or `0xffaa0000` are now possible.

## v0.6.0

**Breaking Changes**

* Change the argument order for `c.draw.text` from `(x, y, color, text)` to `(text, x, y, color)`.

**Other Changes**

* Improve frame tick labels
* Add this changelog
* Add `c.draw.polylines` for optimized multiple-polyline rendering. It is possible to draw ~100k lines in 60 FPS using this function (instead of ~500 lines). Using this function, it was possible to implement:
    * `c.draw.ellipses` for optimized multiple ellipse drawing
    * `c.draw.rects` for optimized multiple rectangle drawing
    * `c.draw.scatter` for scatter plots with fancy markers
* Add experimental benchmarking setup
