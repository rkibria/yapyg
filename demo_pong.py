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

def create(screen_width, screen_height, tile_size):
    global ENT_PONG_PADDLE
    ENT_PONG_PADDLE = "paddle"
    global ENT_PONG_TOPWALL
    ENT_PONG_TOPWALL = "top_wall"
    global ENT_PONG_LEFTWALL
    ENT_PONG_LEFTWALL = "left_wall"
    global ENT_PONG_RIGHTWALL
    ENT_PONG_RIGHTWALL = "right_wall"
    global ENT_PONG_BOTTOMWALL
    ENT_PONG_BOTTOMWALL = "bottom_wall"
    global ENT_PONG_BALL
    ENT_PONG_BALL = "ball"
    global PONG_BALL_MOVE_SPEED
    PONG_BALL_MOVE_SPEED = 100
    global PONG_BALL_ANIM_SPEED
    PONG_BALL_ANIM_SPEED = 3.0 / 1000000
    global PONG_BALL_START_POS
    PONG_BALL_START_POS = [1, 3]

    state = yapyg.factory.create(screen_width, screen_height, tile_size)

    PADDLE_WIDTH = 1.0 / 2
    PADDLE_HEIGHT = 1.0 / 8

    PADDLE_Y = 1.5
    yapyg.entities.insert(state,
        ENT_PONG_PADDLE,
        {
            "std": {
                "textures": [("rectangle", PADDLE_WIDTH * tile_size, PADDLE_HEIGHT * tile_size, 1, 1, 1)],
            },
        },
        [1, PADDLE_Y],
        0)
    yapyg.entities.set_sprite(state, ENT_PONG_PADDLE, "std")
    yapyg.collisions.add(state, ENT_PONG_PADDLE, ["rectangle", PADDLE_WIDTH, PADDLE_HEIGHT], False)

    yapyg.entities.insert(state,
        ENT_PONG_BOTTOMWALL,
        {
            "std": {
                "textures": [("rectangle", screen_width, tile_size, 0, 0, 0)],
            },
        },
        [0, PADDLE_Y - 1 - 2 * PADDLE_HEIGHT],
        0)
    yapyg.entities.set_sprite(state, ENT_PONG_BOTTOMWALL, "std")
    yapyg.collisions.add(state, ENT_PONG_BOTTOMWALL, ["rectangle", float(screen_width) / tile_size, 1], False)

    yapyg.entities.insert(state,
        ENT_PONG_TOPWALL,
        {
            "std": {
                "textures": [("rectangle", screen_width, tile_size, 0, 0, 0)],
            },
        },
        [0, screen_height / float(tile_size)],
        0)
    yapyg.entities.set_sprite(state, ENT_PONG_TOPWALL, "std")
    yapyg.collisions.add(state, ENT_PONG_TOPWALL, ["rectangle", float(screen_width) / tile_size, 1], False)

    yapyg.entities.insert(state,
        ENT_PONG_LEFTWALL,
        {
            "std": {
                "textures": [("rectangle", tile_size, screen_height, 0, 0, 0)],
            }
        },
        [-1, 0],
        0)
    yapyg.entities.set_sprite(state, ENT_PONG_LEFTWALL, "std")
    yapyg.collisions.add(state, ENT_PONG_LEFTWALL, ["rectangle", 1, float(screen_height) / tile_size], False)

    yapyg.entities.insert(state,
        ENT_PONG_RIGHTWALL,
        {
            "std": {
                "textures": [("rectangle", tile_size, screen_height, 0, 0, 0)],
            }
        },
        [float(screen_width) / tile_size, 0],
        0)
    yapyg.entities.set_sprite(state, ENT_PONG_RIGHTWALL, "std")
    yapyg.collisions.add(state, ENT_PONG_RIGHTWALL, ["rectangle", 1, float(screen_height) / tile_size], False)

    yapyg.entities.insert(state,
        ENT_PONG_BALL,
        {
            "std": {
                "textures": [("ellipse", PADDLE_HEIGHT * tile_size, PADDLE_HEIGHT * tile_size, 1, 1, 1)],
            },
        },
        PONG_BALL_START_POS,
        0)
    yapyg.entities.set_sprite(state, ENT_PONG_BALL, "std")
    yapyg.collisions.add(state, ENT_PONG_BALL, ["circle", PADDLE_HEIGHT])

    yapyg.collisions.set_handler(state, collision_handler)

    yapyg.controls.add_joystick(state)
    yapyg.movers.controlled.add(state,
        ENT_PONG_PADDLE,
        "joystick",
        0.1,
        [0, PADDLE_Y, float(screen_width) / tile_size - PADDLE_WIDTH, PADDLE_Y])

    yapyg.movers.linear.add(state, ENT_PONG_BALL, [PONG_BALL_MOVE_SPEED, PONG_BALL_MOVE_SPEED], PONG_BALL_ANIM_SPEED)

    return state

def collision_handler(state, collision_list):
    collision_entity = collision_list[0][0] if collision_list[0][0] != ENT_PONG_BALL else collision_list[0][1]
    ball_mover = yapyg.movers.get_active(state, ENT_PONG_BALL)
    if yapyg.movers.get_type(state, ball_mover) == "linear":
        rel_vector = ball_mover["rel_vector"]
        if collision_entity == ENT_PONG_LEFTWALL or collision_entity == ENT_PONG_RIGHTWALL:
            yapyg.movers.linear.add(state, ENT_PONG_BALL, [-rel_vector[0], rel_vector[1]], PONG_BALL_ANIM_SPEED, do_replace=True)
        elif collision_entity == ENT_PONG_TOPWALL:
            yapyg.movers.linear.add(state, ENT_PONG_BALL, [rel_vector[0], -PONG_BALL_MOVE_SPEED], PONG_BALL_ANIM_SPEED, do_replace=True)
        elif collision_entity == ENT_PONG_BOTTOMWALL:
            yapyg.movers.wait.add(state, ENT_PONG_BALL, 1000000, do_replace=True)
            yapyg.movers.jump.add(state, ENT_PONG_BALL, PONG_BALL_START_POS)
            yapyg.movers.linear.add(state, ENT_PONG_BALL, [PONG_BALL_MOVE_SPEED, PONG_BALL_MOVE_SPEED], PONG_BALL_ANIM_SPEED)
        elif collision_entity == ENT_PONG_PADDLE:
            yapyg.movers.linear.add(state, ENT_PONG_BALL, [rel_vector[0], PONG_BALL_MOVE_SPEED], PONG_BALL_ANIM_SPEED, do_replace=True)
