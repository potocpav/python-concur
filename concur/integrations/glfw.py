"""Main integration back-end."""


import glfw
import OpenGL.GL as gl
import time

import imgui
from imgui.integrations.glfw import GlfwRenderer

from concur.integrations.opengl import create_offscreen_fb, get_fb_data


__pdoc__ = dict(create_window=False, begin_maximized_window=False, create_window_dock=False)


class PatchedGlfwRenderer(GlfwRenderer):
    """ Custom variant of Glfwrenderer in PyImGui:

    https://github.com/swistakm/pyimgui/blob/master/imgui/integrations/glfw.py

    This works around the issue that GLFW uses EN_US keyboard to specify the key codes
    in `keyboard_callback`. This meant that keyboard shortcuts were broken on non-querty
    keyboard layouts.

    See https://github.com/ocornut/imgui/issues/2959 for details.

    # Temporary try except fix until we find a better solution, if we don't apply this,
    # the app will crash if certain special keys are pressed.
    """
    def keyboard_callback(self, window, key, scancode, action, mods):
        try:
            _key = key
            if _key < 0x100:
                # Translate characters to the correct keyboard layout.
                key_name = glfw.get_key_name(key, 0)
                if key_name is not None:
                    _key = ord(key_name.upper())
            super(PatchedGlfwRenderer, self).keyboard_callback(window, _key, scancode, action, mods)
        except:
            super(PatchedGlfwRenderer, self).keyboard_callback(window, key, scancode, action, mods)


def create_window(window_name, width, height, visible=True, maximized=False):
    """ Create a GLFW window. """
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    if not visible:
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    if maximized:
        glfw.window_hint(glfw.MAXIMIZED, glfw.TRUE)

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


def begin_maximized_window(name, glfw_window, menu_bar=False):
    imgui.set_next_window_position(0, 0)
    imgui.set_next_window_size(*glfw.get_window_size(glfw_window))
    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
    window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | \
        imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | \
        imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS | \
        imgui.WINDOW_NO_DOCKING
    if menu_bar:
        window_flags |= imgui.WINDOW_MENU_BAR
    imgui.begin(name, True, window_flags)
    imgui.pop_style_var(2)


def create_window_dock(glfw_window, menu_bar=False):
    imgui.set_next_window_bg_alpha(0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
    begin_maximized_window("Background Window", glfw_window, menu_bar)
    imgui.pop_style_var(1)
    imgui.dock_space("Window Dock Space", 0., 0., 1 << 3)
    imgui.end()


def main(
        widget, name="Concur", width=640, height=480,
        fps=60, save_screencast=None, screencast_fps=60,
        menu_bar=False, maximized=False):
    """ Create a GLFW window, spin up the main loop, and display a given widget inside.

    To create a maximized window, pass width and height larger than the screen.

    Args:
        widget: The widget to display inside the window. When the widget returns, the application exits.
        name: Window name, displayed in the title bar and other OS outputs.
        width: Desired window width.
        height: Desired window height.
        fps: Maximum number of frames per second
        save_screencast: Capture and save the UI into a specified video file (experimental). Main window shouldn't
            be resized while the application is running when using this option.
        screencast_fps: Save the screencast video with a given FPS.
        menu_bar: Reserve space for `concur.widgets.main_menu_bar` at the top of the window.
        maximized: Create a maximized window.
    """
    if imgui.get_current_context() is None:
        imgui.create_context()

    # Set config flags
    imgui.get_io().config_flags |= imgui.CONFIG_DOCKING_ENABLE # | imgui.CONFIG_VIEWPORTS_ENABLE

    window = create_window(name, width, height, maximized=maximized)
    impl = PatchedGlfwRenderer(window)

    win_w, win_h = glfw.get_window_size(window)
    fb_w, fb_h = glfw.get_framebuffer_size(window)
    font_scaling_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)
    imgui.get_io().font_global_scale /= font_scaling_factor
    impl.refresh_font_texture()  # Refresh the font texture in case user changed it

    # Using this feels significantly choppier than sleeping manually. TODO: investigate & fix
    # glfw.swap_interval(-1)
    if save_screencast:
        import imageio
        width, height = glfw.get_framebuffer_size(window)
        offscreen_fb = create_offscreen_fb(width, height)
        writer = imageio.get_writer(save_screencast, mode='I', fps=screencast_fps)

    try:
        while not glfw.window_should_close(window):
            t0 = time.perf_counter()
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            create_window_dock(window, menu_bar=menu_bar)
            begin_maximized_window("Default##Concur", window, menu_bar=menu_bar)

            try:
                next(widget)
            except StopIteration:
                break
            finally:
                imgui.end()
                imgui.render()

                gl.glClearColor(0.5, 0.5, 0.5, 1)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

                if save_screencast:
                    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, offscreen_fb)
                    impl.render(imgui.get_draw_data())
                    image = get_fb_data(offscreen_fb, width, height)
                    writer.append_data(image)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

                impl.render(imgui.get_draw_data())
                glfw.swap_buffers(window)

            t1 = time.perf_counter()
            if t1 - t0 < 1/fps:
                time.sleep(1/fps - (t1 - t0))
    finally:
        impl.shutdown()
        imgui.destroy_context(imgui.get_current_context())
        glfw.terminate()
        if save_screencast:
            writer.close()
