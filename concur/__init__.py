"""
.. include:: ../README.md
   :start-after: [**Examples**](examples)
   :end-before: # Installation

.. include:: introduction.md

.. include:: troubleshooting.md

# API

All the functions and classes from `concur.core` and `concur.widget` are re-exported in the `concur` module. The most convenient way to access them is by importing `concur` qualified:

```python
import concur as c
```

"""

from .core import *
from .widgets import *
