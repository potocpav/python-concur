""" Integration with the host system: windowing, user input, etc.

Even using PyImGui's integration code, quite a bit of boilerplate is needed just to create a window,
or to display an image. This module provides functions that simplify getting stuff rendered to just
a couple of lines of code.
"""

import concur.integrations.glfw
import concur.integrations.opengl
import concur.integrations.puppet

from .glfw import *
from .opengl import *
