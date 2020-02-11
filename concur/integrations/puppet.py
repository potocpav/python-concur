"""Automation back-end with screen capture and programmatical user input.

Normally, this is used with functions in `concur.testing`.
"""

from __future__ import absolute_import

import glfw
import imgui
import time
import OpenGL.GL as gl

# Save as video
from PIL import Image
import imageio
import numpy as np

from concur.integrations.glfw import create_window, create_window_dock, begin_maximized_window
from concur.integrations.opengl import create_offscreen_fb, get_fb_data
from imgui.integrations import compute_fb_scale
from imgui.integrations.opengl import ProgrammablePipelineRenderer


class PuppetRenderer(ProgrammablePipelineRenderer):
    """Renderer for automated testing. User inputs are set programmatically, rather than interactively."""
    def __init__(self, window):
        super(PuppetRenderer, self).__init__()
        self.window = window

        self.io.display_size = glfw.get_framebuffer_size(self.window)

        self._map_keys()
        self._gui_time = None

        self._click = [False] * 3
        self._mouse_buttons = [False] * 3
        self._mouse_pos = 100, 100
        self._mouse_wheel = 0.0

    def _map_keys(self):
        key_map = self.io.key_map

        key_map[imgui.KEY_TAB] = glfw.KEY_TAB
        key_map[imgui.KEY_LEFT_ARROW] = glfw.KEY_LEFT
        key_map[imgui.KEY_RIGHT_ARROW] = glfw.KEY_RIGHT
        key_map[imgui.KEY_UP_ARROW] = glfw.KEY_UP
        key_map[imgui.KEY_DOWN_ARROW] = glfw.KEY_DOWN
        key_map[imgui.KEY_PAGE_UP] = glfw.KEY_PAGE_UP
        key_map[imgui.KEY_PAGE_DOWN] = glfw.KEY_PAGE_DOWN
        key_map[imgui.KEY_HOME] = glfw.KEY_HOME
        key_map[imgui.KEY_END] = glfw.KEY_END
        key_map[imgui.KEY_DELETE] = glfw.KEY_DELETE
        key_map[imgui.KEY_BACKSPACE] = glfw.KEY_BACKSPACE
        key_map[imgui.KEY_ENTER] = glfw.KEY_ENTER
        key_map[imgui.KEY_ESCAPE] = glfw.KEY_ESCAPE
        key_map[imgui.KEY_A] = glfw.KEY_A
        key_map[imgui.KEY_C] = glfw.KEY_C
        key_map[imgui.KEY_V] = glfw.KEY_V
        key_map[imgui.KEY_X] = glfw.KEY_X
        key_map[imgui.KEY_Y] = glfw.KEY_Y
        key_map[imgui.KEY_Z] = glfw.KEY_Z

    def process_inputs(self):
        """Process the virtual user inputs. Called by `main` at the beginning of each frame."""
        io = imgui.get_io()

        window_size = glfw.get_window_size(self.window)
        fb_size = glfw.get_framebuffer_size(self.window)

        io.display_size = window_size
        io.display_fb_scale = compute_fb_scale(window_size, fb_size)
        io.delta_time = 1.0/60

        current_time = glfw.get_time()

        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1. / 60.

        self._gui_time = current_time

        for i, b in enumerate(self._click):
            if b:
                io.mouse_down[i] = True
                self._click[i] = False
            else:
                io.mouse_down[i] = False
        for i, b in enumerate(self._mouse_buttons):
            if b:
                io.mouse_down[i] = True

        io.mouse_pos = self._mouse_pos
        io.mouse_wheel = self._mouse_wheel
        self._mouse_wheel = 0.0

    def click(self, button=0):
        """Simulate a mouse button click.

        * 0 .. left button
        * 1 .. right button
        * 2 .. middle button
        """
        self._click[button] = True

    def set_mouse_pos(self, x, y):
        'Set the mouse cursor position to a specified value.'
        self._mouse_pos = x, y

    def scroll_up(self):
        'Scroll the mouse wheel up one click.'
        self._mouse_wheel = 1

    def scroll_dn(self):
        'Scroll the mouse wheel down one click.'
        self._mouse_wheel = -1

    def mouse_dn(self, button=0):
        """Push a specified mouse button."""
        self._mouse_buttons[button] = True

    def mouse_up(self, button=0):
        """Release a specified mouse button."""
        self._mouse_buttons[button] = False

    def key_dn(self, key):
        imgui.get_io().keys_down[key] = True
        exit(0)

    def key_up(self, key):
        imgui.get_io().keys_down[key] = False

    def write_char(self, c):
        assert 0 < c < 0x10000
        imgui.get_io().add_input_character(c)




def main(name, widget_gen, width, height, save_screencast=None, return_sshot=False):
    """ Create a GLFW window, spin up the main loop, and display a given widget inside.

    The resulting window is not hooked up to the user input. Instead, input is handled
    by a PuppetRenderer instance.

    `widget_gen` takes as an argument a `PuppetRenderer` instance, and returns a widget.
    """
    imgui.create_context()

    # Set config flags
    imgui.get_io().config_flags |= imgui.CONFIG_DOCKING_ENABLE | imgui.CONFIG_VIEWPORTS_ENABLE

    window = create_window(name, width, height)
    impl = PuppetRenderer(window)
    widget = widget_gen(impl)
    offscreen_fb = create_offscreen_fb(width, height)

    if save_screencast:
        writer = imageio.get_writer(save_screencast, mode='I', fps=60)

    while not glfw.window_should_close(window):
        t0 = time.perf_counter()
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        create_window_dock(window)
        begin_maximized_window("Default##Concur", window)

        try:
            next(widget)
        except StopIteration:
            imgui.end()
            imgui.render()
            break
        except:
            # Cleanup on exception for iPython
            imgui.end()
            imgui.render()
            impl.shutdown()
            glfw.terminate()
            raise

        imgui.end()
        imgui.render()

        if save_screencast:
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, offscreen_fb)
            impl.render(imgui.get_draw_data())
            image = get_fb_data(offscreen_fb, width, height)
            writer.append_data(image)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        t1 = time.perf_counter()
        if t1 - t0 < 1/60:
            time.sleep(1/60 - (t1 - t0))

    if save_screencast:
        writer.close()

    if return_sshot:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, offscreen_fb)
        impl.render(imgui.get_draw_data())
        image = get_fb_data(offscreen_fb, width, height)
        ret = image
    else:
        ret = None

    # # retrieve pixels from framebuffer and write to file
    # file_path = "test.png"
    # image = get_fb_data(offscreen_fb, width, height)
    # image.save(file_path)

    impl.shutdown()
    glfw.terminate()
    return ret
