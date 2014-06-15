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

import globals
import texture_db
import view
import screen
import fixpoint

IDX_TILES_SIZE = 0
IDX_TILES_DEFS = 1
IDX_TILES_AREA = 2
IDX_TILES_RECTS = 3

def initialize(state, tile_size):
        """
        TODO
        """
        state[globals.IDX_STATE_TILES] = [
                fixpoint.float2fix(float(tile_size)),
                {},
                [],
                [],]
        add_tile_def(state, "tl_null", ["assets/img/tiles/no_tile.png",])

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_TILES] = None

def get_tile_size(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_TILES][IDX_TILES_SIZE]

def set_area(state, area):
        """
        TODO
        """
        state[globals.IDX_STATE_TILES][IDX_TILES_AREA] = area

def get_area(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_TILES][IDX_TILES_AREA]

def add_tile_def(state, tile_name, texture_list):
        """
        TODO
        """
        state[globals.IDX_STATE_TILES][IDX_TILES_DEFS][tile_name] = {}
        state[globals.IDX_STATE_TILES][IDX_TILES_DEFS][tile_name]["textures"] = texture_list
        texture_db.insert_combined(state, fixpoint.FIXP_1, tile_name, texture_list)

tiles_origin_table = (
        ('0', (0,0)),
        ('1', (1,0)),
        ('2', (2,0)),
        ('3', (3,0)),

        ('4', (0,1)),
        ('5', (1,1)),
        ('6', (2,1)),
        ('7', (3,1)),

        ('8', (0,2)),
        ('9', (1,2)),
        ('a', (2,2)),
        ('b', (3,2)),

        ('c', (0,3)),
        ('d', (1,3)),
        ('e', (2,3)),
        ('f', (3,3)),
        )

def load_walls(state, base_name, background_file, tile_file):
        """
        TODO
        """
        tile_size = screen.get_tile_size(state)
        int_tile_size = fixpoint.fix2int(tile_size)
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
                texture_db.insert(state, full_tile_name, tile_texture)

def get_tile(state, row, col):
        """
        row = 0 is the most southern part of the map
        col = 0 is the most western part of the map
        -> 0/0 is the lower left corner
        """
        area = get_area(state)
        row = int(row)
        maxrows = len(area)
        if row < 0 or row >= maxrows:
                return None
        col = int(col)
        rowdata = area[maxrows - row - 1]
        if col < 0 or col >= len(rowdata):
                return None
        return rowdata[col]

def draw(state, scale, canvas, view_size):
        """
        TODO
        """
        origin_xy = screen.get_origin(state)

        target_w = view_size[0]
        target_h = view_size[1]

        scaled_tile_size = fixpoint.mul(get_tile_size(state), scale)
        view_pos = view.get_view_pos(state)
        map_x = fixpoint.mul(view_pos[0], scaled_tile_size)
        map_y = fixpoint.mul(view_pos[1], scaled_tile_size)

        first_row = fixpoint.fix2int(fixpoint.div(map_y, scaled_tile_size))
        total_rows = fixpoint.fix2int(fixpoint.div(target_h, scaled_tile_size))

        first_col = fixpoint.fix2int(fixpoint.div(map_x, scaled_tile_size))
        total_cols = fixpoint.fix2int(fixpoint.div(target_w, scaled_tile_size))

        tile_rects = state[globals.IDX_STATE_TILES][IDX_TILES_RECTS]

        tile_index = 0
        with canvas:
                for row in xrange(first_row, first_row + total_rows + 2):
                        for col in xrange(first_col, first_col + total_cols + 2):

                                tile_x = fixpoint.mul(fixpoint.int2fix(col), scaled_tile_size)
                                tile_y = fixpoint.mul(fixpoint.int2fix(row), scaled_tile_size)

                                draw_pos = (
                                        fixpoint.fix2int((tile_x - map_x) + origin_xy[0]),
                                        fixpoint.fix2int((tile_y - map_y) + origin_xy[1]))

                                texture = texture_db.get(state, "tl_null")
                                tile = get_tile(state, row, col)
                                if tile:
                                        texture = texture_db.get(state, tile)

                                draw_size = (
                                        fixpoint.fix2int(fixpoint.mul(fixpoint.int2fix(texture.width), scale)),
                                        fixpoint.fix2int(fixpoint.mul(fixpoint.int2fix(texture.height), scale)),)

                                if tile_index >= len(tile_rects):
                                        PushMatrix()
                                        tile_rect = Rectangle(texture=texture,
                                                pos=draw_pos,
                                                size=draw_size)
                                        tile_rects.append(tile_rect)
                                        PopMatrix()
                                else:
                                        tile_rect = tile_rects[tile_index]
                                        if tile_rect.pos != draw_pos:
                                                tile_rect.pos = draw_pos
                                        if tile_rect.size != draw_size:
                                                tile_rect.size = draw_size
                                        if not tile_rect.texture is texture:
                                                tile_rect.texture = texture
                                tile_index += 1
