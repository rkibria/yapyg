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

cimport fixpoint

import globals
import screen

cpdef initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXTURE_DB] = {}

cpdef destroy(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXTURE_DB] = None

cpdef insert(list state, str texture_name, texture):
        """
        TODO
        """
        cdef dict texturedb
        texturedb = state[globals.IDX_STATE_TEXTURE_DB]
        texturedb[texture_name] = texture

cpdef load(list state, str texture_name, str texture_filename):
        """
        TODO
        """
        cdef dict texturedb
        texturedb = state[globals.IDX_STATE_TEXTURE_DB]
        texturedb[texture_name] = Image(source=texture_filename).texture

cpdef get(list state, str texture_name):
        """
        TODO
        """
        cdef dict texturedb
        texturedb = state[globals.IDX_STATE_TEXTURE_DB]
        if texturedb.has_key(texture_name):
                return texturedb[texture_name]
        else:
                return None

cpdef insert_combined(list state, int texture_size, str texture_name, tuple texture_list):
        """
        TODO
        """
        cdef int tile_size
        tile_size = screen.get_tile_size(state)
        
        texture_size = fixpoint.mul(tile_size, texture_size)
        
        cdef int int_texture_size
        int_texture_size = fixpoint.fix2int(texture_size)

        cdef str texture_filename
        if len(texture_list) == 0:
                return
        elif len(texture_list) == 1:
                # Single texture, just load it and enter it with the
                # tile name as key to texture dict
                load(state, texture_name, texture_list[0])
        else:
                # Combine several textures into one
                texture = Texture.create(size=(int_texture_size, int_texture_size), colorfmt='rgba')
                for texture_filename in texture_list:
                        other_texture = Image(source=texture_filename).texture
                        fbo = Fbo(size=(int_texture_size, int_texture_size), texture=texture)
                        with fbo:
                                Color(1, 1, 1)
                                Rectangle(pos=(0, 0), size=other_texture.size, texture=other_texture)
                        fbo.draw()
                insert(state, texture_name, texture)

cpdef insert_color_rect(list state, float texture_w, float texture_h, str texture_name, float c_r, float c_g, float c_b):
        """
        TODO
        """
        cdef float float_tile_size
        float_tile_size = fixpoint.fix2float(screen.get_tile_size(state))

        cdef int int_texture_w
        cdef int int_texture_h
        int_texture_w = int(texture_w * float_tile_size)
        int_texture_h = int(texture_h * float_tile_size)
        
        texture = Texture.create(size=(int_texture_w, int_texture_h), colorfmt='rgba')
        fbo = Fbo(size=(int_texture_w, int_texture_h), texture=texture)
        with fbo:
                Color(c_r, c_g, c_b)
                Rectangle(pos=(0, 0), size=(int_texture_w, int_texture_h))
        fbo.draw()
        insert(state, texture_name, texture)

cpdef insert_color_ellipse(list state, float texture_w, float texture_h, str texture_name, float c_r, float c_g, float c_b):
        """
        TODO
        """
        cdef float float_tile_size
        float_tile_size = fixpoint.fix2float(screen.get_tile_size(state))

        cdef int int_texture_w
        cdef int int_texture_h
        int_texture_w = int(texture_w * float_tile_size)
        int_texture_h = int(texture_h * float_tile_size)
        
        texture = Texture.create(size=(int_texture_w, int_texture_h), colorfmt='rgba')
        fbo = Fbo(size=(int_texture_w, int_texture_h), texture=texture)
        with fbo:
                Color(c_r, c_g, c_b)
                Ellipse(pos=(0, 0), size=(int_texture_w, int_texture_h))
        fbo.draw()
        insert(state, texture_name, texture)
