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
Tiles
"""

from kivy.graphics import PushMatrix, Rectangle, Fbo, Color, PopMatrix
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

import yapyg.screen
import yapyg.fixpoint
import yapyg.texture_db

tiles_origin_table = (
        ('_', (0,0)),
        ('(', (1,0)),
        ('-', (2,0)),
        (')', (3,0)),

        ('[', (0,1)),
        ('<', (1,1)),
        ('>', (2,1)),
        (']', (3,1)),

        (',', (0,2)),
        (';', (1,2)),
        (':', (2,2)),
        ('.', (3,2)),
        )

def load_walls(state, base_name, background_file, tile_file):
        """
        TODO
        """
        tile_size = yapyg.screen.get_tile_size(state)
        int_tile_size = yapyg.fixpoint.fix2int(tile_size)
        background_texture = Image(source=background_file).texture
        walls_texture = Image(source=tile_file).texture
        for tile_name, origin_xy in tiles_origin_table:
                full_tile_name = base_name + tile_name
                wall_texture = walls_texture.get_region(
                        origin_xy[0] * int_tile_size,
                        origin_xy[1] * int_tile_size,
                        int_tile_size,
                        int_tile_size)

                tile_texture = Texture.create(size=(int_tile_size, int_tile_size), colorfmt='rgba')
                fbo = Fbo(size=(int_tile_size, int_tile_size), texture=tile_texture)
                with fbo:
                        Color(1, 1, 1)
                        Rectangle(pos=(0, 0), size=tile_texture.size, texture=background_texture)
                        Rectangle(pos=(0, 0), size=tile_texture.size, texture=wall_texture)
                fbo.draw()
                yapyg.texture_db.insert(state, full_tile_name, tile_texture)
