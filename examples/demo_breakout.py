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

from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import fixpoint
from yapyg import fixpoint_trig
from yapyg import controls
from yapyg import text
from yapyg import timer
from yapyg import collisions
from yapyg_movers import physical_mover
from yapyg_viewers import relative_viewer
from yapyg_movers import controlled_mover
from yapyg_helpers import entities_helpers
from yapyg_helpers import tiles_helpers

ENT_BLOCK_BASE = "400_block"

def create(screen_width, screen_height, tile_size):
        ENT_PADDLE = "500_paddle"
        ENT_BALL = "500_ball"

        PADDLE_WIDTH = fixpoint.float2fix(1.0 / 2.0)
        PADDLE_HEIGHT = fixpoint.float2fix(1.0 / 8.0)
        PADDLE_Y = fixpoint.float2fix(2.0)
        BOTTOM_Y = fixpoint.float2fix(1.5)
        BORDER_THICKNESS = fixpoint.float2fix(2.0)
        BORDER_OFFSET = fixpoint.float2fix(0.1)

        BALL_MOVE_SPEED = fixpoint.float2fix(100.0)
        BALL_ANIM_SPEED = fixpoint.float2fix(3.0)
        BALL_START_POS = (fixpoint.float2fix(1.0), fixpoint.float2fix(2.0 + 0.5), 0)
        BALL_VXY = fixpoint.float2fix(2.0)
        BLOCK_WIDTH = fixpoint.float2fix(1.78 / 3.5)
        BLOCK_HEIGHT = fixpoint.float2fix(1.0 / 3.5)
        BLOCK_X = fixpoint.float2fix(0.1)
        BLOCK_Y = fixpoint.float2fix(4.5)

        state = factory.create(screen_width, screen_height, tile_size)

        tiles.add_tile_def(state, ".", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

        entities_helpers.create_screen_wall(state, "000_screenbox", BORDER_THICKNESS, BORDER_OFFSET, BOTTOM_Y, color=(0, 0.15, 1))

        for row in xrange(5):
                for col in xrange(7):
                        fix_row = fixpoint.int2fix(row)
                        fix_col = fixpoint.int2fix(col)

                        block_entity_name = ENT_BLOCK_BASE + "_%d_%d" % (col, row)
                        color = (0.5, 0.2, 1) if ((row + col) % 2 == 0) else (0, 1, 0)
                        entities.insert(state,
                                block_entity_name,
                                {
                                        "*": {
                                                "textures": (("rectangle", BLOCK_WIDTH, BLOCK_HEIGHT, color[0], color[1], color[2]),),
                                        },
                                },
                                (BLOCK_X + fixpoint.mul(fix_col, BLOCK_WIDTH), BLOCK_Y + fixpoint.mul(fix_row, BLOCK_HEIGHT), 0),
                                collision=((("rectangle", 0, 0, BLOCK_WIDTH, BLOCK_HEIGHT),)))

        entities.insert(state,
                ENT_PADDLE,
                {
                        "*": {
                                "textures": (("rectangle", PADDLE_WIDTH, PADDLE_HEIGHT, 1, 1, 1),),
                        },
                },
                (fixpoint.float2fix(1.75), PADDLE_Y, 0),
                collision=((("rectangle", 0, 0, PADDLE_WIDTH, PADDLE_HEIGHT),)))

        FIXP_2 = fixpoint.int2fix(2)
        entities.insert(state,
                ENT_BALL,
                {
                        "*": {
                                "textures": (("ellipse", PADDLE_HEIGHT, PADDLE_HEIGHT, 1, 1, 1),),
                        },
                },
                BALL_START_POS,
                collision=(((
                        "circle",
                        fixpoint.div(PADDLE_HEIGHT, FIXP_2),
                        fixpoint.div(PADDLE_HEIGHT, FIXP_2),
                        fixpoint.div(PADDLE_HEIGHT, FIXP_2)),))
                )

        physical_mover.add(state,
                ENT_BALL,
                fixpoint.int2fix(1),
                BALL_VXY,
                BALL_VXY,
                0,
                0,
                fixpoint.int2fix(1),
                fixpoint.int2fix(1),
                0,
                0,
                fixpoint.int2fix(1),
                0,
                )

        collisions.set_handler(state, collision_handler)

        controls.add_joystick(state)

        controlled_mover.add(state,
                ENT_PADDLE,
                "joystick",
                fixpoint.float2fix(0.1),
                [BORDER_OFFSET, PADDLE_Y,
                fixpoint.div(screen_width, tile_size) - PADDLE_WIDTH - BORDER_OFFSET, PADDLE_Y]
                )

        return state

def collision_handler(state, collisions_list):
        for entity_name_1, entity_name_2 in collisions_list:
                if ENT_BLOCK_BASE in entity_name_1:
                        entities.delete(state, entity_name_1)
