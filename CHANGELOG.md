
## 0.6.1

**Additions**

* Add a `c.quick_plot` function for quick asynchronous plotting without worrying about the threading and event details
* Add a `fps` argument to `c.main`
* Flexible color specification including [xkcd strings](https://xkcd.com/color/rgb/). Colors like `(0,1,1)`, `'dark red'`, `(blue, 0.5)`, or `0xffaa0000` are now possible.

## 0.6.0

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
