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

from kivy.logger import Logger

from kivy.graphics import PushMatrix, Rectangle, Fbo, Color, PopMatrix
from kivy.uix.image import Image

import texture_db
import view
import screen

def initialize(state, tile_size):
    """
    TODO
    """
    state["tiles"] = {
        "size": tile_size,
        "defs": {},
        "area": [],
        "tile_rects": [],
    }
    add_tile_def(state, "tl_null", ["assets/img/tiles/no_tile.png",])

def destroy(state):
    """
    TODO
    """
    del state["tiles"]

def get_tile_size(state):
    """
    TODO
    """
    return state["tiles"]["size"]

def set_area(state, area):
    """
    TODO
    """
    state["tiles"]["area"] = area

def get_area(state):
    """
    TODO
    """
    return state["tiles"]["area"]

def add_tile_def(state, tile_name, texture_list):
    state["tiles"]["defs"][tile_name] = {}
    state["tiles"]["defs"][tile_name]["textures"] = texture_list
    texture_db.insert_combined(state, 1, tile_name, texture_list)

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

    scaled_tile_size = get_tile_size(state) * scale
    view_pos = view.get_view_pos(state)
    map_x = view_pos[0] * scaled_tile_size
    map_y = view_pos[1] * scaled_tile_size

    first_row = int(map_y / scaled_tile_size)
    total_rows = int(target_h / scaled_tile_size)

    first_col = int(map_x / scaled_tile_size)
    total_cols = int(target_w / scaled_tile_size)

    tile_rects = state["tiles"]["tile_rects"]

    tile_index = 0
    with canvas:
        for row in xrange(first_row, first_row + total_rows + 2):
            for col in xrange(first_col, first_col + total_cols + 2):
                tile_x = col * scaled_tile_size
                tile_y = row * scaled_tile_size
                draw_x = (tile_x - map_x) + origin_xy[0]
                draw_y = (tile_y - map_y) + origin_xy[1]
                draw_pos = (draw_x, draw_y)
                texture = texture_db.get(state, "tl_null")
                tile = get_tile(state, row, col)

                if tile:
                    texture = texture_db.get(state, tile)
                draw_size = (texture.width * scale, texture.height * scale,)

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
