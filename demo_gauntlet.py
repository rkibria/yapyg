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

# Called from the menu widget, this function creates and
# sets up the game state object. Parameters are the usable
# screen size and tile size in pixels.
def create(screen_width_px, screen_height_px, tile_size_px):
        # If there is an on-screen joystick
        # (there may not be one needed for non-mobile or other platforms)
        # set the drawing origin to above it (WORK IN PROGRESS, this needs a
        # cleaner solution).
        joystick_props = yapyg.controls.get_joystick_properties()
        origin_xy = (0, joystick_props["h"] * screen_height_px)

        # Create the actual game state object that stores all information that yapyg needs.
        state = yapyg.factory.create(screen_width_px, screen_height_px, tile_size_px, origin_xy)
        
        # Enable the joystick.
        yapyg.controls.add_joystick(state)

        # Create some tiles to use for our game area. Individual tiles are referred to by strings.
        # Each tile can be composed by layering several images over each other
        yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/dirtysquares.png",])

        # Special wall tile import helper.
        yapyg.tiles.load_walls(state, "", "assets/img/tiles/dirtysquares.png", "assets/img/tiles/bricks_walls.png")

        # The tile map is made as a list of lists. The arrangement is drawn as seen here,
        # i.e. the '5' tile is in the lower left corner of the screen.
        yapyg.tiles.set_area(state,
                [
                ['6', 'a', 'a', '7'],
                ['9', '.', '.', '9'],
                ['9', '.', '.', '9'],
                ['9', '.', '.', '9'],
                ['5', 'a', 'a', '8'],
                ])

        # We create the "man" entity which has 2 different sprite representations: standing and walking.
        # The idle sprite is the default sprite, since it starts with an asterisk (*). The animation of
        # the sprites is defined by a list of images that will be played in order, then repeated, where
        # the playback speed is defined individually for the sprite as well. We also define the starting
        # coordinates (in "map coordinates", which are relative to tile size, not pixels!), here [1,1],
        # the rotation amount of the entity (0 here) and an offset for drawing the sprite to the actual position,
        # here [0.25, 0.25].
        yapyg.entities.insert(state, "man", {
                        "*idle": {
                                "textures": [("assets/img/sprites/man_idle/%d.png" % i) for i in [0,1,2,3,1,0,3,2]],
                                "speed": 333,
                        },
                        "walk": {
                                "textures": [("assets/img/sprites/man_walk/%d.png" % i) for i in [1,2,3]],
                                "speed" : 150,
                        },
                }, [1, 1], 0, [0.25, 0.25])

        # We add a mover that will translate joystick movement to moving the man around the area.
        # This particular mover needs the source of control, a factor for the strength of the movement,
        # the allowed range for the movement, what sprites to use for idle and moving state and if to
        # rotate the entity to the movement direction.
        yapyg.movers.controlled.add(state,
                "man",
                "joystick",
                0.03,
                [0, 0, 3, 4],
                ["*idle", "walk"],
                True)

        # The state object is finished.
        return state
