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

import yapyg.factory
import yapyg.screen
import yapyg.movers.linear
import yapyg.movers.jump
import yapyg.movers.set_property
import yapyg.movers.wait
import yapyg.view
import yapyg.viewers.relative

def create(screen_width, screen_height, tile_size):
    global ENT_BOUNCE_TOPWALL
    ENT_BOUNCE_TOPWALL = "top_wall"
    global ENT_BOUNCE_LEFTWALL
    ENT_BOUNCE_LEFTWALL = "left_wall"
    global ENT_BOUNCE_RIGHTWALL
    ENT_BOUNCE_RIGHTWALL = "right_wall"
    global ENT_BOUNCE_BOTTOMWALL
    ENT_BOUNCE_BOTTOMWALL = "bottom_wall"
    global ENT_BOUNCE_BALL
    ENT_BOUNCE_BALL = "ball"
    global BOUNCE_BALL_ANIM_SPEED
    BOUNCE_BALL_ANIM_SPEED = 3.0 / 1000000
    BALL_SIZE = 1.0 / 8

    state = yapyg.factory.create(screen_width, screen_height, tile_size)

    yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/gray_square.png",])
    yapyg.tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

    yapyg.entities.insert(state,
        ENT_BOUNCE_BOTTOMWALL,
        {
            "*": {
                "textures": [("rectangle", screen_width, tile_size, 0, 0, 0)],
            },
        },
        [0, -1],
        0)
    yapyg.collisions.add(state, ENT_BOUNCE_BOTTOMWALL, ["rectangle", float(screen_width) / tile_size, 1], False)

    yapyg.entities.insert(state,
        ENT_BOUNCE_TOPWALL,
        {
            "*": {
                "textures": [("rectangle", screen_width, tile_size, 0, 0, 0)],
            },
        },
        [0, screen_height / float(tile_size)],
        0)
    yapyg.collisions.add(state, ENT_BOUNCE_TOPWALL, ["rectangle", float(screen_width) / tile_size, 1], False)

    yapyg.entities.insert(state,
        ENT_BOUNCE_LEFTWALL,
        {
            "*": {
                "textures": [("rectangle", tile_size, screen_height, 0, 0, 0)],
            }
        },
        [-1, 0],
        0)
    yapyg.collisions.add(state, ENT_BOUNCE_LEFTWALL, ["rectangle", 1, float(screen_height) / tile_size], False)

    yapyg.entities.insert(state,
        ENT_BOUNCE_RIGHTWALL,
        {
            "*": {
                "textures": [("rectangle", tile_size, screen_height, 0, 0, 0)],
            }
        },
        [float(screen_width) / tile_size, 0],
        0)
    yapyg.collisions.add(state, ENT_BOUNCE_RIGHTWALL, ["rectangle", 1, float(screen_height) / tile_size], False)

    yapyg.entities.insert(state,
        ENT_BOUNCE_BALL,
        {
            "*": {
                "textures": [("ellipse", BALL_SIZE * tile_size, BALL_SIZE * tile_size, 1, 1, 1)],
            },
        },
        [1.5, 3],
        0)
    yapyg.collisions.add(state, ENT_BOUNCE_BALL, ["circle", BALL_SIZE])

    yapyg.collisions.set_handler(state, collision_handler)

    return state

def collision_handler(state, collision_list):
    pass
