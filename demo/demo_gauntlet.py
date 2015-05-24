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

import math

from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import controls
from yapyg import text
from yapyg import view
from yapyg import collisions
from yapyg import user
from yapyg_movers import controlled_mover
from yapyg_movers import linear_mover
from yapyg_movers import destroy_mover
from yapyg_viewers import relative_viewer
from yapyg_helpers import tiles_helpers

DEBUG_MODE = False

ENT_MAN = "500_man"
ENT_SHOT = "600_throwingstar"
ENT_GHOST = "700_ghost"
ENT_TEXT_SCORE = "text_score"
ENT_TEXT_HEALTH = "text_health"
ENT_PREFIX_COINS = "700_coins"

FONT_NAME = "DroidSansMonoDotted16x32"

USERDATA_SCORE = "score"

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
        if not DEBUG_MODE:
                floor_tile = "assets/img/tiles/dirtysquares.png"
        else:
                floor_tile = "assets/img/tiles/grid_double.png"

        tiles.add_tile_def(state, "x", (floor_tile,))
        if DEBUG_MODE:
                TILE_SIZE = 1.0
                tiles.add_tile_def(state, "#", ("assets/img/tiles/plain.png",), (("rectangle", 0, 0, TILE_SIZE, TILE_SIZE),))

        # Special wall tile import helper.
        if not DEBUG_MODE:
                tiles_helpers.load_walls(state, "", floor_tile, "assets/img/tiles/bricks_walls.png")
        else:
                tiles_helpers.load_walls(state, "", floor_tile, "assets/img/tiles/grid_quad_walls.png")

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

        text.load_font(state, FONT_NAME, "assets/img/fonts/%s.png" % FONT_NAME, 16, 32)

        user.set_data(state, USERDATA_SCORE, 0)
        entities.insert(state,
                        ENT_TEXT_SCORE,
                        {
                                "*": {
                                      "textures": (("text", "Score:0", FONT_NAME),),
                                      },
                         },
                        (0, 0, 0),
                        (0,0),
                        None,
                        True,
                        )

        entities.insert(state,
                        ENT_TEXT_HEALTH,
                        {
                         "*": {
                               "textures": (("text", "Health:100", FONT_NAME),),
                               },
                         },
                        (2.4, 0, 0),
                        (0,0),
                        None,
                        True,
                        )

        # We create the ENT_MAN entity which has 2 different sprite representations: standing and walking.
        # The idle sprite is the default sprite, since it starts with an asterisk (*).

        # The animation of the sprites is defined by a list of images that will be played in order,
        # then repeated, where the playback speed is defined individually for the sprite as well.

        # We define the starting coordinates (in "map coordinates", which are relative to tile size, not pixels!), here [1,1],
        # the rotation amount of the entity (0 here) and an offset for drawing the sprite to the actual position,
        # here [0.25, 0.25].
        MAN_SIZE = 1.0 / 2.0 # 64 px = 128 px tile / 2
        MAN_RADIUS = MAN_SIZE / 2.0
        MAN_OFFSET = -MAN_RADIUS # entity position defines the center of the sprite (sprite drawn left+lower of position)
        if not DEBUG_MODE:
                man_idle_textures = (
                                     "assets/img/sprites/man_idle/0.png",
                                     "assets/img/sprites/man_idle/1.png",
                                     "assets/img/sprites/man_idle/2.png",
                                     "assets/img/sprites/man_idle/3.png",
                                     "assets/img/sprites/man_idle/1.png",
                                     "assets/img/sprites/man_idle/0.png",
                                     "assets/img/sprites/man_idle/3.png",
                                     "assets/img/sprites/man_idle/2.png",
                                     )
                man_walk_textures = (
                                     "assets/img/sprites/man_walk/1.png",
                                     "assets/img/sprites/man_walk/2.png",
                                     "assets/img/sprites/man_walk/3.png",
                                     )
        else:
                man_idle_textures = (
                                     "assets/img/sprites/half_ball.png",
                                     )
                man_walk_textures = (
                                     "assets/img/sprites/half_ball.png",
                                     )

        entities.insert(state,
                        ENT_MAN,
                        {
                         "*idle": {
                                   "textures": man_idle_textures,
                                   "speed": 333.0,
                                   },
                         "walk": {
                                  "textures": man_walk_textures,
                                  "speed" : 150.0,
                                  },
                         },
                        (1.0, 1.0, 0),
                        (MAN_OFFSET, MAN_OFFSET),
                        collision=(("circle", MAN_RADIUS, MAN_RADIUS, MAN_RADIUS,),),
                        )

        # A pile of coins
        COINS_SIZE = 1.0 / 2.0 # 64 px = 128 px tile / 2
        COINS_RADIUS = COINS_SIZE / 2.0
        COINS_OFFSET = -COINS_RADIUS
        if not DEBUG_MODE:
                coin_textures = ("assets/img/sprites/coins/0.png",
                                 "assets/img/sprites/coins/1.png",
                                 "assets/img/sprites/coins/2.png",
                                 "assets/img/sprites/coins/1.png",
                                 )
        else:
                coin_textures = ("assets/img/sprites/half_ball_2.png",)
        entities.insert(state,
                        "%s_1" % (ENT_PREFIX_COINS),
                        {
                         "*": {
                               "textures": coin_textures,
                               "speed": 150.0,
                               },
                         },
                        (1.0, 7.0, 0),
                        (COINS_OFFSET, COINS_OFFSET),
                        collision=(("circle", COINS_RADIUS, COINS_RADIUS, COINS_RADIUS,),),
                        )

        GHOST_SIZE = 1.0
        GHOST_RADIUS = GHOST_SIZE / 2.0
        GHOST_OFFSET = -(GHOST_RADIUS)
        if not DEBUG_MODE:
                ghost_textures = (
                                  "assets/img/sprites/ghost/1.png",
                                  "assets/img/sprites/ghost/2.png",
                                  "assets/img/sprites/ghost/3.png",
                                  "assets/img/sprites/ghost/2.png",
                                )
        else:
                ghost_textures = ("assets/img/sprites/full_ball.png",)

        entities.insert(state,
                        ENT_GHOST,
                        {
                         "*": {
                                   "textures": ghost_textures,
                                   "speed": 200.0,
                                   },
                         },
                        (1.0, 3.0, 0),
                        (GHOST_OFFSET, GHOST_OFFSET), # sprite appears lower and more left of actual entity position
                        collision=(("circle", GHOST_RADIUS, GHOST_RADIUS, GHOST_RADIUS,),),
                        )

        # We add a mover that will translate joystick movement to moving the man around the area.
        # This particular mover needs the source of control, a factor for the strength of the movement,
        # the allowed range for the movement, what sprites to use for idle and moving state and if to
        # rotate the entity to the movement direction.
        controlled_mover.add(state,
                             ENT_MAN,
                             "joystick",
                             0.03,
                             (0, 0, 10.0, 10.0),
                             ("*idle", "walk"),
                             True
                             )

        view.set_viewer(state,
                        relative_viewer.create(state,
                                               ENT_MAN,
                                               [-2.0, -2.25]))

        start_ghost_movement(state, None)

        # The state object is finished.
        return state

def start_ghost_movement(state, mover_name):
        path = (
                (2.0, 0.0),
                (0.0, 2.0),
                (-2.0, 0.0),
                (0.0, -2.0),
                )
        for index in xrange(len(path)):
                rel_vector = ((path[index][0]), (path[index][1]))
                linear_mover.add(state, ENT_GHOST, rel_vector, 1.0, on_end_function=None if index != len(path) - 1 else start_ghost_movement)

def collision_handler(state, collisions_list):
        # print str(collisions_list)
        for entity_name_1, entity_name_2 in collisions_list:
                if entity_name_1 == ENT_MAN:
                        if entity_name_2 == ENT_SHOT:
                                pass
                        elif entity_name_2[0:len(ENT_PREFIX_COINS)] == ENT_PREFIX_COINS:
                                score = user.get_data(state, USERDATA_SCORE)
                                score += 10
                                score_text = "Score:%d" % score
                                user.set_data(state, USERDATA_SCORE, score)
                                entities.set_sprite(state,
                                                    ENT_TEXT_SCORE,
                                                    "*",
                                                    {
                                                     "textures": (("text", score_text, FONT_NAME),),
                                                     },
                                                    screen_relative=True,
                                                    )
                                destroy_mover.add(state, entity_name_2, do_replace=True)
                        else:
                                entities.undo_last_move(state, entity_name_1)
                elif entity_name_1 == ENT_SHOT:
                        if entity_name_2[0:len(ENT_PREFIX_COINS)] == ENT_PREFIX_COINS:
                                pass
                        elif entity_name_2 == ENT_GHOST:
                                do_ghost_boom(state, entities.get_pos(state, ENT_GHOST))
                                destroy_mover.add(state, ENT_GHOST, do_replace=True)
                                do_shot_boom(state, entities.get_pos(state, ENT_SHOT))
                                destroy_mover.add(state, ENT_SHOT, do_replace=True)
                        else:
                                do_shot_boom(state, entities.get_pos(state, ENT_SHOT))
                                destroy_mover.add(state, ENT_SHOT, do_replace=True)

TRAVEL_DISTANCE = 10
START_OFFSET_FACTOR = 0.25
SHOT_RADIUS = (((1.0 / 8.0)) / 2)
SHOT_SPRITE_OFFSET = (-0.125, -0.125) 
SHOT_SPEED = 4.0
SHOT_ROTATE_SPEED = -1.0
SHOT_ROTATE_DEF = ("const", SHOT_ROTATE_SPEED)
SHOT_COLLISION_DEF = (("circle", SHOT_RADIUS, SHOT_RADIUS, SHOT_RADIUS,),)
if not DEBUG_MODE:
        shot_textures = ("assets/img/sprites/throwingstar/0.png",)
else:
        shot_textures = ("assets/img/sprites/quarter_ball.png",)
SHOT_SPRITE_DEF = {
                   "*": {
                         "textures": shot_textures,
                         "speed": 0,
                         },
                   }

def on_fire_button(state, button_pressed):
        if button_pressed and not entities.get(state, ENT_SHOT):
                man_pos = entities.get_pos(state, ENT_MAN)

                man_rot = math.radians(man_pos[2] + 90.0)

                heading_x = math.cos(man_rot)
                heading_y = math.sin(man_rot)

                start_pos = (man_pos[0] + (START_OFFSET_FACTOR * heading_x),
                             man_pos[1] + (START_OFFSET_FACTOR * heading_y),
                             0,
                             )

                heading = ((TRAVEL_DISTANCE * heading_x),
                           (TRAVEL_DISTANCE * heading_y),
                           )

                entities.insert(state,
                                ENT_SHOT,
                                SHOT_SPRITE_DEF,
                                start_pos,
                                SHOT_SPRITE_OFFSET,
                                collision=SHOT_COLLISION_DEF,
                                )

                linear_mover.add(state, ENT_SHOT, heading, SHOT_SPEED, SHOT_ROTATE_DEF, None, True)
                destroy_mover.add(state, ENT_SHOT)

SHOT_BOOM_TEXTURES = ("assets/img/sprites/explosion_small/0.png",
                 "assets/img/sprites/explosion_small/1.png",
                 "assets/img/sprites/explosion_small/2.png",
                 "assets/img/sprites/explosion_small/3.png",
                 "assets/img/sprites/explosion_small/4.png",
                 )
SHOT_BOOM_SPRITEDEF = {
                  "*": {
                        "textures": SHOT_BOOM_TEXTURES,
                        "speed": 50.0,
                        },
                  }
SHOT_BOOM_SPRITEOFFSET = (-0.125, -0.125)

def do_shot_boom(state, pos):
        entities.insert(state,
                        "shot_boom",
                        SHOT_BOOM_SPRITEDEF,
                        pos,
                        SHOT_BOOM_SPRITEOFFSET,
                        play_once=True,
                        )

GHOST_BOOM_TEXTURES = ("assets/img/sprites/explosion_smoke/0.png",
                       "assets/img/sprites/explosion_smoke/1.png",
                       "assets/img/sprites/explosion_smoke/2.png",
                       "assets/img/sprites/explosion_smoke/3.png",
                       "assets/img/sprites/explosion_smoke/4.png",
                       "assets/img/sprites/explosion_smoke/5.png",
                       "assets/img/sprites/explosion_smoke/6.png",
                       "assets/img/sprites/explosion_smoke/7.png",
                       )
GHOST_BOOM_SPRITEDEF = {
                  "*": {
                        "textures": GHOST_BOOM_TEXTURES,
                        "speed": 50.0,
                        },
                  }
GHOST_BOOM_SPRITEOFFSET = (-0.5, -0.5)

def do_ghost_boom(state, pos):
        entities.insert(state,
                        "ghost_boom",
                        GHOST_BOOM_SPRITEDEF,
                        pos,
                        GHOST_BOOM_SPRITEOFFSET,
                        play_once=True,
                        )

