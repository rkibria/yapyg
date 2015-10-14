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

import random

from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import collisions
from yapyg import debug

from yapyg_widgets.screen_widget import ScreenWidget
from yapyg_movers import physical_mover
from yapyg_helpers import entities_helpers

from physics_params import *

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        BOTTOM_Y = 0.5
        BORDER_THICKNESS = 2.0
        BORDER_OFFSET = 0.1
        WALLS_COLOR = (0.3, 0.45, 1)
        tiles.add_tile_def(state, " ", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [[" " for x in xrange(10)] for x in xrange(10)])
        entities_helpers.create_screen_wall(state, "000_screenbox", BORDER_THICKNESS, BORDER_OFFSET, BOTTOM_Y, color=WALLS_COLOR)

        # collisions.set_handler(state, collision_handler)

        for i in xrange(4):
                objtype = random.randint(0, 2)
                ent_name = "%d" % i
                ent_mass = 1.0
                angle = random.randint(0, 20) - 10.0

                if objtype == 0:
                        ent_name = "square_" + ent_name
                        if i % 2 == 0:
                                tx = "assets/img/sprites/half_square.png"
                        else:
                                tx = "assets/img/sprites/half_square_2.png"

                        entities.insert(state,
                                        ent_name,
                                        {
                                         "*": {
                                               "textures": (tx,),
                                               },
                                         },
                                        (0.5 + i * 0.75, 5, angle,),
                                        collision=(("rectangle", 0, 0, 0.5, 0.5),)
                                        )
                elif objtype == 1:
                        ent_name = "circle_" + ent_name
                        if i % 2 == 0:
                                tx = "assets/img/sprites/half_ball.png"
                        else:
                                tx = "assets/img/sprites/half_ball_2.png"

                        entities.insert(state,
                                ent_name,
                                {
                                        "*": {
                                                "textures": (tx,),
                                        },
                                },
                                (0.5 + i * 0.75, 4.0, angle),
                                collision=(("circle", 0.25, 0.25, 0.25),))

                elif objtype == 2:
                        ent_mass = 2.0
                        ent_name = "rect_" + ent_name
                        if i % 2 == 0:
                                tx = "assets/img/sprites/one_by_half_rectangle.png"
                        else:
                                tx = "assets/img/sprites/one_by_half_rectangle_2.png"

                        entities.insert(state,
                                        ent_name,
                                        {
                                         "*": {
                                               "textures": (tx,),
                                               },
                                         },
                                        (0.5 + i * 0.75, 3.0, 90 + angle,),
                                        collision=(("rectangle", 0, 0, 1.0, 0.5),)
                                        )

                physical_mover.add (state,
                                    ent_name,
                                    ent_mass,
                                    0,
                                    0,
                                    0.0,
                                    YAPYG_STD_GRAVITY,
                                    YAPYG_STD_FRICTION,
                                    YAPYG_STD_INELASTICITY,
                                    0,
                                    YAPYG_STD_ROT_FRICTION,
                                    YAPYG_STD_ROT_DECAY,
                                    YAPYG_STD_STICKYNESS,
                                    )

        return state

def collision_handler(state, collisions_list):
        for entity_name_1, entity_name_2 in collisions_list:
                debug.set_line(state, 0, "collision: %s <-> %s" % (entity_name_1, entity_name_2,))
