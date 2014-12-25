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

from yapyg import screen
from yapyg import fixpoint
from yapyg import tiles

TILE_SIZE = fixpoint.float2fix(1.0)
WALL_WIDTH = fixpoint.float2fix(1.0 / 4.0)
OFFSET_WALL = TILE_SIZE - WALL_WIDTH - WALL_WIDTH
SOUTH_WALL = ("rectangle", 0, 0, TILE_SIZE, WALL_WIDTH)
WEST_WALL = ("rectangle", 0, 0, WALL_WIDTH, TILE_SIZE)
NORTH_WALL = ("rectangle", 0, OFFSET_WALL, TILE_SIZE, WALL_WIDTH)
EAST_WALL = ("rectangle", OFFSET_WALL, 0, WALL_WIDTH, TILE_SIZE)
tiles_origin_table = (
        ('_', (0,0), (SOUTH_WALL,)),
        ('(', (1,0), (WEST_WALL,)),
        ('-', (2,0), (NORTH_WALL,)),
        (')', (3,0), (EAST_WALL,)),

        ('[', (0,1), (SOUTH_WALL, WEST_WALL)),
        ('<', (1,1), (NORTH_WALL, WEST_WALL)),
        ('>', (2,1), (NORTH_WALL, EAST_WALL)),
        (']', (3,1), (SOUTH_WALL, EAST_WALL)),

        (',', (0,2), (("rectangle", 0, 0, WALL_WIDTH, WALL_WIDTH),)),
        (';', (1,2), (("rectangle", 0, OFFSET_WALL, WALL_WIDTH, WALL_WIDTH),)),
        (':', (2,2), (("rectangle", OFFSET_WALL, OFFSET_WALL, WALL_WIDTH, WALL_WIDTH),)),
        ('.', (3,2), (("rectangle", OFFSET_WALL, 0, WALL_WIDTH, WALL_WIDTH),)),
        )

def load_walls(state, base_name, background_file, tile_file, with_collisions=True):
        """
        TODO
        """
        tile_size = screen.get_tile_size(state)
        int_tile_size = fixpoint.fix2int(tile_size)
        background_texture = Image(source=background_file).texture
        walls_texture = Image(source=tile_file).texture
        for tile_name, origin_xy, collision in tiles_origin_table:
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
                if not with_collisions:
                        collision = None
                tiles.add_tile_def(state, full_tile_name, tile_texture, collision)

def strings_to_chars(area_strings):
        """
        TODO
        """
        area = []
        for area_string_row in area_strings:
                new_row = []
                area.append(new_row)
                for tile in area_string_row:
                        new_row.append(tile)
        return area
