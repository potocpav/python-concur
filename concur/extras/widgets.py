
import imgui


def simple_image(tex_id, w, h):
    """ Passive fixed-size image widget.

    Takes as an argument OpenGL texture ID, which can be created by raw OpenGL calls, or by the `concur.integrations.opengl.texture` function. """
    pos = imgui.get_cursor_screen_pos()
    uva = 0, 0
    uvb = 1, 1
    draw_list = imgui.get_window_draw_list()
    draw_list.add_image(tex_id, (pos.x, pos.y), (pos.x + w, pos.y + h), uva, uvb);
