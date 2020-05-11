"""

Most of the functions and classes from submodules are re-exported in the
`concur` root module. The idiomatic way to access them is by importing `concur` qualified:

```python
import concur as c

# nearly anything can be accessed using `c.anything` now.
```

A notable exception is the `concur.draw` functions: they have a bit different semantics, so they are in a separate
module, `c.draw`.
"""

import concur.extra_widgets
import concur.integrations
import concur.draw
import concur.testing

from .core import *
from .widgets import *
from .extra_widgets import *
from .integrations import main, quick_plot, quick_window, quick_image

import functools


def partial(*args, **argv):
    """Re-export of [`functools.partial`](https://docs.python.org/3.9/library/functools.html#functools.partial)
    for convenience
    """
    return functools.partial(*args, **argv)
