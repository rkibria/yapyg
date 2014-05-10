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
import yapyg.movers.entitycmd
import yapyg.movers.wait

def create(screen_width, screen_height, tile_size):
    state = yapyg.factory.create(screen_width, screen_height, tile_size)

    for x in xrange(int(screen_width / 256) + 1):
        for y in xrange(int(screen_height / 256) + 2):
            yapyg.sprites.insert(state, "000_stars_%d_%d" % (x, y), ["assets/img/sprites/stars.png"], pos=[x * 2, y * 2])

    yapyg.entities.insert(state, "500_ship",
        {
            "idle": {
                "textures": [("assets/img/sprites/ship_idle/%d.png" % i) for i in [0, 1]],
                "speed": 100000,
            },
            "thrust": {
                "textures": [("assets/img/sprites/ship_thrust/%d.png" % i) for i in [0, 1]],
                "speed" : 50000,
            },
        }, [1, 1], 0)

    start_stars_movement(state, None)
    start_ship_movement(state, None)

    return state

def start_stars_movement(state, mover_name):
    for x in xrange(int(yapyg.screen.get_width(state) / 256) + 1):
        for y in xrange(int(yapyg.screen.get_height(state) / 256) + 2):
            sprite_name = "000_stars_%d_%d" % (x, y)
            yapyg.movers.jump.add(state, sprite_name + "_mover", yapyg.sprites.get_pos(state, sprite_name), [x * 2, y * 2])
            yapyg.movers.linear.add(state, sprite_name + "_mover",
                yapyg.sprites.get_pos(state, sprite_name),
                yapyg.sprites.get_rot(state, sprite_name),
                [0, -2], 0.25 / 1000000)
    yapyg.movers.wait.add(state, sprite_name + "_mover", 0, start_stars_movement)

def start_ship_movement(state, mover_name):
    small_step = 0.33
    big_step = 2 * small_step
    path = [[0, big_step], [small_step, small_step], [big_step, 0], [small_step, -small_step],
        [0, -big_step], [-small_step, -small_step], [-big_step, 0], [-small_step, small_step]]
    for index in xrange(len(path)):
        yapyg.movers.entitycmd.add(state, "ship_mover", "500_ship", "set_sprite", "idle")
        yapyg.movers.wait.add(state, "ship_mover", 500000)
        yapyg.movers.entitycmd.add(state, "ship_mover", "500_ship", "set_sprite", "thrust")
        yapyg.movers.linear.add(state, "ship_mover",
            yapyg.entities.get_pos(state, "500_ship"),
            yapyg.entities.get_rot(state, "500_ship"),
            path[index], 1.0 / 1000000,
            True, None if index != len(path) - 1 else start_ship_movement)
