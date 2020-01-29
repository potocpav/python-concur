# -*- coding: utf-8 -*-
from __future__ import absolute_import

import glfw
import imgui
import time
import OpenGL.GL as gl

# Save as video
from PIL import Image
import imageio
import numpy as np

from concur.integrations.glfw import create_window, create_window_dock
from imgui.integrations import compute_fb_scale
from imgui.integrations.opengl import ProgrammablePipelineRenderer


class PuppetRenderer(ProgrammablePipelineRenderer):
    'Renderer for automated testing'
    def __init__(self, window):
        super(PuppetRenderer, self).__init__()
        self.window = window

        self.io.display_size = glfw.get_framebuffer_size(self.window)

        self._map_keys()
        self._gui_time = None

        self._click = [False] * 3
        self._mouse_buttons = [False] * 3
        self._mouse_pos = -1, -1
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
        self._click[button] = True

    def set_mouse_pos(self, x, y):
        self._mouse_pos = x, y

    def scroll_up(self):
        self._mouse_wheel = 1

    def scroll_dn(self):
        self._mouse_wheel = -1

    def mouse_dn(self, button=0):
        self._mouse_buttons[button] = True

    def mouse_up(self, button=0):
        self._mouse_buttons[button] = False


def create_offscreen_fb(width, height):
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

    # create new framebuffer
    offscreen_fb = gl.glGenFramebuffers(1)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, offscreen_fb)
    # attach texture to framebuffer
    gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, texture, 0)
    return offscreen_fb


def get_fb_data(offscreen_fb, width, height):
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, offscreen_fb)
    pixels = gl.glReadPixels(0, 0, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
    image = Image.frombytes('RGBA', (width, height), pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return image



def main(name, widget_gen, width, height, save_video=None, return_sshot=False):
    """ Create a GLFW window, spin up the main loop, and display a given widget inside.

    The resulting window is not hooked up to the user input. Instead, input is handled
    by a PuppetRenderer instance.

    `widget_gen` takes as an argument a PuppetRenderer instance, and returns a widget.
    """
    imgui.create_context()

    # Set config flags
    imgui.get_io().config_flags |= imgui.CONFIG_DOCKING_ENABLE | imgui.CONFIG_VIEWPORTS_ENABLE

    window = create_window(name, width, height)
    impl = PuppetRenderer(window)
    widget = widget_gen(impl)
    offscreen_fb = create_offscreen_fb(width, height)

    if save_video:
        writer = imageio.get_writer(save_video, mode='I', fps=60)

    while not glfw.window_should_close(window):
        t0 = time.perf_counter()
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        create_window_dock(window)

        try:
            next(widget)
        except StopIteration:
            imgui.render()
            break
        except:
            # Cleanup on exception for iPython
            imgui.render()
            impl.shutdown()
            glfw.terminate()
            raise

        imgui.render()

        if save_video:
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, offscreen_fb)
            impl.render(imgui.get_draw_data())
            image = get_fb_data(offscreen_fb, width, height)
            writer.append_data(np.array(image))

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        t1 = time.perf_counter()
        if t1 - t0 < 1/60:
            time.sleep(1/60 - (t1 - t0))

    if save_video:
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
