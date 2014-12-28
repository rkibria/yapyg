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
from yapyg import tiles
from yapyg import entities
from yapyg import fixpoint
from yapyg import controls
from yapyg_movers import physical_mover
from yapyg_movers import flipper_mover
from yapyg_helpers import entities_helpers

def create(screen_width_px, screen_height_px, tile_size_px):
        BOTTOM_Y = fixpoint.float2fix(0.0)
        BORDER_THICKNESS = fixpoint.float2fix(2.0)
        BORDER_OFFSET = fixpoint.float2fix(0.1)

        WALLS_COLOR = (0, 0.15, 1)

        joystick_props = controls.get_joystick_properties()
        origin_xy = (0, joystick_props["h"] * screen_height_px)
        state = factory.create(screen_width_px, screen_height_px, tile_size_px, origin_xy)

        controls.add_buttons(state, (("LEFT", on_left_button, "left", "big"),
                                     ("RIGHT", on_right_button, "right", "big")))

        tiles.add_tile_def(state, ".", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [["."] * 10] * 10)

        entities_helpers.create_screen_wall(state, "000_screenbox", BORDER_THICKNESS, BORDER_OFFSET, BOTTOM_Y,
                        top=False, # bottom=False,
                        color=WALLS_COLOR)

        BOUNCE_GRAVITY = fixpoint.float2fix(-9.0)
        BOUNCE_INELASTICITY = fixpoint.float2fix(0.999)
        BOUNCE_FRICTION = fixpoint.float2fix(0.95)
        BOUNCE_STICKYNESS = fixpoint.float2fix(0.0)
        ROT_FRICTION = fixpoint.float2fix(0.35)
        ROT_DECAY = fixpoint.float2fix(0.999)

        ball_entity_name = "900_ball_0"

        BALL_SIZE = fixpoint.float2fix(1.0 / 4.0)
        CIRCLE_RADIUS = fixpoint.div(BALL_SIZE, fixpoint.int2fix(2))
        filename = "assets/img/sprites/quarter_ball.png"
        mass = fixpoint.int2fix(1)

        entities.insert(state,
                ball_entity_name,
                {
                        "*": {
                                "textures": (filename,),
                        },
                },
                (fixpoint.float2fix(1.75), fixpoint.float2fix(4.3), 0,),
                collision=(("circle", CIRCLE_RADIUS, CIRCLE_RADIUS, CIRCLE_RADIUS,),))

        physical_mover.add(state,
                ball_entity_name,
                mass,
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

        ENT_FLIPPER_1 = "000_flipper_1"
        FLIPPER_X = fixpoint.float2fix(1.0)
        FLIPPER_Y = fixpoint.float2fix(1.0)
        FLIPPER_WIDTH = fixpoint.float2fix(1.0)
        FLIPPER_HEIGHT = fixpoint.float2fix(0.25)
        FLIPPER_ROTATION_OFFSET = fixpoint.float2fix(-0.5)
        FLIPPER_COLOR = (1.0, 0.0, 0.0)
        entities.insert(state,
                              ENT_FLIPPER_1,
                              {
                               "*": {
                                     "textures": (("rectangle", FLIPPER_WIDTH, FLIPPER_HEIGHT,
                                                   FLIPPER_COLOR[0], FLIPPER_COLOR[1], FLIPPER_COLOR[2]),),
                                     },
                               },
                              (FLIPPER_X, FLIPPER_Y, fixpoint.float2fix(0.0)),
                              collision=((("rectangle", 0, 0, FLIPPER_WIDTH, FLIPPER_HEIGHT),))
                              )

        flipper_mover.add(state, ENT_FLIPPER_1,
                                 FLIPPER_WIDTH, FLIPPER_HEIGHT,
                                 FLIPPER_ROTATION_OFFSET,
                                 fixpoint.float2fix(360.0)
                                 )

        return state

def on_left_button(state, button_pressed):
        pass

def on_right_button(state, button_pressed):
        pass
