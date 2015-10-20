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
from yapyg import controls
from yapyg import text
from yapyg import view
from yapyg import collisions
from yapyg import user
from yapyg import movers
from yapyg import timer
from yapyg import math_2d
from yapyg_movers import controlled_mover
from yapyg_movers import linear_mover
from yapyg_movers import destroy_mover
from yapyg_movers import wait_mover
from yapyg_movers import physical_mover
from yapyg_viewers import relative_viewer
from yapyg_helpers import tiles_helpers

from physics_params import *

FONT_NAME = "DroidSansMonoDotted16x32"

ENT_PLAYER_CAR = "player_car"

def create(screen_width_px, screen_height_px, tile_size_px):
        joystick_props = controls.get_joystick_properties()
        origin_xy = (0, joystick_props["h"] * screen_height_px)

        state = factory.create(screen_width_px, screen_height_px, tile_size_px, origin_xy)

        controls.add_joystick(state)
        controls.add_buttons(state, (("Fire", on_fire_button, "right", "big"),))

        floor_tile = "assets/img/tiles/dirt_ground.png"
        tiles.add_tile_def(state, ' ', (floor_tile,))
        tiles_helpers.load_walls(state, "", floor_tile, "assets/img/tiles/bricks_walls.png")
        tiles.set_area(state,
                [ ['<', '-', '-', '-', '-', '-', '-', '-', '-', '>'],
                  ['(', ' ', ' ', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ' ', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ' ', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', '<', '>', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', '[', ']', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ' ', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ' ', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', '<', '>', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', '[', ']', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ')', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ')', ' ', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', '<', '>', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', '[', ']', ' ', ')', ' ', ' ', ' ', ')'],
                  ['(', ' ', ' ', ' ', ' ', ':', ' ', ' ', ' ', ')'],
                  ['(', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ')'],
                  ['[', '_', '_', '_', '_', '_', '_', '_', '_', ']']]
                  )

        text.load_font(state, FONT_NAME, "assets/img/fonts/%s.png" % FONT_NAME, 16, 32)

        entities.insert(state,
                        ENT_PLAYER_CAR,
                        {
                         "*": {
                                   "textures": (
                                                "assets/img/sprites/car/0.png",
                                                ),
                                   "speed": 0.0,
                                   },
                         "+": {
                                   "textures": (
                                                "assets/img/sprites/car/1.png",
                                                ),
                                   "speed": 0.0,
                                   },
                         "-": {
                                   "textures": (
                                                "assets/img/sprites/car/2.png",
                                                ),
                                   "speed": 0.0,
                                   },
                         },
                        (1.0, 1.0, 0),
                        (0, 0),
                        collision=(("rectangle", 0.0, 0.0, 0.25, 0.5),),
                        )

        view.set_viewer(state,
                        relative_viewer.create(state,
                                               ENT_PLAYER_CAR,
                                               [-2.0, -2.25]))

        physical_mover.add(state,
                           ENT_PLAYER_CAR,
                           1.0,
                           0,
                           0,
                           0,
                           0,
                           0.9, # IDX_MOVERS_PHYSICAL_FRICTION
                           0.001, # YAPYG_STD_INELASTICITY,
                           0,
                           YAPYG_STD_ROT_FRICTION,
                           YAPYG_STD_ROT_DECAY,
                           YAPYG_STD_STICKYNESS,
                           )

        for i in xrange(3):
                barrel_entity_name = "barrel_%d" % i
                entities.insert(state,
                        barrel_entity_name,
                        {
                                "*": {
                                        "textures": ("assets/img/sprites/barrel.png",),
                                },
                        },
                        (
                                0.5 + i * 0.5,
                                5.5,
                                0,
                        ),
                        collision=(("circle", (1.0 / 4.0) / 2.0, (1.0 / 4.0) / 2.0, (1.0 / 4.0) / 2.0,),))
                physical_mover.add(state,
                        barrel_entity_name,
                        0.01,
                        0,
                        0,
                        0,
                        0,
                        0.92,
                        YAPYG_STD_INELASTICITY,
                        0,
                        YAPYG_STD_ROT_FRICTION,
                        YAPYG_STD_ROT_DECAY,
                        YAPYG_STD_STICKYNESS,
                        )

        for i in xrange(2):
                barrier_entity_name = "barrier_%d" % i
                entities.insert(state,
                        barrier_entity_name,
                        {
                                "*": {
                                        "textures": ("assets/img/sprites/barrier.png",),
                                },
                        },
                        (
                                0.4 + i * 0.6,
                                3.5,
                                0,
                        ),
                        collision=(("rectangle", 0.0, 0.0, 0.5, 0.125),))
                physical_mover.add(state,
                        barrier_entity_name,
                        0.5,
                        0,
                        0,
                        0,
                        0,
                        0.92,
                        YAPYG_STD_INELASTICITY,
                        0,
                        YAPYG_STD_ROT_FRICTION,
                        YAPYG_STD_ROT_DECAY,
                        YAPYG_STD_STICKYNESS,
                        )

        timer.create(state, on_timer, 100)

        return state

def on_timer(state, last_frame_delta):
        phys_mover = movers.get_active(state, ENT_PLAYER_CAR)
        if phys_mover:
                direction = controls.get_joystick(state)
                joy_dir = direction[0]
                joy_accel = direction[1]
                player_pos = entities.get_pos(state, ENT_PLAYER_CAR)
                player_speed = (phys_mover[physical_mover.IDX_MOVERS_PHYSICAL_VX], phys_mover[physical_mover.IDX_MOVERS_PHYSICAL_VY])
                player_rot = player_pos[2]
                if joy_accel > 0.0:
                        accel_factor = 10.0
                else:
                        accel_factor = 4.0
                dir_factor = 0.01 * math_2d.length(player_speed)
                accel_vector = math_2d.vector_mul(math_2d.rotated_point((0, 0), (0.0, 1.0), player_rot), accel_factor * joy_accel)
                phys_mover[physical_mover.IDX_MOVERS_PHYSICAL_AX] = accel_vector[0]
                phys_mover[physical_mover.IDX_MOVERS_PHYSICAL_AY] = accel_vector[1]
                phys_mover[physical_mover.IDX_MOVERS_PHYSICAL_VR] += (-joy_dir) * dir_factor * (-1 if joy_accel < 0 else 1)

                if joy_accel > 0.0:
                        entities.set_active_sprite(state, ENT_PLAYER_CAR, "+")
                elif joy_accel == 0.0:
                        entities.set_active_sprite(state, ENT_PLAYER_CAR, "*")
                else:
                        entities.set_active_sprite(state, ENT_PLAYER_CAR, "-")

def on_fire_button(state, button_pressed):
        pass
