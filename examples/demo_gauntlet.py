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
from yapyg import fixpoint_trig
from yapyg import controls
from yapyg import text
from yapyg import view
from yapyg import collisions
from yapyg import debug
from yapyg_movers import controlled_mover
from yapyg_movers import linear_mover
from yapyg_movers import destroy_mover
from yapyg_viewers import relative_viewer
from yapyg_helpers import tiles_helpers

ENT_MAN = "500_man"
ENT_SHOT = "600_throwingstar"

# Called from the menu widget, this function creates and
# sets up the game state object. Parameters are the usable
# screen size and tile size in pixels.
def create(screen_width_px, screen_height_px, tile_size_px):
        # If there is an on-screen joystick
        # (there may not be one needed for non-mobile or other platforms)
        # set the drawing origin to above it (WORK IN PROGRESS, this needs a
        # cleaner solution).
        joystick_props = controls.get_joystick_properties()
        origin_xy = (0, joystick_props["h"] * screen_height_px)

        # Create the actual game state object that stores all information that yapyg needs.
        state = factory.create(screen_width_px, screen_height_px, tile_size_px, origin_xy)

        # Enable the joystick.
        controls.add_joystick(state)

        # Request buttons
        controls.add_buttons(state, (("Fire", on_fire_button, "right", "big"),))

        # Create some tiles to use for our game area. Individual tiles are referred to by strings.
        # Each tile can be composed by layering several images over each other
        floor_tile = "assets/img/tiles/dirtysquares.png"
        tiles.add_tile_def(state, "x", (floor_tile,))

        # Special wall tile import helper.
        tiles_helpers.load_walls(state, "", floor_tile, "assets/img/tiles/bricks_walls.png")

        # The tile map is made as a list of lists.
        tiles.set_area(state,
                [ ['<', '-', '-', '>', '<', '-', '-', '-', '-', '>'],
                  ['(', '.', ',', ')', '(', '.', '_', '_', ',', ')'],
                  ['(', ')', '(', ')', '(', ')', '<', '>', '(', ')'],
                  ['[', ']', '(', ')', '(', ')', '(', ')', '[', ']'],
                  ['<', '-', ';', ')', '(', ')', '(', ':', '-', '>'],
                  ['(', 'x', 'x', ')', '(', ')', '(', '.', '_', ']'],
                  ['(', 'x', 'x', ':', ';', ')', '(', ':', '-', '>'],
                  ['(', '.', '_', '_', ',', ')', '(', 'x', 'x', ')'],
                  ['(', ':', '-', '-', ';', ':', ';', 'x', 'x', ')'],
                  ['[', '_', '_', '_', '_', '_', '_', '_', '_', ']']]
                  )

        collisions.set_handler(state, collision_handler)

        text.load_font(state, "DroidSansMonoDotted16x32", "assets/img/fonts/DroidSansMonoDotted16x32.png", 16, 32)

        entities.insert(state,
                "000_text_score",
                {
                        "*": {
                                "textures": (("text", "Score:0", "DroidSansMonoDotted16x32"),),
                        },
                },
                (0, 0, 0),
                (0,0),
                None,
                True,
                )

        entities.insert(state,
                "000_text_health",
                {
                        "*": {
                                "textures": (("text", "Health:100", "DroidSansMonoDotted16x32"),),
                        },
                },
                (fixpoint.float2fix(2.4), 0, 0),
                (0,0),
                None,
                True,
                )

        # We create the ENT_MAN entity which has 2 different sprite representations: standing and walking.
        # The idle sprite is the default sprite, since it starts with an asterisk (*). The animation of
        # the sprites is defined by a list of images that will be played in order, then repeated, where
        # the playback speed is defined individually for the sprite as well. We also define the starting
        # coordinates (in "map coordinates", which are relative to tile size, not pixels!), here [1,1],
        # the rotation amount of the entity (0 here) and an offset for drawing the sprite to the actual position,
        # here [0.25, 0.25].
        CIRCLE_RADIUS = fixpoint.div(fixpoint.float2fix(1.0 / 4.0), fixpoint.int2fix(2))
        entities.insert(state, ENT_MAN, {
                        "*idle": {
                                "textures": (
                                        "assets/img/sprites/man_idle/0.png",
                                        "assets/img/sprites/man_idle/1.png",
                                        "assets/img/sprites/man_idle/2.png",
                                        "assets/img/sprites/man_idle/3.png",
                                        "assets/img/sprites/man_idle/1.png",
                                        "assets/img/sprites/man_idle/0.png",
                                        "assets/img/sprites/man_idle/3.png",
                                        "assets/img/sprites/man_idle/2.png",
                                        ),
                                "speed": fixpoint.float2fix(333.0),
                        },
                        "walk": {
                                "textures": (
                                        "assets/img/sprites/man_walk/1.png",
                                        "assets/img/sprites/man_walk/2.png",
                                        "assets/img/sprites/man_walk/3.png",
                                        ),
                                "speed" : fixpoint.float2fix(150.0),
                        },
                }, (fixpoint.float2fix(1.0), fixpoint.float2fix(1.0), 0),
                (fixpoint.float2fix(-0.25), fixpoint.float2fix(-0.25)),
                collision=(("circle", CIRCLE_RADIUS, CIRCLE_RADIUS, CIRCLE_RADIUS,),),
                )

        # We add a mover that will translate joystick movement to moving the man around the area.
        # This particular mover needs the source of control, a factor for the strength of the movement,
        # the allowed range for the movement, what sprites to use for idle and moving state and if to
        # rotate the entity to the movement direction.
        controlled_mover.add(state,
                ENT_MAN,
                "joystick",
                fixpoint.float2fix(0.03),
                (0, 0, fixpoint.float2fix(10.0), fixpoint.float2fix(10.0)),
                ("*idle", "walk"),
                True)

        view.set_viewer(state, relative_viewer.create(state, ENT_MAN, [fixpoint.float2fix(-1.75), fixpoint.float2fix(-2.5)]))

        # The state object is finished.
        return state

def collision_handler(state, collisions_list):
        print str(collisions_list)
        for entity_name_1, entity_name_2 in collisions_list:
                if entity_name_1 == ENT_MAN and entity_name_2 != ENT_SHOT:
                        entities.undo_last_move(state, entity_name_1)

                if entity_name_1 == ENT_SHOT:
                        destroy_mover.add(state, ENT_SHOT, do_replace=True)

FIXP_TRAVEL_DISTANCE = fixpoint.int2fix(10)

SHOT_RADIUS = fixpoint.div(fixpoint.float2fix(1.0 / 8.0), fixpoint.int2fix(2))
def on_fire_button(state, button_pressed):
        if button_pressed and not entities.get(state, ENT_SHOT):
                man_pos = entities.get_pos(state, ENT_MAN)

                man_rot = man_pos[2]
                man_rot += fixpoint.int2fix(90)

                heading_x = fixpoint_trig.cos(man_rot)
                heading_y = fixpoint_trig.sin(man_rot)

                heading = (heading_x, heading_y)
                heading = (fixpoint.mul(FIXP_TRAVEL_DISTANCE, heading[0]),
                           fixpoint.mul(FIXP_TRAVEL_DISTANCE, heading[1]))

                entities.insert(state, ENT_SHOT, {
                                                  "*": {
                                                        "textures": (
                                                                     "assets/img/sprites/throwingstar/0.png",
                                                                     ),
                                                        "speed": 0,
                                                        },
                                                  },
                                man_pos,
                                (fixpoint.float2fix(-0.125),
                                 fixpoint.float2fix(-0.125)
                                 ),
                                collision=(("circle", SHOT_RADIUS, SHOT_RADIUS, SHOT_RADIUS,),),
                                )
                linear_mover.add(state, ENT_SHOT, heading, fixpoint.float2fix(4.0), ("const", fixpoint.float2fix(-1.0)), None, True)
                destroy_mover.add(state, ENT_SHOT)
