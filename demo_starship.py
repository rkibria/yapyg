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
import yapyg.movers.jump
import yapyg.movers.linear
import yapyg.movers.wait
import yapyg.movers.set_property

def star_name(x, y):
        return "000_stars_%d_%d" % (x, y)

def create(screen_width, screen_height, tile_size):
        state = yapyg.factory.create(screen_width, screen_height, tile_size)

        for x in xrange(int(screen_width / 256) + 1):
                for y in xrange(int(screen_height / 256) + 2):
                        entity_name = star_name(x, y)
                        yapyg.entities.insert(state, entity_name, {
                                        "*": {
                                                "textures": ["assets/img/sprites/stars.png"],
                                                "speed": 100,
                                        },
                                }, [x * 2, y * 2], 0)

        yapyg.entities.insert(state, "500_ship",
                {
                        "*idle": {
                                "textures": [("assets/img/sprites/ship_idle/%d.png" % i) for i in [0, 1]],
                                "speed": 100,
                        },
                        "thrust": {
                                "textures": [("assets/img/sprites/ship_thrust/%d.png" % i) for i in [0, 1]],
                                "speed" : 50,
                        },
                }, [1, 1], 0)

        start_stars_movement(state, None)
        start_ship_movement(state, None)

        return state

def callback(state, mover_name):
        print "END"

def start_stars_movement(state, mover_name):
        int_screen_width = yapyg.fixpoint.fix2int(yapyg.screen.get_width(state))
        int_screen_height = yapyg.fixpoint.fix2int(yapyg.screen.get_height(state))
        for x in xrange((int_screen_width / 256) + 1):
                for y in xrange((int_screen_height / 256) + 2):
                        entity_name = star_name(x, y)
                        yapyg.movers.jump.add(state, entity_name, [x * 2, y * 2])
                        yapyg.movers.linear.add(state, entity_name, [0, -2], 0.25)
        yapyg.movers.wait.add(state, entity_name, 0, start_stars_movement)

def start_ship_movement(state, mover_name):
        path = [[0, 0.66], [0.33, 0.33], [0.66, 0], [0.33, -0.33],
                [0, -0.66], [-0.33, -0.33], [-0.66, 0], [-0.33, 0.33]]
        for index in xrange(len(path)):
                yapyg.movers.set_property.add(state, "500_ship", "set_active_sprite", "*idle")
                yapyg.movers.wait.add(state, "500_ship", 0.5)
                yapyg.movers.set_property.add(state, "500_ship", "set_active_sprite", "thrust")
                yapyg.movers.linear.add(state, "500_ship", path[index], 1.0,
                        True, None if index != len(path) - 1 else start_ship_movement)
