""" Even using PyImGui's integration code, quite a bit of boilerplate is needed just to create a window, or to display an image. This module provides functions that simplify getting stuff rendered.
"""

import concur.integrations.glfw
import concur.integrations.opengl
import concur.integrations.puppet
#
# __all__ = glfw.__all__ + opengl.__all__

from .glfw import *
from .opengl import *
