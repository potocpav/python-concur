"""Main integration back-end."""


import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
from concur.integrations.opengl import create_offscreen_fb, get_fb_data
import time


__pdoc__ = dict(create_window=False, begin_maximized_window=False, create_window_dock=False)


def create_window(window_name, width, height):
    """ Create a GLFW window. """
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

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


def begin_maximized_window(name, glfw_window):
    imgui.set_next_window_position(0, 0)
    imgui.set_next_window_size(*glfw.get_window_size(glfw_window))
    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
    window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS | imgui.WINDOW_NO_DOCKING
    imgui.begin(name, True, window_flags)
    imgui.pop_style_var(2)


def create_window_dock(glfw_window):
    imgui.set_next_window_bg_alpha(0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
    begin_maximized_window("Background Window", glfw_window)
    imgui.pop_style_var(1)
    imgui.dock_space("Window Dock Space", 0., 0., 1 << 3)
    imgui.end()


def main(name, widget, width, height, save_screencast=None):
    """ Create a GLFW window, spin up the main loop, and display a given widget inside.

    To create a maximized window, pass width and height larger than the screen.

    `save_screencast` is for capturing and saving the UI into a specified video file (experimental).
    """
    imgui.create_context()

    # Set config flags
    imgui.get_io().config_flags |= imgui.CONFIG_DOCKING_ENABLE # | imgui.CONFIG_VIEWPORTS_ENABLE

    window = create_window(name, width, height)
    impl = GlfwRenderer(window)

    ## Using this feels significantly choppier than sleeping manually. TODO: investigate & fix
    # glfw.swap_interval(-1)
    if save_screencast:
        import imageio
        offscreen_fb = create_offscreen_fb(width, height)
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
            if save_screencast:
                writer.close()
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

    impl.shutdown()
    glfw.terminate()
