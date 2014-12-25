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

import yapyg
import yapyg_movers.linear_mover
import yapyg_helpers.tiles

from yapyg.fixpoint import int2fix, float2fix, fix2int, div

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        tiles.add_tile_def(state, " ", ("assets/img/tiles/gray_square.png",))
        tiles.add_tile_def(state, "#", ("assets/img/tiles/plain.png",))
        area_strings = (
                "             ",
                "             ",
                " #           ",
                "             ",
                "             ",
                "             ",
                )
        area = yapyg_helpers.tiles.strings_to_chars(area_strings)
        tiles.set_area(state, area)

        BALL_SIZE = float2fix(1.0 / 4.0)
        CIRCLE_RADIUS = fixpoint.div(BALL_SIZE, int2fix(2))
        filename = "assets/img/sprites/quarter_ball.png"
        entity_name = "500_ship"
        entities.insert(state,
                entity_name,
                {
                        "*": {
                                "textures": (filename,),
                        },
                },
                (float2fix(1.5), float2fix(1), 0,),
                collision=(("circle", CIRCLE_RADIUS, CIRCLE_RADIUS, CIRCLE_RADIUS,),))
        yapyg_movers.linear.add(state, entity_name, (int2fix(0), int2fix(5)), float2fix(1.5))

        return state
