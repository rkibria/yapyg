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
from yapyg import entities
from yapyg import fixpoint
from yapyg import screen
from yapyg_movers import jump_mover
from yapyg_movers import linear_mover
from yapyg_movers import wait_mover
from yapyg_movers import set_property_mover

def star_name(x, y):
        return "000_stars_%d_%d" % (x, y)

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        for x in xrange((screen_width / 256) + 1):
                for y in xrange((screen_height / 256) + 2):
                        entity_name = star_name(x, y)
                        entities.insert(state, entity_name, {
                                        "*": {
                                                "textures": ("assets/img/sprites/stars.png",),
                                                "speed": fixpoint.int2fix(100),
                                        },
                                }, (fixpoint.int2fix(x * 2), fixpoint.int2fix(y * 2), 0)
                                )

        entities.insert(state, "500_ship",
                {
                        "*idle": {
                                "textures": (
                                        "assets/img/sprites/ship_idle/0.png",
                                        "assets/img/sprites/ship_idle/1.png",
                                        ),
                                "speed": fixpoint.int2fix(100),
                        },
                        "thrust": {
                                "textures": (
                                        "assets/img/sprites/ship_thrust/0.png",
                                        "assets/img/sprites/ship_thrust/1.png",
                                        ),
                                "speed" : fixpoint.int2fix(50),
                        },
                }, (fixpoint.int2fix(1), fixpoint.int2fix(1), 0)
                )

        start_stars_movement(state, None)
        start_ship_movement(state, None)

        return state

def start_stars_movement(state, mover_name):
        int_screen_width = fixpoint.fix2int(screen.get_width(state))
        int_screen_height = fixpoint.fix2int(screen.get_height(state))
        for x in xrange((int_screen_width / 256) + 1):
                for y in xrange((int_screen_height / 256) + 2):
                        entity_name = star_name(x, y)
                        jump_mover.add(state, entity_name, (fixpoint.int2fix(x * 2), fixpoint.int2fix(y * 2), 0))
                        linear_mover.add(state, entity_name, (0, fixpoint.int2fix(-2)), fixpoint.float2fix(0.25))
        wait_mover.add(state, entity_name, 0, start_stars_movement)

def start_ship_movement(state, mover_name):
        path = ((0, 0.66), (0.33, 0.33), (0.66, 0), (0.33, -0.33),
                (0, -0.66), (-0.33, -0.33), (-0.66, 0), (-0.33, 0.33))
        for index in xrange(len(path)):
                set_property_mover.add(state, "500_ship", "set_active_sprite", "*idle")
                wait_mover.add(state, "500_ship", fixpoint.float2fix(0.5))
                set_property_mover.add(state, "500_ship", "set_active_sprite", "thrust")
                rel_vector = (fixpoint.float2fix(path[index][0]), fixpoint.float2fix(path[index][1]))
                linear_mover.add(state, "500_ship", rel_vector, fixpoint.float2fix(1.0), ("auto", 0), None if index != len(path) - 1 else start_ship_movement)
