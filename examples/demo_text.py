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

import math
import time

from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import fixpoint
from yapyg import text
from yapyg import timer
from yapyg_movers import linear_mover

def get_time_string():
        return time.strftime("%H:%M:%S", time.localtime())

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        tiles.add_tile_def(state, ".", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

        text.load_font(state, "DroidSansMonoDotted32x64", "assets/img/fonts/DroidSansMonoDotted32x64.png", 32, 64)
        text.load_font(state, "DroidSansMonoDotted16x32", "assets/img/fonts/DroidSansMonoDotted16x32.png", 16, 32)
        text.load_font(state, "DroidSansMonoDotted12x24", "assets/img/fonts/DroidSansMonoDotted12x24.png", 12, 24)
        text.load_font(state, "DroidSansMonoDotted10x16", "assets/img/fonts/DroidSansMonoDotted10x16.png", 10, 16)
        text.load_font(state, "DroidSansMonoDotted8x12", "assets/img/fonts/DroidSansMonoDotted8x12.png", 8, 12)

        entities.insert(state,
                "500_text_1",
                {
                        "*": {
                                "textures": (("text", "This is text\nSecond line", "DroidSansMonoDotted16x32"),),
                        },
                },
                (fixpoint.int2fix(1), fixpoint.int2fix(2), 0))

        start_movement(state, None)

        entities.insert(state,
                "500_text_2",
                {
                        "*": {
                                "textures": (("text", 
                                                "Lorem ipsum dolor sit amet, consectetur adipisici elit,\n"
                                                "sed eiusmod tempor incidunt ut labore et dolore magna aliqua.\n"
                                                "Ut enim ad minim veniam, quis nostrud exercitation ullamco\n"
                                                "laboris nisi ut aliquid ex ea commodi consequat. Quis aute\n"
                                                "iure reprehenderit in voluptate velit esse cillum dolore eu\n"
                                                "fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non\n"
                                                "proident, sunt in culpa qui officia deserunt mollit anim id\n"
                                                "est laborum.",
                                        "DroidSansMonoDotted8x12"),),
                        },
                },
                (0, fixpoint.int2fix(4), 0))

        entities.insert(state,
                "500_text_3",
                {
                        "*": {
                                "textures": (("text", "Title", "DroidSansMonoDotted10x16"),),
                        },
                },
                (0, fixpoint.int2fix(5), 0))

        entities.insert(state,
                "500_text_4",
                {
                        "*": {
                                "textures": (("text", "Chapter", "DroidSansMonoDotted12x24"),),
                        },
                },
                (0, fixpoint.float2fix(5.5), 0))

        entities.insert(state,
                "500_text_time",
                {
                        "*": {
                                "textures": (("text", get_time_string(), "DroidSansMonoDotted32x64"),),
                        },
                },
                (0.0, fixpoint.float2fix(0.5), 0))

        timer.create(state, on_timer, fixpoint.int2fix(1000))

        return state

def on_timer(state, last_frame_delta):
        entities.set_sprite(state,
                "500_text_time",
                "*",
                {
                        "textures": (("text", get_time_string(), "DroidSansMonoDotted32x64"),),
                        })

def start_movement(state, mover_name):
        n_steps = 20
        for index in xrange(n_steps):
                degrees = float(index) / n_steps * 360.0
                dx = math.cos(math.radians(degrees)) / n_steps
                dy = math.sin(math.radians(degrees)) / n_steps
                linear_mover.add(state, "500_text_1",
                        (fixpoint.float2fix(dx), fixpoint.float2fix(dy)),
                        fixpoint.float2fix(0.5),
                        ("auto", 0), None if index != n_steps - 1 else start_movement)
