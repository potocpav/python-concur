"""
.. include:: ../README.md
   :start-after: <!-- Start docs -->
   :end-before: <!-- End docs -->

.. include:: introduction.md

.. include:: troubleshooting.md

# API

Most of the functions and classes from submodules are re-exported in the
`concur` root module. The most convenient way to access them is by importing `concur` qualified:

```python
import concur as c

# nearly anything can be accessed using `c.anything` now.
```

A notable exception is the `concur.draw` functions: they have a bit different semantics (no layout,
no user interaction), so they are separate and can be accessed using `c.draw.something`.
"""

import concur.extra_widgets
import concur.integrations
import concur.draw
import concur.testing

from .core import *
from .widgets import *
from .extra_widgets import *
from .integrations import main

import functools


def partial(*args, **argv):
    """Re-export of [`functools.partial`](https://docs.python.org/3.9/library/functools.html#functools.partial)
    for convenience
    """
    return functools.partial(*args, **argv)
