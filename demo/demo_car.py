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
from yapyg import sprites
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
from yapyg_movers import control_phys_mover
from yapyg_viewers import relative_viewer
from yapyg_helpers import tiles_helpers

from physics_params import *

FONT_NAME = "DroidSansMonoDotted16x32"

ENT_PLAYER_CAR = "player_car"
ENT_PLAYER_CAR_EXHAUST = "player_car_exhaust"

def create(screen_width_px, screen_height_px, tile_size_px):
        joystick_props = controls.get_joystick_properties()
        origin_xy = (0, joystick_props["h"] * screen_height_px)

        state = factory.create(screen_width_px, screen_height_px, tile_size_px, origin_xy)

        user.set_data(state, "n_barrels", 0)
        user.set_data(state, "n_barriers", 0)

        controls.add_joystick(state)
        controls.add_buttons(state, (("Fire", on_fire_button, "right", "big"),))

        floor_tile = "assets/img/tiles/dirt_ground.png"
        tiles.add_tile_def(state, ' ', (floor_tile,))
        tiles_helpers.load_walls(state, "", floor_tile, "assets/img/tiles/bricks_walls.png")
        tiles_helpers.load_walls(state, "/", "assets/img/tiles/grass.png", "assets/img/tiles/bricks_walls.png")
        tiles.add_tile_def(state, '|', (floor_tile, "assets/img/tiles/road-I.png",))
        tiles.add_tile_def(state, '~', (floor_tile, "assets/img/tiles/road-h.png",))
        tiles.add_tile_def(state, 'L', (floor_tile, "assets/img/tiles/road-cnr-bl.png",))
        tiles.add_tile_def(state, 'T', (floor_tile, "assets/img/tiles/road-cnr-tl.png",))
        tiles.add_tile_def(state, 'J', (floor_tile, "assets/img/tiles/road-cnr-br.png",))
        tiles.add_tile_def(state, 'j', (floor_tile, "assets/img/tiles/road-cnr-ur.png",))
        tiles.add_tile_def(state, '/', ("assets/img/tiles/grass.png",))
        tiles.add_tile_def(state, 't', ("assets/img/tiles/grass.png", "assets/img/tiles/tree.png"))
        tiles.set_area(state,
                 [
                  ['t', '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/'],
                  ['/', '/.', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/,', '/'],
                  ['t', '/)', '<' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '>' , '/(', 't'],
                  ['/', '/)', '(' , 'T' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , 'j' , ')' , '/(', '/'],
                  ['t', '/)', '(' , '|' , '.' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , ',' , '|' , ')' , '/(', 't'],
                  ['/', '/)', '(' , '|' , ')' , '/<', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/>', '(' , '|' , ')' , '/(', '/'],
                  ['t', '/)', '(' , '|' , ')' , '/(', '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/)', '(' , '|' , ')' , '/(', 't'],
                  ['/', '/)', '(' , '|' , ')' , '/(', 't' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/)', '(' , '|' , ')' , '/(', '/'],
                  ['t', '/)', '(' , '|' , ')' , '/(', '/' , '/' , '/' , '/' , '/' , '/' , '/' , 't' , '/)', '(' , '|' , ')' , '/(', 't'],
                  ['/', '/)', '(' , '|' , ')' , '/(', 't' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/)', '(' , '|' , ')' , '/(', '/'],
                  ['t', '/)', '(' , '|' , ')' , '/(', '/' , '/' , '/' , '/' , '/' , '/' , '/' , 't' , '/)', '(' , '|' , ')' , '/(', 't'],
                  ['/', '/)', '(' , '|' , ')' , '/(', 't' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/)', '(' , '|' , ')' , '/(', '/'],
                  ['t', '/)', '(' , '|' , ')' , '/(', '/' , '/' , '/' , '/' , '/' , '/' , '/' , 't' , '/)', '(' , '|' , ')' , '/(', 't'],
                  ['/', '/)', '(' , '|' , ')' , '/(', 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , '/)', '(' , '|' , ')' , '/(', '/'],
                  ['t', '/)', '(' , '|' , ')' , '/[', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/_', '/]', '(' , '|' , ')' , '/(', 't'],
                  ['/', '/)', '(' , '|' , ':' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , '-' , ';' , '|' , ')' , '/(', '/'],
                  ['t', '/)', '(' , 'L' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , '~' , 'J' , ')' , '/(', 't'],
                  ['/', '/)', '[' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , '_' , ']' , '/(', '/'],
                  ['t', '/:', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/-', '/;', '/'],
                  ['/', 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't' , '/' , 't'],
                  ['/', '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/' , '/'],
                 ]
                 )
        play_area_origin = (2.0, 3.0)

        # text.load_font(state, FONT_NAME, "assets/img/fonts/%s.png" % FONT_NAME, 16, 32)

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
                        (play_area_origin[0] + 1.5, play_area_origin[1] + 6.0, 0),
                        (-0.125, -0.25),
                        collision=(("rectangle", 0.0, 0.0, 0.25, 0.5),),
                        )

        view.set_viewer(state, relative_viewer.create(state, ENT_PLAYER_CAR))

        control_phys_mover.add(state,
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
                           dir_factor=0.005,
                           pos_accel=12.0,
                           neg_accel=4.0,
                           rest_sprite="*",
                           pos_sprite="+",
                           neg_sprite="-"
                           )

        for i in xrange(7):
                add_barrel(state, play_area_origin[0] + 0.5, play_area_origin[1] + 2.0 + 2.0 * i)

        for i in xrange(7):
                add_barrel(state, play_area_origin[0] + 15.25, play_area_origin[1] + 2.0 + 2.0 * i)

        for i in xrange(8):
                add_barrier(state, play_area_origin[0] + 0.5 - 0.125, play_area_origin[1] + 1.0 + 2.0 * i, 90.0)

        for i in xrange(8):
                add_barrier(state, play_area_origin[0] + 1.0 + 0.125 + 2.0 * i, play_area_origin[1] + 0.5, 0.0)

        for i in xrange(7):
                add_barrier(state, play_area_origin[0] + 1.0 + 0.125 + 2.0 * i, play_area_origin[1] + 15.25, 0.0)

        for i in xrange(7):
                add_barrel(state, play_area_origin[0] + 2.0 + 0.125 + 2.0 * i, play_area_origin[1] + 15.25)

        for i in xrange(6):
                add_barrel(state, play_area_origin[0] + 2.0 + 0.25 + 2.0 * i, play_area_origin[1] + 13.5)

        for i in xrange(6):
                add_barrier(state, play_area_origin[0] + 3.0 + 0.25 + 2.0 * i, play_area_origin[1] + 13.5, 0.0)

        for i in xrange(7):
                add_barrel(state, play_area_origin[0] + 2.0 + 0.125 + 2.0 * i, play_area_origin[1] + 0.5)

        for i in xrange(8):
                add_barrier(state, play_area_origin[0] + 15.25 - 0.125, play_area_origin[1] + 1.0 + 2.0 * i, 90.0)

        for i in xrange(1, 6):
                add_barrel(state, play_area_origin[0] + 2.25, play_area_origin[1] + 2.0 + 2.0 * i)
                add_barrel(state, play_area_origin[0] + 13.5, play_area_origin[1] + 2.0 + 2.0 * i)

        for i in xrange(6):
                add_barrier(state, play_area_origin[0] + 2.25 - 0.125, play_area_origin[1] + 3.0 + 2.0 * i, 90.0)
                add_barrier(state, play_area_origin[0] + 13.5 - 0.125, play_area_origin[1] + 3.0 + 2.0 * i, 90.0)

        for i in xrange(6):
                add_barrel(state, play_area_origin[0] + 2.25 + 2.0 * i, play_area_origin[1] + 2.25)
                add_barrier(state, play_area_origin[0] + 3.25 - 0.125 + 2.0 * i, play_area_origin[1] + 2.25, 0.0)

        timer.create(state, on_timer, 100)

        return state

def on_timer(state, last_frame_delta):
        phys_mover = movers.get_active(state, ENT_PLAYER_CAR)
        if phys_mover:
                exhaust_sprite_name = entities.get_active_sprite_name(state, ENT_PLAYER_CAR_EXHAUST)
                if not sprites.is_enabled(state, exhaust_sprite_name):
                        do_exhaust(state, math_2d.get_radial_offset(entities.get_pos(state, ENT_PLAYER_CAR), -0.25))

def on_fire_button(state, button_pressed):
        pass

def add_barrel(state, x, y):
        barrel_count = user.get_data(state, "n_barrels")
        barrel_entity_name = "barrel_%d" % barrel_count
        user.set_data(state, "n_barrels", barrel_count + 1)

        entities.insert(state,
                barrel_entity_name,
                {
                        "*": {
                                "textures": ("assets/img/sprites/barrel.png",),
                        },
                },
                (
                        x,
                        y,
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

def add_barrier(state, x, y, r):
        barrier_count = user.get_data(state, "n_barriers")
        barrier_entity_name = "barrier_%d" % barrier_count
        user.set_data(state, "n_barriers", barrier_count + 1)

        entities.insert(state,
                barrier_entity_name,
                {
                        "*": {
                                "textures": ("assets/img/sprites/barrier.png",),
                        },
                },
                (
                        x,
                        y,
                        r,
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

def do_exhaust(state, pos):
        entities.insert(state,
                        ENT_PLAYER_CAR_EXHAUST,
                        {
                          "*": {
                                "textures": ("assets/img/sprites/exhaust/0.png",
                                             "assets/img/sprites/exhaust/1.png",
                                             "assets/img/sprites/exhaust/2.png",
                                             "assets/img/sprites/exhaust/1.png",
                                             ),
                                "speed": 50.0,
                                },
                          },
                        pos,
                        (-0.125, -0.125),
                        play_once=True,
                        )
