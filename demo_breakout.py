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
import yapyg.entities
import yapyg.movers
import yapyg.movers.controlled
import yapyg.controls
import yapyg.collisions
import yapyg.helpers
import yapyg.movers.physical

def create(screen_width, screen_height, tile_size):
    global ENT_PADDLE
    ENT_PADDLE = "500_paddle"
    global ENT_BALL
    ENT_BALL = "500_ball"
    global BALL_MOVE_SPEED
    BALL_MOVE_SPEED = 100
    global BALL_ANIM_SPEED
    BALL_ANIM_SPEED = 3.0 / 1000000
    global BALL_START_POS
    BALL_START_POS = [1, 3]
    BALL_VXY = 2.0 / 1000000

    state = yapyg.factory.create(screen_width, screen_height, tile_size)

    yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/gray_square.png",])
    yapyg.tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

    PADDLE_WIDTH = 1.0 / 2
    PADDLE_HEIGHT = 1.0 / 8
    PADDLE_Y = 2.0
    BOTTOM_Y = 1.5
    BORDER_THICKNESS = 0.1

    yapyg.helpers.create_collision_box(state, "000_screenbox",
        (0, BOTTOM_Y),
        ((screen_width / tile_size), (screen_height / tile_size) - BOTTOM_Y),
        thickness=BORDER_THICKNESS)

    yapyg.entities.insert(state,
        ENT_PADDLE,
        {
            "*": {
                "textures": [("rectangle", PADDLE_WIDTH * tile_size, PADDLE_HEIGHT * tile_size, 1, 1, 1)],
            },
        },
        [1, PADDLE_Y],
        0)
    yapyg.collisions.add(state, ENT_PADDLE, ["rectangle", PADDLE_WIDTH, PADDLE_HEIGHT], False)

    yapyg.entities.insert(state,
        ENT_BALL,
        {
            "*": {
                "textures": [("ellipse", PADDLE_HEIGHT * tile_size, PADDLE_HEIGHT * tile_size, 1, 1, 1)],
            },
        },
        BALL_START_POS,
        0)
    yapyg.collisions.add(state, ENT_BALL, ["circle", PADDLE_HEIGHT])
    yapyg.movers.physical.add(state, ENT_BALL, vx=BALL_VXY, vy=BALL_VXY)

    yapyg.collisions.set_handler(state, collision_handler)

    yapyg.controls.add_joystick(state)
    yapyg.movers.controlled.add(state,
        ENT_PADDLE,
        "joystick",
        0.1,
        [BORDER_THICKNESS, PADDLE_Y, float(screen_width) / tile_size - PADDLE_WIDTH - BORDER_THICKNESS, PADDLE_Y])

    return state

def collision_handler(state, collision_list):
    yapyg.movers.physical.collision_handler(state, collision_list)
