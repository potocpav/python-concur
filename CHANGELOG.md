
## 0.6.0

**Breaking Changes**

* Change the argument order for c.draw.text from (x, y, color, text) to (text, x, y, color).

**Other Changes**

* Improve frame tick labels
* Add this changelog
* Add c.draw.polylines for optimized multiple-polyline rendering. It is possible to draw
  ~100k lines in 60 FPS using this function (instead of ~500 lines)
* Add experimental benchmarking setup
