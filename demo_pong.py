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
import yapyg.movers.controlled
import yapyg.controls
import yapyg.collisions

def create(screen_width, screen_height, tile_size):
    state = yapyg.factory.create(screen_width, screen_height, tile_size)

    paddle_width = 1.0 / 2
    paddle_height = 1.0 / 8

    yapyg.entities.insert(state,
        "paddle",
        {
            "std": {
                "textures": [("rectangle", paddle_width * tile_size, paddle_height * tile_size, 1, 1, 1)],
            },
        },
        [1, 1.5],
        0)
    yapyg.entities.set_sprite(state, "paddle", "std")
    yapyg.collisions.add(state, "paddle", ["rectangle", paddle_width, paddle_height], False)

    yapyg.entities.insert(state,
        "top_wall",
        {
            "std": {
                "textures": [("rectangle", screen_width, tile_size, 0, 0, 0)],
            },
        },
        [0, screen_height / float(tile_size)],
        0)
    yapyg.entities.set_sprite(state, "top_wall", "std")
    yapyg.collisions.add(state, "top_wall", ["rectangle", float(screen_width) / tile_size, 1], False)

    yapyg.entities.insert(state,
        "left_wall",
        {
            "std": {
                "textures": [("rectangle", tile_size, screen_height, 0, 0, 0)],
            }
        },
        [-1, 0],
        0)
    yapyg.entities.set_sprite(state, "left_wall", "std")
    yapyg.collisions.add(state, "left_wall", ["rectangle", 1, float(screen_height) / tile_size], False)

    yapyg.entities.insert(state,
        "right_wall",
        {
            "std": {
                "textures": [("rectangle", tile_size, screen_height, 0, 0, 0)],
            }
        },
        [float(screen_width) / tile_size, 0],
        0)
    yapyg.entities.set_sprite(state, "right_wall", "std")
    yapyg.collisions.add(state, "right_wall", ["rectangle", 1, float(screen_height) / tile_size], False)

    yapyg.entities.insert(state,
        "ball",
        {
            "std": {
                "textures": [("ellipse", paddle_height * tile_size, paddle_height * tile_size, 1, 1, 1)],
            },
        },
        [1, 3],
        0)
    yapyg.entities.set_sprite(state, "ball", "std")
    yapyg.collisions.add(state, "ball", ["circle", paddle_height])

    yapyg.collisions.set_handler(state, collision_handler)

    yapyg.controls.add_joystick(state)
    yapyg.movers.controlled.add(state,
        "paddle",
        "joystick",
        0.1,
        [0, 1.5, float(screen_width) / tile_size - paddle_width, 1.5])

    yapyg.movers.linear.add(state, "ball", [100, 100], 2.0 / 1000000)

    return state

def collision_handler(state, collision_list):
    print str(collision_list)
    exit()
