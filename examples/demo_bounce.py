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
from yapyg_helpers import entities_helpers
from yapyg_movers import physical_mover

def create(screen_width, screen_height, tile_size):
        ENT_BOUNCE_BLOCK_1 = "000_block_1"
        ENT_BOUNCE_BLOCK_2 = "100_block_2"

        BOUNCE_VX = fixpoint.float2fix(0.0)
        BOTTOM_Y = fixpoint.float2fix(0.5)
        BORDER_THICKNESS = fixpoint.float2fix(2.0)
        BORDER_OFFSET = fixpoint.float2fix(0.1)

        WALLS_COLOR = (0.3, 0.45, 1)

        state = factory.create(screen_width, screen_height, tile_size)

        tiles.add_tile_def(state, " ", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [[" " for x in xrange(10)] for x in xrange(10)])

        entities_helpers.create_screen_wall(state, "000_screenbox", BORDER_THICKNESS, BORDER_OFFSET, BOTTOM_Y, color=WALLS_COLOR)

        BLOCK_SIZE = fixpoint.float2fix(2.75)
        BLOCK_OFFSET = fixpoint.float2fix(-0.15)
        BLOCK_Y = fixpoint.float2fix(1.0)

        entities.insert(state,
                ENT_BOUNCE_BLOCK_1,
                {
                        "*": {
                                "textures": (("rectangle", BLOCK_SIZE, BLOCK_SIZE, WALLS_COLOR[0], WALLS_COLOR[1], WALLS_COLOR[2]),),
                        }
                },
                (fixpoint.float2fix(-1.5) + BLOCK_OFFSET, BLOCK_Y, fixpoint.float2fix(45.0)),
                collision=((("rectangle", 0, 0, BLOCK_SIZE, BLOCK_SIZE),)))

        entities.insert(state,
                ENT_BOUNCE_BLOCK_2,
                {
                        "*": {
                                "textures": (("rectangle", BLOCK_SIZE, BLOCK_SIZE, WALLS_COLOR[0], WALLS_COLOR[1], WALLS_COLOR[2]),),
                        }
                },
                (fixpoint.float2fix(2.75) + BLOCK_OFFSET, BLOCK_Y, fixpoint.float2fix(45.0)),
                collision=((("rectangle", 0, 0, BLOCK_SIZE, BLOCK_SIZE),)))

        index = 0
        n_rows = 6
        n_columns = 4

        BOUNCE_GRAVITY = fixpoint.float2fix(-20.0)
        BOUNCE_INELASTICITY = fixpoint.float2fix(0.9)
        BOUNCE_FRICTION = fixpoint.float2fix(0.95)
        BOUNCE_STICKYNESS = fixpoint.float2fix(0.5)

        BALL_DISTANCE = fixpoint.float2fix(1.0 / 4.0)
        ROT_FRICTION = fixpoint.float2fix(0.35)
        ROT_DECAY = fixpoint.float2fix(0.9)

        for column in xrange(n_columns):
                for row in xrange(n_rows):
                        ball_entity_name = "900_ball_%d" % index

                        if index % 2 == 0:
                                BALL_SIZE = fixpoint.float2fix(1.0 / 4.0)
                                CIRCLE_RADIUS = fixpoint.div(BALL_SIZE, fixpoint.int2fix(2))
                                filename = "assets/img/sprites/quarter_ball.png"
                                mass = fixpoint.int2fix(1)
                        else:
                                # index += 1
                                # continue
                                BALL_SIZE = fixpoint.float2fix(1.0 / 8.0)
                                CIRCLE_RADIUS = fixpoint.div(BALL_SIZE, fixpoint.int2fix(2))
                                filename = "assets/img/sprites/eigth_ball.png"
                                mass = fixpoint.int2fix(1)

                        entities.insert(state,
                                ball_entity_name,
                                {
                                        "*": {
                                                "textures": (filename,),
                                        },
                                },
                                (
                                        fixpoint.float2fix(1.0) + fixpoint.mul(fixpoint.int2fix(row), fixpoint.mul(BALL_DISTANCE, fixpoint.float2fix(1.25))),
                                        fixpoint.float2fix(4.5) + fixpoint.mul(fixpoint.mul(fixpoint.int2fix(column), fixpoint.float2fix(1.25)), fixpoint.mul(BALL_DISTANCE, fixpoint.float2fix(1.25))),
                                        0,
                                ),
                                collision=(("circle", CIRCLE_RADIUS, CIRCLE_RADIUS, CIRCLE_RADIUS,),))

                        physical_mover.add(state,
                                ball_entity_name,
                                mass,
                                BOUNCE_VX,
                                0,
                                0,
                                BOUNCE_GRAVITY,
                                BOUNCE_FRICTION,
                                BOUNCE_INELASTICITY,
                                0,
                                ROT_FRICTION,
                                ROT_DECAY,
                                BOUNCE_STICKYNESS,
                                )

                        index += 1

        return state
