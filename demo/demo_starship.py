# Copyright (c) 2015 Raihan Kibria
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

DEBUG_MODE = False

from yapyg import factory
from yapyg import entities
from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import controls
from yapyg import text
from yapyg import view
from yapyg import collisions
from yapyg import user
from yapyg import screen
from yapyg_movers import jump_mover
from yapyg_movers import linear_mover
from yapyg_movers import wait_mover
from yapyg_movers import set_property_mover
from yapyg_movers import controlled_mover

ENT_SHIP = "500_ship"

def star_name(x, y):
        return "000_stars_%d_%d" % (x, y)

def create(screen_width_px, screen_height_px, tile_size_px):
        joystick_props = controls.get_joystick_properties()
        origin_xy = (0, joystick_props["h"] * screen_height_px)
        state = factory.create(screen_width_px, screen_height_px, tile_size_px, origin_xy)
        controls.add_joystick(state)
        controls.add_buttons(state, (("Fire", None, "right", "big"),))

        n_x = (screen_width_px / 256) + 1
        n_y = (screen_height_px / 256) + 2
        for x in xrange(n_x):
                for y in xrange(n_y):
                        entity_name = star_name(x, y)
                        textures_tuple = ("assets/img/sprites/stars.png",)
                        if DEBUG_MODE:
                                color = (float(x) / n_x, float(y) / n_y, 0)
                                textures_tuple = (("rectangle", 2, 2, color[0], color[1], color[2]),)
                        entities.insert(state, entity_name, {
                                        "*": {
                                                "textures": textures_tuple,
                                                "speed": 0,
                                        },
                                }, ((x * 2), (y * 2), 0)
                                )

        entities.insert(state, ENT_SHIP,
                {
                        "*idle": {
                                "textures": (
                                        "assets/img/sprites/ship_idle/0.png",
                                        "assets/img/sprites/ship_idle/1.png",
                                        ),
                                "speed": 100,
                        },
                        "thrust": {
                                "textures": (
                                        "assets/img/sprites/ship_thrust/0.png",
                                        "assets/img/sprites/ship_thrust/1.png",
                                        ),
                                "speed" : 50,
                        },
                }, (1, 1, 0)
                )

        start_stars_movement(state, None)

        controlled_mover.add(state,
                             ENT_SHIP,
                             "joystick",
                             0.03,
                             (0, 0, 3.25, 1.0),
                             ("*idle", "thrust"),
                             False
                             )

        return state

def start_stars_movement(state, mover_name):
        int_screen_width = int(screen.get_width(state))
        int_screen_height = int(screen.get_height(state))
        for x in xrange((int_screen_width / 256) + 1):
                for y in xrange((int_screen_height / 256) + 2):
                        entity_name = star_name(x, y)
                        jump_mover.add(state, entity_name, ((x * 2), (y * 2), 0))
                        linear_mover.add(state, entity_name, (0, -2), 0.25)
        wait_mover.add(state, entity_name, 0, start_stars_movement)
