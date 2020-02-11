"""Raw OpenGL functions, mostly for creating and deleting textures."""

import numpy as np
from PIL import Image
from OpenGL.GL import *


__pdoc__ = dict(create_offscreen_fb=False, get_fb_data=False)


def texture(arr):
    """ Create a new OpenGL texture and return its texture ID. """
    if len(arr.shape) == 2:
        arr = np.tile(np.expand_dims(arr, 2), (1, 1, 3))

    if len(arr.shape) == 3:
        if arr.shape[2] == 4:
            rgb_mode = GL_RGBA
        elif arr.shape[2] == 3:
            rgb_mode = GL_RGB
        else:
            raise ValueError(f"Only RGB or RGBA channels supported, instead found {arr.shape[2]} color channels.")
    else:
        raise ValueError(f"Shape rank has to be 2 or 3, but it is {len(arr.shape)}")

    texid = int(glGenTextures(1)) # Conversion from np.uint32 to int
    glBindTexture(GL_TEXTURE_2D, texid)
    # If the array isn't normalized, glTexImage2D may leak reference count
    glTexImage2D(GL_TEXTURE_2D, 0, rgb_mode, arr.shape[1], arr.shape[0],
                 0, rgb_mode, GL_UNSIGNED_BYTE, np.ascontiguousarray(arr, 'u1'))
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    return texid


def rm_textures(tex_ids):
    """ Delete a list of OpenGL textures. """
    glDeleteTextures(tex_ids)


def rm_texture(tex_id):
    """ Delete a single OpenGL texture. """
    glDeleteTextures([tex_id])


def replace_texture(arr, prev_tex_id):
    """ Convenience function: delete the texture `prev_tex_id`, if not `None`, and create a new one,
    returning its texture ID.
    """
    if prev_tex_id is not None:
        rm_texture(prev_tex_id)
    return texture(arr)


def create_offscreen_fb(width, height):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # create new framebuffer
    offscreen_fb = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, offscreen_fb)
    # attach texture to framebuffer
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)
    return offscreen_fb


def get_fb_data(offscreen_fb, width, height):
    glBindFramebuffer(GL_FRAMEBUFFER, offscreen_fb)
    pixels = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes('RGBA', (width, height), pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return np.array(image)
