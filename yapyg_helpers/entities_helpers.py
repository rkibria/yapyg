# Copyright (c) 2015 Raihan Kibria
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
Helpers for recurring tasks
"""

from yapyg import entities
from yapyg import screen


def create_screen_wall(state, base_name, border_thickness, border_offset, bottom_y, top=True, bottom=True, left=True, right=True, color=(1,1,1)):
        """
        TODO
        """
        screen_width = screen.get_width(state)
        screen_height = screen.get_height(state)
        tile_size = screen.get_tile_size(state)

        pos = (-border_thickness + border_offset, -border_thickness + bottom_y + border_offset)
        size_w = (
                (screen_width / tile_size)
                + (2.0 * border_thickness)
                - (2.0 * border_offset)
                )
        size_h = (
                (screen_height / tile_size)
                - bottom_y + (2.0 * border_thickness)
                - (2.0 * ( border_offset))
                )

        create_collision_box(state, base_name,
                pos,
                (size_w, size_h),
                border_thickness,
                top,
                bottom,
                left,
                right,
                color,
                )

def create_collision_box(state, base_name, pos, size, thickness, top=True, bottom=True, left=True, right=True, color=(1,1,1)):
        """
        TODO
        """
        ENT_TOPWALL = base_name + "_top"
        ENT_LEFTWALL = base_name + "_left"
        ENT_RIGHTWALL = base_name + "_right"
        ENT_BOTTOMWALL = base_name + "_bottom"

        horizontal_wall_width = size[0]
        vertical_wall_height = size[1]

        if bottom:
                entities.insert(state,
                        ENT_BOTTOMWALL,
                        {
                                "*": {
                                        "textures": (("rectangle",
                                                horizontal_wall_width,
                                                thickness,
                                                color[0], color[1], color[2],),),
                                },
                        },
                        (pos[0], pos[1], 0),
                        collision=((("rectangle", 0, 0, horizontal_wall_width, thickness),)))

        if left:
                entities.insert(state,
                        ENT_LEFTWALL,
                        {
                                "*": {
                                        "textures": (("rectangle",
                                                thickness,
                                                vertical_wall_height,
                                                color[0], color[1], color[2],),),
                                },
                        },
                        (pos[0], pos[1], 0),
                        collision=((("rectangle", 0, 0, thickness, vertical_wall_height),)))

        if top:
                entities.insert(state,
                        ENT_TOPWALL,
                        {
                                "*": {
                                        "textures": (("rectangle",
                                                horizontal_wall_width,
                                                thickness,
                                                color[0], color[1], color[2],),),
                                },
                        },
                        (pos[0], pos[1] + vertical_wall_height - thickness, 0),
                        collision=((("rectangle", 0, 0, horizontal_wall_width, thickness),)))

        if right:
                entities.insert(state,
                        ENT_RIGHTWALL,
                        {
                                "*": {
                                        "textures": (("rectangle",
                                                thickness,
                                                vertical_wall_height,
                                                color[0], color[1], color[2],),),
                                },
                        },
                        (pos[0] + horizontal_wall_width - thickness, pos[1], 0),
                        collision=((("rectangle", 0, 0, thickness, vertical_wall_height),)))
