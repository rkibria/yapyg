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
    joystick_props = yapyg.controls.get_joystick_properties()
    origin_xy = (0, joystick_props["h"] * screen_height)
    state = yapyg.factory.create(screen_width, screen_height, tile_size, origin_xy)

    yapyg.controls.add_joystick(state)

    yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/grass.png",])

    yapyg.tiles.add_tile_def(state, "1", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/sw_x.png"])
    yapyg.tiles.add_tile_def(state, "2", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/s_x.png"])
    yapyg.tiles.add_tile_def(state, "3", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/se_x.png"])
    yapyg.tiles.add_tile_def(state, "4", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/e_x.png"])
    yapyg.tiles.add_tile_def(state, "5", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/ne_x.png"])
    yapyg.tiles.add_tile_def(state, "6", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/n_x.png"])
    yapyg.tiles.add_tile_def(state, "7", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/nw_x.png"])
    yapyg.tiles.add_tile_def(state, "8", ["assets/img/tiles/grass.png", "assets/img/tiles/brick/w_x.png"])

    area_strings = [
        "765",
        "8.4",
        "8.4",
        "8.4",
        "123",
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
            "*idle": {
                "textures": [("assets/img/sprites/man_idle/%d.png" % i) for i in [0,1,2,3,1,0,3,2]],
                "speed": 200000,
            },
            "walk": {
                "textures": [("assets/img/sprites/man_walk/%d.png" % i) for i in [1,2,3]],
                "speed" : 100000,
            },
        }, [1, 1], 0, [0.25, 0.25])

    yapyg.movers.controlled.add(state,
        "man",
        "joystick",
        0.1,
        [0, 0, 2, 4])

    return state
