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

import yapyg.factory
import yapyg.screen
import yapyg.movers.linear
import yapyg.movers.jump
import yapyg.movers.set_property
import yapyg.movers.wait
import yapyg.view
import yapyg.viewers.relative

def create(screen_width, screen_height, tile_size):
    state = yapyg.factory.create(screen_width, screen_height, tile_size)

    yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/grass.png",])

    yapyg.tiles.add_tile_def(state, "1", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/sw_x.png"])
    yapyg.tiles.add_tile_def(state, "2", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/s_x.png"])
    yapyg.tiles.add_tile_def(state, "3", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/se_x.png"])
    yapyg.tiles.add_tile_def(state, "4", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/e_x.png"])
    yapyg.tiles.add_tile_def(state, "5", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/ne_x.png"])
    yapyg.tiles.add_tile_def(state, "6", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/n_x.png"])
    yapyg.tiles.add_tile_def(state, "7", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/nw_x.png"])
    yapyg.tiles.add_tile_def(state, "8", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/w_x.png"])
    yapyg.tiles.add_tile_def(state, "9", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/x_1.png"])
    yapyg.tiles.add_tile_def(state, "0", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/x_2.png"])
    yapyg.tiles.add_tile_def(state, "!", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/x_4.png"])
    yapyg.tiles.add_tile_def(state, "$", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/x_3.png"])

    yapyg.tiles.add_tile_def(state, "+", ["assets/img/tiles/grass.png", "assets/img/tiles/road/I.png"])

    yapyg.tiles.add_tile_def(state, "t", ["assets/img/tiles/grass.png", "assets/img/tiles/tree.png"])

    area_strings = [
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+!2222$.....",
        "......+476658.....",
        "......+48tt48.....",
        "......+48tt48.....",
        "......+412238.....",
        "......+966660.....",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        "......+...........",
        ]

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
                "speed": 200000,
            },
            "walk": {
                "textures": [("assets/img/sprites/man_walk/%d.png" % i) for i in [1,2,3]],
                "speed" : 100000,
            },
        }, [6, 5], 0, [0.25, 0.25])

    start_movement(state, None)

    yapyg.view.set_viewer(state, yapyg.viewers.relative.create(state, "man", [-1.5, -1.5]))

    return state

def start_movement(state, mover_name):
    path = [[6, 0], [0, 5], [-6, 0], [0, -5]]
    for index in xrange(len(path)):
        yapyg.movers.set_property.add(state, "man", "set_sprite", "idle")
        yapyg.movers.wait.add(state, "man", 500000)
        yapyg.movers.set_property.add(state, "man", "set_sprite", "walk")
        yapyg.movers.linear.add(state, "man", path[index], 1.0 / 1000000,
            True, None if index != len(path) - 1 else start_movement)
