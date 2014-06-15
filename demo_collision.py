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

def create(screen_width, screen_height, tile_size):
        BOTTOM_Y = 0
        BORDER_THICKNESS = 2.0
        BORDER_OFFSET = 0

        global ENT_BALL
        ENT_BALL = "500_ball"
        global BALL_MOVE_SPEED
        BALL_MOVE_SPEED = 100
        global BALL_START_POS
        BALL_SIZE = 1.0 / 32.0
        BALL_START_POS = [2 * BORDER_OFFSET, 2 * BORDER_OFFSET + 0.1]
        BALL_VXY = 2.0
        BLOCK_WIDTH = 0.1
        BLOCK_HEIGHT = 0.1
        BLOCK_X = 1.0
        BLOCK_Y = 0.0
        global ENT_BLOCK_BASE
        ENT_BLOCK_BASE = "400_block"

        state = yapyg.factory.create(screen_width, screen_height, tile_size)

        yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/gray_square.png",])
        yapyg.tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

        yapyg.helpers.create_collision_box(state, "000_screenbox",
                (-BORDER_THICKNESS + BORDER_OFFSET, -BORDER_THICKNESS + BOTTOM_Y + BORDER_OFFSET),
                ((screen_width / tile_size) + 2 * BORDER_THICKNESS - 2 * BORDER_OFFSET,
                (screen_height / tile_size) - BOTTOM_Y + 2 * BORDER_THICKNESS - 2 * BORDER_OFFSET),
                thickness=BORDER_THICKNESS, color=(0.1, 0.1, 0.1))

        for row in xrange(52):
                for col in xrange(30):
                        block_entity_name = ENT_BLOCK_BASE + "_%d_%d" % (col, row)
                        color = (0.5, 0.2, 1) if ((row + col) % 2 == 0) else (0, 1, 0)
                        yapyg.entities.insert(state,
                                block_entity_name,
                                {
                                        "*": {
                                                "textures": [("rectangle", BLOCK_WIDTH, BLOCK_HEIGHT, color[0], color[1], color[2])],
                                        },
                                },
                                [BLOCK_X + col * BLOCK_WIDTH, BLOCK_Y + row * BLOCK_HEIGHT],
                                collision=((("rectangle", 0, 0, BLOCK_WIDTH, BLOCK_HEIGHT),)))

        yapyg.entities.insert(state,
                ENT_BALL,
                {
                        "*": {
                                "textures": [("ellipse", BALL_SIZE, BALL_SIZE, 0, 1, 0)],
                        },
                },
                BALL_START_POS,
                collision=((("circle", BALL_SIZE / 2.0, BALL_SIZE / 2.0, BALL_SIZE / 2.0),)))
        yapyg.movers.physical.add(state, ENT_BALL, vx=BALL_VXY, vy=BALL_VXY)
        
        yapyg.collisions.set_handler(state, collision_handler)

        return state

def collision_handler(state, collision_list):
        yapyg.movers.physical.collision_handler(state, collision_list)
