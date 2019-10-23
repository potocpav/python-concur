
import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
import time


def main(widget, name, width, height, maximized=False, bg_color=(0.9, 0.9, 0.9)):
    """ Create a GLFW window, spin up the main loop, and display a given widget inside. """
    imgui.create_context()
    window = create_window(name, width, height, maximized)
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        time.sleep(1/60)

        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        try:
            next(widget)
        except StopIteration:
            exit(1)
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

    impl.shutdown()
    glfw.terminate()


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
