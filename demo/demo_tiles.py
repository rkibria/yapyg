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

from yapyg import view
from yapyg_movers import linear_mover
from yapyg_movers import wait_mover
from yapyg_movers import set_property_mover
from yapyg_viewers import relative_viewer
from yapyg_helpers import tiles_helpers

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        tiles.add_tile_def(state, " ", ("assets/img/tiles/grass.png",))
        tiles.add_tile_def(state, "+", ("assets/img/tiles/grass.png", "assets/img/tiles/brown_ground.png"))
        tiles.add_tile_def(state, "t", ("assets/img/tiles/grass.png", "assets/img/tiles/tree.png"))

        tiles_helpers.load_walls(state, "", "assets/img/tiles/grass.png", "assets/img/tiles/bricks_walls.png")

        area_strings = (
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +.____,     ",
                "      +)<-->(     ",
                "      +)(tt)(     ",
                "      +)(tt)(     ",
                "      +)[__](     ",
                "      +:----;     ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                "      +           ",
                )
        area = tiles_helpers.strings_to_chars(area_strings)
        tiles.set_area(state, area)

        entities.insert(state, "man",
                {
                        "idle": {
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
                                "speed": 333.0,
                        },
                        "walk": {
                                "textures": (
                                        "assets/img/sprites/man_walk/1.png",
                                        "assets/img/sprites/man_walk/2.png",
                                        "assets/img/sprites/man_walk/3.png",
                                        ),
                                "speed" : 150.0,
                        },
                }, (7.0, 5.0, 0), (0.25, 0.25))

        start_movement(state, None)

        view.set_viewer(state, relative_viewer.create(state, "man", [-1.5, -2.5]))

        return state

def start_movement(state, mover_name):
        path = ((5.0, 0), (0, 5.0), (-5.0, 0), (0, -5.0))
        for index in xrange(len(path)):
                set_property_mover.add(state, "man", "set_active_sprite", "idle")
                wait_mover.add(state, "man", 2.0)
                set_property_mover.add(state, "man", "set_active_sprite", "walk")
                rel_vector = ((path[index][0]), (path[index][1]))
                linear_mover.add(state, "man", rel_vector, 1.0,
                        ("auto", 0), None if index != len(path) - 1 else start_movement)
