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
import yapyg.viewers.relative

def create(screen_width, screen_height, tile_size):
        state = yapyg.factory.create(screen_width, screen_height, tile_size)

        yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/grass.png",])
        yapyg.tiles.add_tile_def(state, "+", ["assets/img/tiles/grass.png", "assets/img/tiles/brown_ground.png"])
        yapyg.tiles.add_tile_def(state, "t", ["assets/img/tiles/grass.png", "assets/img/tiles/tree.png"])

        yapyg.tiles.load_walls(state, "", "assets/img/tiles/grass.png", "assets/img/tiles/bricks_walls.png")

        area_strings = (
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+.6aa7.3....",
                "......+.9tt9.9....",
                "......+.9tt9.9....",
                "......+.5aa8.1....",
                "......+...........",
                "......+.2aa4......",
                "......+...........",
                "......+...........",
                "......+...........",
                "......+...........",
                )

        area = []
        for area_string_row in area_strings:
                new_row = []
                area.append(new_row)
                for tile in area_string_row:
                        new_row.append(tile)

        yapyg.tiles.set_area(state, area)

        yapyg.entities.insert(state, "man",
                {
                        "idle": {
                                "textures": [("assets/img/sprites/man_idle/%d.png" % i) for i in [0,1,2,3,1,0,3,2]],
                                "speed": 333,
                        },
                        "walk": {
                                "textures": [("assets/img/sprites/man_walk/%d.png" % i) for i in [1,2,3]],
                                "speed" : 150,
                        },
                }, [7, 5], 0, [0.25, 0.25])

        start_movement(state, None)

        yapyg.view.set_viewer(state, yapyg.viewers.relative.create(state, "man", [-1.5, -2.5]))

        return state

def start_movement(state, mover_name):
        path = [[5, 0], [0, 5], [-5, 0], [0, -5]]
        for index in xrange(len(path)):
                yapyg.movers.set_property.add(state, "man", "set_active_sprite", "idle")
                yapyg.movers.wait.add(state, "man", 2.0)
                yapyg.movers.set_property.add(state, "man", "set_active_sprite", "walk")
                yapyg.movers.linear.add(state, "man", path[index], 1.0,
                        True, None if index != len(path) - 1 else start_movement)
