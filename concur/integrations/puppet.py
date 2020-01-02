# -*- coding: utf-8 -*-
from __future__ import absolute_import

import glfw
import imgui
import time
import OpenGL.GL as gl

from imgui.integrations import compute_fb_scale
from imgui.integrations.opengl import ProgrammablePipelineRenderer


class PuppetRenderer(ProgrammablePipelineRenderer):
    'Renderer for automated testing'
    def __init__(self, window, attach_callbacks=True):
        super(PuppetRenderer, self).__init__()
        self.window = window

        if attach_callbacks:
            glfw.set_key_callback(self.window, self.keyboard_callback)
            glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
            glfw.set_window_size_callback(self.window, self.resize_callback)
            glfw.set_char_callback(self.window, self.char_callback)
            glfw.set_scroll_callback(self.window, self.scroll_callback)

        self.io.display_size = glfw.get_framebuffer_size(self.window)

        self._map_keys()
        self._gui_time = None

        self._click = [False] * 3
        self._mouse_pos = -1, -1

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

    def keyboard_callback(self, window, key, scancode, action, mods):
        # perf: local for faster access
        io = self.io

        if action == glfw.PRESS:
            io.keys_down[key] = True
        elif action == glfw.RELEASE:
            io.keys_down[key] = False

        io.key_ctrl = (
            io.keys_down[glfw.KEY_LEFT_CONTROL] or
            io.keys_down[glfw.KEY_RIGHT_CONTROL]
        )

        io.key_alt = (
            io.keys_down[glfw.KEY_LEFT_ALT] or
            io.keys_down[glfw.KEY_RIGHT_ALT]
        )

        io.key_shift = (
            io.keys_down[glfw.KEY_LEFT_SHIFT] or
            io.keys_down[glfw.KEY_RIGHT_SHIFT]
        )

        io.key_super = (
            io.keys_down[glfw.KEY_LEFT_SUPER] or
            io.keys_down[glfw.KEY_RIGHT_SUPER]
        )

    def char_callback(self, window, char):
        io = imgui.get_io()

        if 0 < char < 0x10000:
            io.add_input_character(char)

    def resize_callback(self, window, width, height):
        self.io.display_size = width, height

    def mouse_callback(self, *args, **kwargs):
        pass

    def scroll_callback(self, window, x_offset, y_offset):
        self.io.mouse_wheel = y_offset

    def process_inputs(self):
        io = imgui.get_io()

        window_size = glfw.get_window_size(self.window)
        fb_size = glfw.get_framebuffer_size(self.window)

        io.display_size = window_size
        io.display_fb_scale = compute_fb_scale(window_size, fb_size)
        io.delta_time = 1.0/60

        if glfw.get_window_attrib(self.window, glfw.FOCUSED):
            io.mouse_pos = glfw.get_cursor_pos(self.window)
        else:
            io.mouse_pos = -1, -1

        io.mouse_down[0] = glfw.get_mouse_button(self.window, 0)
        io.mouse_down[1] = glfw.get_mouse_button(self.window, 1)
        io.mouse_down[2] = glfw.get_mouse_button(self.window, 2)

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

        io.mouse_pos = self._mouse_pos

    def click(self, button=0):
        self._click[button] = True

    def set_mouse_pos(self, x, y):
        self._mouse_pos = x, y


def create_window(window_name, width, height, maximized):
    """ Create a GLFW window. """
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    if maximized:
        glfw.window_hint(glfw.MAXIMIZED, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


def create_window_dock(glfw_window):
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(*glfw.get_window_size(glfw_window))
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        main_window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS | imgui.WINDOW_NO_DOCKING
        imgui.begin("Background Window", True, main_window_flags)
        imgui.pop_style_var(3)
        imgui.dock_space("Window Dock Space", 0., 0., 0)
        imgui.end()


def main(name, widget_gen, width, height, maximized=False, bg_color=(0.9, 0.9, 0.9), pass_window_to_widget=False):
    """ Create a GLFW window, spin up the main loop, and display a given widget inside.

    If `pass_window_to_widget` is `True`, the `widget` parameter must be a function which takes a GLFW window handle
    and returns a widget. Else, `widget` is just a widget. This is useful if the widget should, for example, scale
    with the GLFW window.
    """
    imgui.create_context()

    # Set config flags
    imgui.get_io().config_flags |= imgui.CONFIG_DOCKING_ENABLE | imgui.CONFIG_VIEWPORTS_ENABLE

    window = create_window(name, width, height, maximized)
    impl = PuppetRenderer(window)
    widget = widget_gen(impl)

    ## Using this feels significantly choppier than sleeping manually. TODO: investigate & fix
    # glfw.swap_interval(-1)

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
            glfw.terminate()
            raise

        gl.glClearColor(*bg_color, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

        t1 = time.perf_counter()
        if t1 - t0 < 1/60:
            time.sleep(1/60 - (t1 - t0))

    impl.shutdown()
    glfw.terminate()
