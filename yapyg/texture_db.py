# Copyright (c) 2014 Raihan Kibria
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Texture storage and operations
"""

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle, Fbo, Ellipse

import globals
import screen

class YapygTextureDbException(Exception):
        """
        TODO
        """
        def __init__(self, value):
                """
                TODO
                """
                self.value = value

        def __str__(self):
                """
                TODO
                """
                return repr(self.value)

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXTURE_DB] = {}

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXTURE_DB] = None

def insert(state, texture_name, texture):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXTURE_DB][texture_name] = texture

def load(state, texture_name, texture_filename):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXTURE_DB][texture_name] = Image(source=texture_filename).texture

def get(state, texture_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_TEXTURE_DB].has_key(texture_name):
                return state[globals.IDX_STATE_TEXTURE_DB][texture_name]
        else:
                raise YapygTextureDbException("Texture '" + texture_name + "' not present")

def insert_combined(state, texture_size, texture_name, texture_list):
        """
        TODO
        """
        tile_size = screen.get_tile_size(state)
        texture_size *= tile_size

        if len(texture_list) == 0:
                raise YapygTextureDbException("insert_combined() called with empty list")
        elif len(texture_list) == 1:
                # Single texture, just load it and enter it with the
                # tile name as key to texture dict
                load(state, texture_name, texture_list[0])
        else:
                # Combine several textures into one
                texture = Texture.create(size=(texture_size, texture_size), colorfmt='rgba')
                for texture_filename in texture_list:
                        other_texture = Image(source=texture_filename).texture
                        fbo = Fbo(size=(texture_size, texture_size), texture=texture)
                        with fbo:
                                Color(1, 1, 1)
                                Rectangle(pos=(0, 0), size=other_texture.size, texture=other_texture)
                        fbo.draw()
                insert(state, texture_name, texture)

def insert_color_rect(state, texture_w, texture_h, texture_name, c_r, c_g, c_b):
        """
        TODO
        """
        tile_size = screen.get_tile_size(state)
        texture_w *= tile_size
        texture_h *= tile_size

        texture = Texture.create(size=(texture_w, texture_h), colorfmt='rgba')
        fbo = Fbo(size=(texture_w, texture_h), texture=texture)
        with fbo:
                Color(c_r, c_g, c_b)
                Rectangle(pos=(0, 0), size=(texture_w, texture_h))
        fbo.draw()
        insert(state, texture_name, texture)

def insert_color_ellipse(state, texture_w, texture_h, texture_name, c_r, c_g, c_b):
        """
        TODO
        """
        tile_size = screen.get_tile_size(state)
        texture_w *= tile_size
        texture_h *= tile_size

        texture = Texture.create(size=(texture_w, texture_h), colorfmt='rgba')
        fbo = Fbo(size=(texture_w, texture_h), texture=texture)
        with fbo:
                Color(c_r, c_g, c_b)
                Ellipse(pos=(0, 0), size=(texture_w, texture_h))
        fbo.draw()
        insert(state, texture_name, texture)
