"""
.. include:: ../README.md
   :start-after: [**Examples**](examples)
   :end-before: # Installation

.. include:: introduction.md

.. include:: troubleshooting.md

# API

All the functions and classes from `concur.core` and `concur.widgets` are re-exported in the `concur` module. The most convenient way to access them is by importing `concur` qualified:

```python
import concur as c
```

"""

import concur.extra_widgets
import concur.integrations
import concur.draw

from .core import *
from .widgets import *
from .extra_widgets import *
