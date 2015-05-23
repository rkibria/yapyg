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

from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import collisions
from yapyg import debug
from yapyg_widgets.screen_widget import ScreenWidget
from yapyg_movers import physical_mover
from yapyg_helpers import entities_helpers

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        BOTTOM_Y = 0.5
        BORDER_THICKNESS = 2.0
        BORDER_OFFSET = 0.1
        WALLS_COLOR = (0.3, 0.45, 1)
        tiles.add_tile_def(state, " ", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [[" " for x in xrange(10)] for x in xrange(10)])
        entities_helpers.create_screen_wall(state, "000_screenbox", BORDER_THICKNESS, BORDER_OFFSET, BOTTOM_Y, color=WALLS_COLOR)

        collisions.set_handler(state, collision_handler)

        speed_factor = 4

        # True # False
        show_collision = True
        target_is_physical = True
        both_moving = True
        shifted = True
        more_rectangles = True
        circle_collision = True
        more_circles = True

        if show_collision:
                # 2 rectangles collide
                BOUNCE_GRAVITY = 0.0
                BOUNCE_INELASTICITY = 1.0
                BOUNCE_FRICTION = 1.0
                BOUNCE_STICKYNESS = 0.0
                ROT_FRICTION = 0.35
                ROT_DECAY = 1.0
                VX_1 = 0.0
                VY_1 = -1.0
                R_1 = 0.0
                VX_2 = 0.0
                VY_2 = 0.0
                R_2 = 0.0
                if both_moving:
                        VY_2 = 1.0
        else:
                # Single rectangle collides with walls
                BOUNCE_GRAVITY = 0.0
                BOUNCE_INELASTICITY = 0.9
                BOUNCE_FRICTION = 1.0
                BOUNCE_STICKYNESS = 0.0
                ROT_FRICTION = 0.35
                ROT_DECAY = 1.0
                VX_1 = 0.5
                VY_1 = -1.0
                R_1 = 40.0
                VX_2 = 0.0
                VY_2 = 0.0

        VX_1 *= speed_factor
        VY_1 *= speed_factor

        VX_2 *= speed_factor
        VY_2 *= speed_factor

        X_1 = 1.75
        if shifted:
                X_1 += 0.33
                VX_1 -= speed_factor

        entities.insert(state,
                        "sq_1",
                        {
                         "*": {
                               "textures": ("assets/img/sprites/half_square.png",),
                               },
                         },
                        (X_1, 5, R_1,),
                        collision=(("rectangle", 0, 0, 0.5, 0.5),)
                        )

        physical_mover.add(state,
                "sq_1",
                1.0,
                VX_1,
                VY_1,
                0.0,
                BOUNCE_GRAVITY,
                BOUNCE_FRICTION,
                BOUNCE_INELASTICITY,
                0,
                ROT_FRICTION,
                ROT_DECAY,
                BOUNCE_STICKYNESS,
                )

        if circle_collision:
                entities.insert(state,
                        "circ_1",
                        {
                                "*": {
                                        "textures": ("assets/img/sprites/half_ball.png",),
                                },
                        },
                        (1.0, 2.55, 0.0),
                        collision=(("circle", 0.25, 0.25, 0.25),))

                if target_is_physical:
                        physical_mover.add(state,
                                "circ_1",
                                1.0,
                                0,
                                0,
                                0,
                                BOUNCE_GRAVITY,
                                BOUNCE_FRICTION,
                                BOUNCE_INELASTICITY,
                                0,
                                ROT_FRICTION,
                                ROT_DECAY,
                                BOUNCE_STICKYNESS,
                                )

                if more_circles:
                        entities.insert(state,
                                "circ_2",
                                {
                                        "*": {
                                                "textures": ("assets/img/sprites/half_ball.png",),
                                        },
                                },
                                (1.0, 1.25, 0.0),
                                collision=(("circle", 0.25, 0.25, 0.25),))

                        if target_is_physical:
                                physical_mover.add(state,
                                        "circ_2",
                                        1.0,
                                        0,
                                        0,
                                        0,
                                        BOUNCE_GRAVITY,
                                        BOUNCE_FRICTION,
                                        BOUNCE_INELASTICITY,
                                        0,
                                        ROT_FRICTION,
                                        ROT_DECAY,
                                        BOUNCE_STICKYNESS,
                                        )

                        entities.insert(state,
                                "circ_3",
                                {
                                        "*": {
                                                "textures": ("assets/img/sprites/half_ball.png",),
                                        },
                                },
                                (1.0, 3.75, 0.0),
                                collision=(("circle", 0.25, 0.25, 0.25),))

                        if target_is_physical:
                                physical_mover.add(state,
                                        "circ_3",
                                        1.0,
                                        0,
                                        0,
                                        0,
                                        BOUNCE_GRAVITY,
                                        BOUNCE_FRICTION,
                                        BOUNCE_INELASTICITY,
                                        0,
                                        ROT_FRICTION,
                                        ROT_DECAY,
                                        BOUNCE_STICKYNESS,
                                        )

        if show_collision:
                entities.insert(state,
                                "sq_2",
                                {
                                 "*": {
                                       "textures": ("assets/img/sprites/half_square_2.png",),
                                       },
                                 },
                                (1.75, 4, R_2,),
                                collision=(("rectangle", 0, 0, 0.5, 0.5),)
                                )

                if target_is_physical:
                        physical_mover.add(state,
                                "sq_2",
                                1.0,
                                VX_2,
                                VY_2,
                                0,
                                BOUNCE_GRAVITY,
                                BOUNCE_FRICTION,
                                BOUNCE_INELASTICITY,
                                0,
                                ROT_FRICTION,
                                ROT_DECAY,
                                BOUNCE_STICKYNESS,
                                )

                if more_rectangles:
                        entities.insert(state,
                                        "sq_3",
                                        {
                                         "*": {
                                               "textures": ("assets/img/sprites/one_by_half_rectangle.png",),
                                               },
                                         },
                                        (1.0, 2.0, 0,),
                                        collision=(("rectangle", 0, 0, 1.0, 0.5),)
                                        )

                        physical_mover.add(state,
                                "sq_3",
                                2.0,
                                0,
                                0,
                                0,
                                BOUNCE_GRAVITY,
                                BOUNCE_FRICTION,
                                BOUNCE_INELASTICITY,
                                0,
                                ROT_FRICTION,
                                ROT_DECAY,
                                BOUNCE_STICKYNESS,
                                )

                        entities.insert(state,
                                        "sq_4",
                                        {
                                         "*": {
                                               "textures": ("assets/img/sprites/one_by_half_rectangle_2.png",),
                                               },
                                         },
                                        (2.0, 2.5, 90.0,),
                                        collision=(("rectangle", 0, 0, 1.0, 0.5),)
                                        )

                        physical_mover.add(state,
                                "sq_4",
                                2.0,
                                0,
                                0,
                                0,
                                BOUNCE_GRAVITY,
                                BOUNCE_FRICTION,
                                BOUNCE_INELASTICITY,
                                0,
                                ROT_FRICTION,
                                ROT_DECAY,
                                BOUNCE_STICKYNESS,
                                )

        return state

def collision_handler(state, collisions_list):
        for entity_name_1, entity_name_2 in collisions_list:
                debug.set_line(state, 0, "collision: %s <-> %s" % (entity_name_1, entity_name_2,))
