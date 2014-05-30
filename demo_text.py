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
import yapyg

def get_time_string():
        return time.strftime("%H:%M:%S", time.localtime())

def create(screen_width, screen_height, tile_size):
        state = yapyg.factory.create(screen_width, screen_height, tile_size)

        yapyg.tiles.add_tile_def(state, ".", ["assets/img/tiles/gray_square.png",])
        yapyg.tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

        yapyg.text.load_font(state, "DroidSansMonoDotted32x64", "assets/img/fonts/DroidSansMonoDotted32x64.png", 32, 64)
        yapyg.text.load_font(state, "DroidSansMonoDotted16x32", "assets/img/fonts/DroidSansMonoDotted16x32.png", 16, 32)
        yapyg.text.load_font(state, "DroidSansMonoDotted12x24", "assets/img/fonts/DroidSansMonoDotted12x24.png", 12, 24)
        yapyg.text.load_font(state, "DroidSansMonoDotted8x12", "assets/img/fonts/DroidSansMonoDotted8x12.png", 8, 12)

        yapyg.entities.insert(state,
                "500_text_1",
                {
                        "*": {
                                "textures": [("text", "This is text\nSecond line", "DroidSansMonoDotted16x32")],
                        },
                },
                [1, 2])

        start_movement(state, None)

        yapyg.entities.insert(state,
                "500_text_2",
                {
                        "*": {
                                "textures": [("text", 
                                                "Lorem ipsum dolor sit amet, consectetur adipisici elit,\n"
                                                "sed eiusmod tempor incidunt ut labore et dolore magna aliqua.\n"
                                                "Ut enim ad minim veniam, quis nostrud exercitation ullamco\n"
                                                "laboris nisi ut aliquid ex ea commodi consequat. Quis aute\n"
                                                "iure reprehenderit in voluptate velit esse cillum dolore eu\n"
                                                "fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non\n"
                                                "proident, sunt in culpa qui officia deserunt mollit anim id\n"
                                                "est laborum.",
                                        "DroidSansMonoDotted8x12")],
                        },
                },
                [0, 4])

        yapyg.entities.insert(state,
                "500_text_3",
                {
                        "*": {
                                "textures": [("text", "Title", "DroidSansMonoDotted12x24")],
                        },
                },
                [0, 5])

        yapyg.entities.insert(state,
                "500_text_time",
                {
                        "*": {
                                "textures": [("text", get_time_string(), "DroidSansMonoDotted32x64")],
                        },
                },
                [0.0, 0.5])

        yapyg.timer.create(state, on_timer, 1000000)

        return state

def on_timer(state, last_frame_delta):
        yapyg.entities.set_sprite(state, "500_text_time", "*", {"textures": [("text", get_time_string(), "DroidSansMonoDotted32x64")],})

def start_movement(state, mover_name):
        n_steps = 1000
        for index in xrange(n_steps):
                degrees = float(index) / n_steps * 360.0
                yapyg.movers.linear.add(state, "500_text_1",
                        (math.cos(math.radians(degrees)) / 1000.0, math.sin(math.radians(degrees)) / 1000.0),
                        0.5 / 1000000,
                        True, None if index != n_steps - 1 else start_movement)
