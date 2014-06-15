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
import yapyg.movers.physical

def create(screen_width, screen_height, tile_size):
        ENT_BOUNCE_TOPWALL = "000_top_wall"
        ENT_BOUNCE_LEFTWALL = "000_left_wall"
        ENT_BOUNCE_RIGHTWALL = "000_right_wall"
        ENT_BOUNCE_BOTTOMWALL = "000_bottom_wall"
        ENT_BOUNCE_BLOCK_1 = "000_block_1"
        ENT_BOUNCE_BLOCK_2 = "100_block_2"

        BALL_SIZE = 1.0 / 8
        SLOW_FACTOR = 1
        BOUNCE_GRAVITY = -0.05 / SLOW_FACTOR
        BOUNCE_VX = 0.5 / SLOW_FACTOR
        BOUNCE_INELASTICITY = 0.95
        BOUNCE_FRICTION = 0.99

        state = yapyg.factory.create(screen_width, screen_height, tile_size)

        yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/gray_square.png",])
        yapyg.tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

        yapyg.entities.insert(state,
                ENT_BOUNCE_BOTTOMWALL,
                {
                        "*": {
                                "textures": [("rectangle", screen_width / tile_size, 1, 0, 0, 1)],
                        },
                },
                [0, -0.5],
                collision=((("rectangle", 0, 0, screen_width / tile_size, 1),)))

        yapyg.entities.insert(state,
                ENT_BOUNCE_TOPWALL,
                {
                        "*": {
                                "textures": [("rectangle", screen_width / tile_size, 1, 0, 0, 1)],
                        },
                },
                [0, -0.5 + screen_height / float(tile_size)],
                collision=((("rectangle", 0, 0, screen_width / tile_size, 1),)))

        yapyg.entities.insert(state,
                ENT_BOUNCE_LEFTWALL,
                {
                        "*": {
                                "textures": [("rectangle", 1, screen_height / tile_size, 0, 0, 1)],
                        }
                },
                [-0.75, 0],
                collision=((("rectangle", 0, 0, 1, screen_height / tile_size),)))

        yapyg.entities.insert(state,
                ENT_BOUNCE_RIGHTWALL,
                {
                        "*": {
                                "textures": [("rectangle", 1, screen_height / tile_size, 0, 0, 1)],
                        }
                },
                [-0.25 + screen_width / tile_size, 0],
                collision=((("rectangle", 0, 0, 1, screen_height / tile_size),)))

        yapyg.entities.insert(state,
                ENT_BOUNCE_BLOCK_1,
                {
                        "*": {
                                "textures": [("rectangle", 1, 1, 0, 0, 1)],
                        }
                },
                [1.5, 0],
                45,
                collision=((("rectangle", 0, 0, 1, 1),)))

        yapyg.entities.insert(state,
                ENT_BOUNCE_BLOCK_2,
                {
                        "*": {
                                "textures": [("rectangle", 1, 1, 0, 0, 1)],
                        }
                },
                [2 - 0.5, 2.5 - 0.5],
                45,
                collision=((("rectangle", 0, 0, 1, 1),)))

        index = 0
        n_rows = 5
        for column in xrange(n_rows):
                for row in xrange(n_rows):
                        ball_entity_name = "900_ball_%d" % index
                        col_red = (column + 1) * (1.0 / (n_rows + 1))
                        col_green = (row + 1) * (1.0 / (n_rows + 1))
                        col_blue = 0.5
                        yapyg.entities.insert(state,
                                ball_entity_name,
                                {
                                        "*": {
                                                "textures": [("ellipse", BALL_SIZE, BALL_SIZE, col_red, col_green, col_blue)],
                                        },
                                },
                                [1 + row * 1.25 * BALL_SIZE + column * 0.0, 4.5 + column * 1.25 * BALL_SIZE],
                                collision=(("circle", BALL_SIZE / 2, BALL_SIZE / 2, BALL_SIZE / 2,),))
                        yapyg.movers.physical.add(state, ball_entity_name,
                                ay=BOUNCE_GRAVITY,
                                vx=BOUNCE_VX,
                                inelasticity=BOUNCE_INELASTICITY,
                                friction=BOUNCE_FRICTION)
                        index += 1

        yapyg.collisions.set_handler(state, collision_handler)

        return state

def collision_handler(state, collision_list):
        yapyg.movers.physical.collision_handler(state, collision_list)
